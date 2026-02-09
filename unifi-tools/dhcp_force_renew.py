#!/usr/bin/env python3
"""
Villa Romanza — UniFi DHCP Force Renewal & IP Reservation Tool
==============================================================

Reusable script for managing fixed IP reservations on the UniFi
Enterprise Fortress Gateway via REST API.

Features:
  - 2FA email authentication
  - CSRF token handling (auto-refreshed)
  - Create/update fixed IP reservations
  - PoE power-cycle for PoE-powered devices (touch panels, etc.)
  - Gateway force-provision to clear DHCP lease table
  - Verification with ping checks

Usage:
  # Full run: set reservations + force renewal
  python3 dhcp_force_renew.py

  # Just verify current IP status
  python3 dhcp_force_renew.py --verify

  # Only PoE-cycle touch panels (no reservation changes)
  python3 dhcp_force_renew.py --poe-only

  # Set reservations without forcing renewal
  python3 dhcp_force_renew.py --reserve-only

  # Force-provision gateway + PoE cycle (no reservation changes)
  python3 dhcp_force_renew.py --renew-only

  # Restart all edge switches — most reliable for non-PoE devices
  python3 dhcp_force_renew.py --restart-switches

  # Bounce specific ports on a switch via SSH (works for ANY port)
  python3 dhcp_force_renew.py --bounce-ports 192.168.1.4:19-23

Requirements:
  Python 3.x (stdlib only — no pip packages needed)
  sshpass (for --bounce-ports and --restart-switches SSH operations)
"""

import os
import urllib.request
import urllib.error
import http.cookiejar
import json
import ssl
import sys
import time
import subprocess
import argparse
from typing import Optional

# ============================================================
# Configuration (credentials from environment variables)
# Set via .env file or export before running:
#   export UNIFI_USER="user@example.com"
#   export UNIFI_PASS="password"
#   export UNIFI_SSH_USER="ssh_user"
#   export UNIFI_SSH_PASS="ssh_pass"
# ============================================================

BASE_URL = os.environ.get("UNIFI_URL", "https://192.168.1.1")
USERNAME = os.environ.get("UNIFI_USER", "")
PASSWORD = os.environ.get("UNIFI_PASS", "")
SITE = os.environ.get("UNIFI_SITE", "default")

# Network config IDs (from UniFi)
CORE_NET_ID = "68315f82f4f53a4a462e1371"
LIGHTING_NET_ID = "6986c3f971a8266c28860dd1"

# Gateway
GW_MAC = "28:70:4e:27:97:49"

# Temporary lease time during renewal (seconds)
TEMP_LEASE_TIME = 120

# Original lease time to restore (seconds)
NORMAL_LEASE_TIME = 86400

# SSH credentials for UniFi switches (from Site settings > Device SSH)
SW_SSH_USER = os.environ.get("UNIFI_SSH_USER", "")
SW_SSH_PASS = os.environ.get("UNIFI_SSH_PASS", "")

# ============================================================
# Reservation Data
# ============================================================

# Format: (name, mac, fixed_ip)
# Grouped by category for readability

RESERVATIONS_CORE = [
    # VRROOM
    ("VRROOM", "18:9b:a5:d4:12:cb", "192.168.1.70"),
    # TVs
    ("TV-MasterCinema", "60:75:6c:32:c3:f2", "192.168.1.71"),
    ("TV-Theatre", "58:96:0a:40:cc:9f", "192.168.1.72"),
    ("TV-DownGuest", "1c:f4:3f:0d:80:c4", "192.168.1.73"),
    ("TV-Sunroom", "b0:37:95:16:fd:f0", "192.168.1.74"),
    ("TV-Cabana", "08:27:a8:23:50:62", "192.168.1.78"),
    # Apple TVs
    ("ATV-MasterCinema", "c4:f7:c1:2b:09:68", "192.168.1.76"),
    ("ATV-Theatre", "c0:95:6d:58:1a:5d", "192.168.1.77"),
    ("ATV-DownGuest", "c4:f7:c1:12:c4:ba", "192.168.1.79"),
    ("ATV-Sunroom", "f0:b3:ec:32:ed:c5", "192.168.1.80"),
    ("ATV-Cabana", "f0:b3:ec:28:fa:60", "192.168.1.81"),
    # Crestron Touch Panels (PoE powered)
    ("TP-Lounge", "c4:42:68:25:33:67", "192.168.1.82"),
    ("TP-Entrata", "c4:42:68:63:85:e0", "192.168.1.83"),
    ("TP-Kitchen", "c4:42:68:68:81:7a", "192.168.1.84"),
    ("TP-VillaMaster", "c4:42:68:63:83:83", "192.168.1.85"),
    ("TP-Cabana", "c4:42:68:63:83:2e", "192.168.1.86"),
    ("TP-Garage", "00:10:7f:ef:fd:c1", "192.168.1.87"),
    ("TP-VillaHis", "c4:42:68:63:88:24", "192.168.1.88"),
    ("TP-CavaRomanza", "c4:42:68:63:82:57", "192.168.1.89"),
    ("TP-Veranda", "c4:42:68:63:82:ea", "192.168.1.90"),
    ("TP-Dining", "c4:42:68:68:73:05", "192.168.1.91"),
    ("TP-VillaHers", "c4:42:68:63:8e:1b", "192.168.1.92"),
    ("TP-LaundryDown", "c4:42:68:63:85:c9", "192.168.1.93"),
    ("TP-NorthPorta", "c4:42:68:68:73:ed", "192.168.1.94"),
    ("TP-Library", "c4:42:68:68:b3:cc", "192.168.1.95"),
    # Sonos Speakers
    ("SNS-Library", "80:4a:f2:ae:30:5b", "192.168.0.100"),
    ("SNS-Lounge", "c4:38:75:8d:3e:24", "192.168.0.101"),
    ("SNS-Kitchen", "74:ca:60:41:8e:61", "192.168.0.102"),
    ("SNS-Dining", "80:4a:f2:ae:30:61", "192.168.0.103"),
    ("SNS-Entrata", "80:4a:f2:a8:43:78", "192.168.0.104"),
    ("SNS-Hers", "80:4a:f2:ae:c6:b2", "192.168.0.105"),
    ("SNS-MasterEntry", "80:4a:f2:ae:c6:c1", "192.168.0.106"),
    ("SNS-His", "74:ca:60:41:8f:66", "192.168.0.107"),
    ("SNS-BlueBedroom", "80:4a:f2:ae:c6:f1", "192.168.0.109"),
    ("SNS-PinkBedroom", "80:4a:f2:ae:a2:10", "192.168.0.110"),
    ("SNS-GuestUp", "c4:38:75:8b:b9:83", "192.168.0.111"),
    ("SNS-GuestDown", "80:4a:f2:ae:c0:be", "192.168.0.112"),
    ("SNS-Garage", "80:4a:f2:ae:c6:df", "192.168.0.113"),
    ("SNS-Wine", "80:4a:f2:a8:42:b2", "192.168.0.114"),
    ("SNS-Porch", "80:4a:f2:a8:42:a3", "192.168.0.115"),
    ("SNS-Lawn", "38:42:0b:26:92:5e", "192.168.0.116"),
    ("SNS-Picnic", "80:4a:f2:a9:7d:07", "192.168.0.117"),
    ("SNS-PoolNorth", "38:42:0b:26:93:39", "192.168.0.118"),
    ("SNS-PoolSouth", "74:ca:60:49:18:8a", "192.168.0.119"),
    ("SNS-PoolEast", "74:ca:60:e0:9a:32", "192.168.0.120"),
    ("SNS-Cabana", "c4:38:75:8b:7d:80", "192.168.0.121"),
    ("SNS-PT-Bar", "38:42:0b:8f:11:ae", "192.168.0.122"),
    ("SNS-PT-SyncFeed", "38:42:0b:8f:0c:ce", "192.168.0.123"),
    ("SNS-PT-Sunroom", "00:1b:66:04:0a:e9", "192.168.0.124"),
    ("SNS-PicnicSub", "74:ca:60:31:da:dc", "192.168.0.125"),
    # AVRs
    ("AVR-Bar", "50:1e:2d:43:a0:c0", "192.168.0.130"),
    ("AVR-Master", "50:1e:2d:43:93:72", "192.168.0.131"),
    ("AVR-Sunroom", "7c:b7:7b:04:29:d1", "192.168.0.132"),
    # Mac Minis
    ("Mech-Mac", "d0:11:e5:ed:43:d4", "192.168.0.140"),
    # Other
    ("PNT-Library", "24:6a:0e:59:7c:ba", "192.168.0.150"),
    ("Ramonas-iMac", "78:7b:8a:aa:e4:ba", "192.168.0.151"),
    ("Villa-Chime-Plug", "58:d6:1f:1e:41:93", "192.168.0.155"),
]

RESERVATIONS_LIGHTING = [
    # Hue Bridges (VLAN 20)
    ("HueB-01-Bar", "c4:29:96:b4:14:ba", "192.168.20.10"),
    ("HueB-02-GreatRoom", "c4:29:96:b4:22:48", "192.168.20.11"),
    ("HueB-03-Chandelier", "c4:29:96:b0:3d:af", "192.168.20.12"),
    ("HueB-04-Dining", "c4:29:96:b4:12:89", "192.168.20.13"),
    ("HueB-05-GroundFX", "c4:29:96:b4:19:65", "192.168.20.14"),
    ("HueB-06-Loggia", "c4:29:96:b8:d9:4b", "192.168.20.15"),
    ("HueB-07-Entrata", "c4:29:96:c4:23:fd", "192.168.20.16"),
    ("HueB-08-Library", "c4:29:96:b4:23:2f", "192.168.20.17"),
    ("HueB-09-1stGuest", "c4:29:96:b4:14:b3", "192.168.20.18"),
    ("HueB-10-Upstairs", "c4:29:96:b4:12:ef", "192.168.20.19"),
    ("HueB-11-Kitchen", "c4:29:96:b0:68:ea", "192.168.20.20"),
    ("HueB-12-SunRoom", "c4:29:96:b4:28:73", "192.168.20.21"),
    ("HueB-13-SouthHall", "c4:29:96:b4:15:83", "192.168.20.22"),
    ("HueB-14-Master", "c4:29:96:b0:3f:32", "192.168.20.23"),
    ("HueB-15-Studio", "c4:29:96:b4:1e:6d", "192.168.20.24"),
    ("HueB-17-Veranda", "c4:29:96:b4:14:bc", "192.168.20.25"),
    ("HueB-18-WestLawn", "c4:29:96:b4:1a:0e", "192.168.20.26"),
    ("HueB-19-Gate", "c4:29:96:ba:11:b2", "192.168.20.27"),
    ("HueB-19-Roof", "c4:29:96:b0:3b:eb", "192.168.20.28"),
    ("HueB-20-Pool", "c4:29:96:b4:2c:c7", "192.168.20.29"),
    ("HueB-21-Lamps", "c4:29:96:b4:20:0c", "192.168.20.30"),
    ("HueB-22-SWBed", "ec:b5:fa:bb:e6:f3", "192.168.20.31"),
    ("HueB-23-SEBed", "ec:b5:fa:b0:8c:fa", "192.168.20.32"),
    ("HueB-24-2ndGuest", "ec:b5:fa:9d:c0:68", "192.168.20.33"),
    ("HueB-25-Theatre", "c4:29:96:ba:14:84", "192.168.20.34"),
    ("HueB-25-Utility", "ec:b5:fa:bb:cd:32", "192.168.20.35"),
    ("HueB-26-MB2", "c4:29:96:b9:a9:9f", "192.168.20.36"),
    ("HueB-Cabana", "c4:29:96:b4:14:7a", "192.168.20.37"),
    ("HueB-Entrata2", "c4:29:96:b4:23:fd", "192.168.20.38"),
]

ALL_RESERVATIONS = RESERVATIONS_CORE + RESERVATIONS_LIGHTING

# Build expected IP map: mac -> (name, ip)
EXPECTED = {mac.lower(): (name, ip) for name, mac, ip in ALL_RESERVATIONS}


# ============================================================
# UniFi API Client
# ============================================================

class UniFiAPI:
    """Handles UniFi OS authentication and API calls."""

    def __init__(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
        self.token: Optional[str] = None
        self.csrf: Optional[str] = None
        self.base = f"{BASE_URL}/proxy/network/api/s/{SITE}"

    def _request(self, method, url, data=None):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.token:
            headers["Cookie"] = f"TOKEN={self.token}"
        if self.csrf:
            headers["X-Csrf-Token"] = self.csrf

        body = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=body, method=method, headers=headers)

        try:
            resp = urllib.request.urlopen(req, context=self.ctx)
            new_csrf = resp.headers.get("X-Csrf-Token")
            if new_csrf:
                self.csrf = new_csrf
            return resp.status, json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raw = e.read().decode()
            try:
                return e.code, json.loads(raw)
            except json.JSONDecodeError:
                return e.code, {"raw": raw[:500]}

    def login(self):
        """Authenticate with 2FA email flow."""
        url = f"{BASE_URL}/api/auth/login"
        payload = {"username": USERNAME, "password": PASSWORD, "rememberMe": True}

        print(f"Authenticating to {BASE_URL}...")

        # Use cookiejar opener for login
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=self.ctx),
            urllib.request.HTTPCookieProcessor(cj),
        )

        # Step 1: initial login
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        try:
            resp = opener.open(req)
            # No 2FA needed
            for c in cj:
                if c.name == "TOKEN":
                    self.token = c.value
            print("  Login OK (no 2FA)")
            self._refresh_csrf()
            return True
        except urllib.error.HTTPError as e:
            body = json.loads(e.read().decode())
            if e.code != 499:
                print(f"  Login failed: {e.code}")
                return False

        # Step 2: 2FA required
        print("  2FA required. Check your email for the verification code.")
        token_2fa = input("  Enter 2FA code: ").strip()
        payload["token"] = token_2fa

        req2 = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        try:
            resp2 = opener.open(req2)
            for c in cj:
                if c.name == "TOKEN":
                    self.token = c.value
            print("  2FA login OK")
            self._refresh_csrf()
            return True
        except urllib.error.HTTPError as e:
            print(f"  2FA login failed: {e.code}")
            return False

    def _refresh_csrf(self):
        """Fetch CSRF token from an authenticated GET."""
        status, _ = self._request("GET", f"{self.base}/self")
        if status != 200:
            print(f"  Warning: could not refresh CSRF (HTTP {status})")

    def get(self, path):
        return self._request("GET", f"{self.base}{path}")

    def put(self, path, data):
        return self._request("PUT", f"{self.base}{path}", data)

    def post(self, path, data):
        return self._request("POST", f"{self.base}{path}", data)


# ============================================================
# Operations
# ============================================================

def set_reservations(api: UniFiAPI):
    """Create or update all fixed IP reservations."""
    print("\n" + "=" * 60)
    print("SETTING FIXED IP RESERVATIONS")
    print("=" * 60)

    # Fetch all known clients
    status, resp = api.get("/rest/user")
    if status != 200:
        print(f"  ERROR: could not fetch clients ({status})")
        return
    users = resp.get("data", [])
    mac_map = {u.get("mac", "").lower(): u for u in users}
    print(f"  Loaded {len(users)} known clients\n")

    ok = skip = fail = 0
    fails = []

    for name, mac, ip in ALL_RESERVATIONS:
        mac_lower = mac.lower()
        client = mac_map.get(mac_lower)

        if client:
            cid = client["_id"]
            cur_ip = client.get("fixed_ip", "")
            cur_fixed = client.get("use_fixedip", False)
            cur_name = client.get("name", "")

            if cur_fixed and cur_ip == ip and cur_name == name:
                print(f"  [SKIP] {name} ({mac_lower}) -- already {ip}")
                skip += 1
                continue

            payload = {"noted": True, "name": name, "use_fixedip": True, "fixed_ip": ip}
            s, r = api.put(f"/rest/user/{cid}", payload)
            if s == 200:
                change = f"was {cur_ip}" if cur_ip and cur_ip != ip else "new"
                print(f"  [OK]   {name} ({mac_lower}) -> {ip} ({change})")
                ok += 1
            else:
                msg = r.get("meta", {}).get("msg", "") or str(r)[:100]
                print(f"  [FAIL] {name} ({mac_lower}) -> {ip} -- {s}: {msg}")
                fail += 1
                fails.append((name, mac, ip, msg))
        else:
            payload = {"mac": mac_lower, "name": name, "noted": True, "use_fixedip": True, "fixed_ip": ip}
            s, r = api.post("/rest/user", payload)
            if s == 200:
                print(f"  [NEW]  {name} ({mac_lower}) -> {ip}")
                ok += 1
            else:
                msg = r.get("meta", {}).get("msg", "") or str(r)[:100]
                print(f"  [FAIL] {name} ({mac_lower}) -> {ip} -- {s}: {msg}")
                fail += 1
                fails.append((name, mac, ip, msg))

        time.sleep(0.15)

    print(f"\n  Results: {ok} set, {skip} skipped, {fail} failed")
    if fails:
        print(f"  Failed:")
        for n, m, i, e in fails:
            print(f"    {n} ({m}) -> {i}: {e}")


def force_renew(api: UniFiAPI):
    """Force DHCP lease renewal: reduce lease time, reprovision gateway, PoE-cycle."""
    print("\n" + "=" * 60)
    print("FORCING DHCP LEASE RENEWAL")
    print("=" * 60)

    # Step 1: Reduce lease time
    print(f"\n  Step 1: Reducing DHCP lease to {TEMP_LEASE_TIME}s...")
    s1, _ = api.put(f"/rest/networkconf/{CORE_NET_ID}", {"dhcpd_leasetime": TEMP_LEASE_TIME})
    print(f"    Core VLAN: {'OK' if s1 == 200 else f'FAIL ({s1})'}")
    s2, _ = api.put(f"/rest/networkconf/{LIGHTING_NET_ID}", {"dhcpd_leasetime": TEMP_LEASE_TIME})
    print(f"    Lighting VLAN: {'OK' if s2 == 200 else f'FAIL ({s2})'}")

    # Step 2: Force-provision gateway (restarts DHCP, clears lease table)
    print(f"\n  Step 2: Force-provisioning gateway...")
    s3, _ = api.post("/cmd/devmgr", {"cmd": "force-provision", "mac": GW_MAC})
    print(f"    Gateway: {'OK' if s3 == 200 else f'FAIL ({s3})'}")
    print(f"    Waiting 30s for reprovision...")
    time.sleep(30)

    # Step 3: PoE-cycle all PoE-powered devices
    poe_cycle(api)

    # Step 4: Kick all non-PoE clients
    print(f"\n  Step 4: Kicking all clients (clears controller cache)...")
    kicked = 0
    for mac in EXPECTED.keys():
        s, _ = api.post("/cmd/stamgr", {"cmd": "kick-sta", "mac": mac})
        if s == 200:
            kicked += 1
        time.sleep(0.05)
    print(f"    Kicked {kicked}/{len(EXPECTED)}")

    # Step 5: Restore lease time
    print(f"\n  Step 5: Restoring DHCP lease to {NORMAL_LEASE_TIME}s...")
    s4, _ = api.put(f"/rest/networkconf/{CORE_NET_ID}", {"dhcpd_leasetime": NORMAL_LEASE_TIME})
    print(f"    Core VLAN: {'OK' if s4 == 200 else f'FAIL ({s4})'}")
    s5, _ = api.put(f"/rest/networkconf/{LIGHTING_NET_ID}", {"dhcpd_leasetime": NORMAL_LEASE_TIME})
    print(f"    Lighting VLAN: {'OK' if s5 == 200 else f'FAIL ({s5})'}")

    # Step 6: Re-provision with restored settings
    print(f"\n  Step 6: Re-provisioning gateway with restored lease time...")
    s6, _ = api.post("/cmd/devmgr", {"cmd": "force-provision", "mac": GW_MAC})
    print(f"    Gateway: {'OK' if s6 == 200 else f'FAIL ({s6})'}")


def poe_cycle(api: UniFiAPI):
    """PoE power-cycle all PoE-powered devices (touch panels)."""
    print(f"\n  Step 3: PoE-cycling PoE-powered devices...")

    # Get switch port mapping for all clients
    s, resp = api.get("/stat/sta")
    if s != 200:
        print(f"    ERROR: could not fetch clients ({s})")
        return
    clients = resp.get("data", [])

    mac_to_port = {}
    for c in clients:
        mac = c.get("mac", "")
        sw_mac = c.get("sw_mac")
        sw_port = c.get("sw_port")
        if sw_mac and sw_port and c.get("is_wired"):
            mac_to_port[mac] = (sw_mac, sw_port)

    # PoE-cycle each device on its own port (skip uplink ports with 3+ devices)
    port_devices = {}
    for mac, (name, ip) in EXPECTED.items():
        info = mac_to_port.get(mac)
        if info:
            key = info
            if key not in port_devices:
                port_devices[key] = []
            port_devices[key].append(name)

    cycled = 0
    failed = 0
    for (sw_mac, port), names in sorted(port_devices.items()):
        if len(names) > 2:
            # Uplink/trunk port — skip (would affect too many devices)
            continue

        label = ", ".join(names)
        s, r = api.post("/cmd/devmgr", {"cmd": "power-cycle", "mac": sw_mac, "port_idx": port})
        if s == 200 and r.get("meta", {}).get("rc") == "ok":
            print(f"    [OK]   port {port:2d} on {sw_mac[-8:]}: {label}")
            cycled += 1
        elif s == 400:
            # Not a PoE port — expected for non-PoE devices
            pass
        else:
            failed += 1

    print(f"    PoE-cycled {cycled} ports ({failed} non-PoE skipped)")


def ssh_port_bounce(switch_ip: str, ports: str, interval: int = 5):
    """Bounce specific switch ports via SSH using swctrl.

    This works for ALL ports (PoE and non-PoE) on UniFi managed switches.
    Uses 'swctrl port restart' which takes the port down and back up.

    Args:
        switch_ip: IP address of the UniFi switch
        ports: Port spec (e.g., "19-23" or "3" or "1,4,9-12")
        interval: Seconds to keep port down (default 5)
    """
    cmd = [
        "sshpass", "-p", SW_SSH_PASS,
        "ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=5",
        f"{SW_SSH_USER}@{switch_ip}",
        f"swctrl port restart id {ports} interval {interval}",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return r.returncode == 0


def restart_edge_switches(api: UniFiAPI, exclude_core: bool = True):
    """Restart edge switches to force all connected devices to DHCP renew.

    This reboots each switch (~90s recovery), causing all connected devices
    to lose link and do a fresh DHCP request on reconnection.

    Does NOT restart the core switch by default (too disruptive).
    For individual ports on the core switch, use ssh_port_bounce() instead.
    """
    print(f"\n  Restarting edge switches...")

    CORE_SW_MAC = "84:78:48:60:15:b3"

    # Get all switches
    s, resp = api.get("/stat/device")
    if s != 200:
        print(f"    ERROR: could not fetch devices ({s})")
        return

    switches = [d for d in resp.get("data", []) if d.get("type") == "usw"]
    restarted = 0

    for sw in switches:
        sw_mac = sw.get("mac", "")
        sw_name = sw.get("name", sw_mac)

        if exclude_core and sw_mac == CORE_SW_MAC:
            print(f"    [SKIP] {sw_name} (core switch)")
            continue

        s, r = api.post("/cmd/devmgr", {"cmd": "restart", "mac": sw_mac})
        if s == 200:
            print(f"    [OK]   {sw_name} ({sw_mac}) restarting...")
            restarted += 1
        else:
            print(f"    [FAIL] {sw_name}: {s}")

        time.sleep(2)  # small stagger between restarts

    print(f"    Restarted {restarted} switches")
    if restarted > 0:
        print(f"    Waiting 90s for switches to come back...")
        time.sleep(90)


def verify(api: UniFiAPI, wait_secs: int = 0):
    """Verify which devices have their correct reserved IPs."""
    if wait_secs:
        print(f"\n  Waiting {wait_secs}s for devices to settle...")
        time.sleep(wait_secs)

    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)

    correct = []
    wrong = []
    unreachable = []

    for mac, (name, expected_ip) in sorted(EXPECTED.items(), key=lambda x: x[1][0]):
        r = subprocess.run(
            ["ping", "-c", "1", "-W", "1", expected_ip],
            capture_output=True, text=True,
        )
        if "1 packets received" in r.stdout or "1 received" in r.stdout:
            correct.append((name, expected_ip))
        else:
            unreachable.append((name, expected_ip, mac))

    print(f"\n  Reachable at new IP:  {len(correct)}/{len(EXPECTED)}")
    print(f"  Not yet migrated:    {len(unreachable)}")

    if correct:
        print(f"\n  Devices on correct IPs:")
        for name, ip in correct:
            print(f"    {name:25s} {ip}")

    if unreachable:
        print(f"\n  Not yet reachable at new IP (will migrate on next DHCP renewal):")
        # Group by category
        cats = {"TP-": [], "SNS-": [], "HueB-": [], "TV-": [], "ATV-": [], "AVR-": []}
        other = []
        for name, ip, mac in unreachable:
            placed = False
            for prefix in cats:
                if name.startswith(prefix):
                    cats[prefix].append(name)
                    placed = True
                    break
            if not placed:
                other.append(name)

        for prefix, names in cats.items():
            if names:
                label = prefix.rstrip("-")
                print(f"    {label}: {len(names)} ({', '.join(names[:5])}{'...' if len(names) > 5 else ''})")
        if other:
            print(f"    Other: {', '.join(other)}")

    return len(correct), len(unreachable)


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Villa Romanza UniFi DHCP Force Renewal Tool"
    )
    parser.add_argument("--verify", action="store_true", help="Only verify current IPs")
    parser.add_argument("--reserve-only", action="store_true", help="Set reservations without forcing renewal")
    parser.add_argument("--renew-only", action="store_true", help="Force renewal without changing reservations")
    parser.add_argument("--poe-only", action="store_true", help="Only PoE-cycle touch panels")
    parser.add_argument("--restart-switches", action="store_true",
                        help="Restart all edge switches to force DHCP renewal (most reliable)")
    parser.add_argument("--bounce-ports", metavar="SWITCH_IP:PORTS",
                        help="SSH port bounce on a specific switch (e.g., 192.168.1.4:19-23)")
    args = parser.parse_args()

    api = UniFiAPI()
    if not api.login():
        print("\nLogin failed. Exiting.")
        sys.exit(1)

    if args.verify:
        verify(api)
    elif args.reserve_only:
        set_reservations(api)
    elif args.renew_only:
        force_renew(api)
        verify(api, wait_secs=120)
    elif args.poe_only:
        poe_cycle(api)
        verify(api, wait_secs=120)
    elif args.restart_switches:
        restart_edge_switches(api)
        verify(api, wait_secs=30)
    elif args.bounce_ports:
        parts = args.bounce_ports.split(":")
        if len(parts) != 2:
            print("Format: SWITCH_IP:PORTS (e.g., 192.168.1.4:19-23)")
            sys.exit(1)
        sw_ip, ports = parts
        print(f"Bouncing ports {ports} on {sw_ip}...")
        ok = ssh_port_bounce(sw_ip, ports)
        print(f"  {'OK' if ok else 'FAILED'}")
        if ok:
            verify(api, wait_secs=45)
    else:
        # Full run
        set_reservations(api)
        force_renew(api)
        verify(api, wait_secs=120)

    print("\nDone.")


if __name__ == "__main__":
    main()
