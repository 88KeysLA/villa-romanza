"""Shared fixtures for unifi-tools tests."""

import sys
import os

# Ensure dhcp_force_renew is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
