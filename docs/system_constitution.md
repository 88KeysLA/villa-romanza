# Villa Romanza: Agentic Performance & Environment System
# Canonical Documentation Set (v1.1)
# Source: /Users/mattserletic/Downloads/System Constitution for Villa Romanza V 1.1.docx

Operational Mandate: Order matters. Each document builds authority and context for the next. These documents are stable; future changes append rather than rewrite history. AI systems must read in order, treat earlier documents as constraints, and never violate stated authority boundaries.

## 01 — Objectives & Opportunities
### 1.1 Purpose
Villa Romanza is a living performance environment where sound, light, visuals, and architecture collaborate to shape emotional experience. It explores music as a spatial force, light as a performative medium, and intelligence as a collaborator rather than a controller.

### 1.2 Core Objectives
- **Emotional Coherence**: Environments must feel "inevitable"—belonging to the music and the moment.
- **Deterministic Beauty**: Every state and transition must be bounded, reversible, and pre-authored.
- **Human-Centered Intelligence**: AI may observe, reason, and propose, but must never override human intent, safety, or architectural calm.

## 02 — System Architecture Overview
### 2.1 Execution Nodes

| Node | Role | Primary Constraints |
|---|---|---|
| Mech Mac mini | Local Executive Agent (LEA), GenAI Foundry, reasoning | No real-time loops; no direct hardware control |
| FX Mac mini | Live audio capture, feature extraction, NDI motion layers | No AV authority; no mode decisions |
| Show Mac mini | TouchDesigner compositing and HDMI program out | No reasoning; no autonomy; deterministic only |
| Crestron CP4-R | Mode authority, AV routing, safety overrides | Cannot be bypassed or overridden by AI |
| VRROOM | Timing and EDID authority, 4K120/4K60 distribution | Sole timing authority; no intelligence |

## 03 — Signal Authority Matrix

| Domain | Primary Authority | Secondary | Advisory |
|---|---|---|---|
| Physical Safety | Crestron CP4-R | Home Assistant | AI Agents |
| Mode Selection | Crestron CP4-R | Home Assistant | AI Agents |
| Visual Program Out | Show Mac (TD) | None | AI Agents |
| Intelligence | Mech Mac (LEA) | None | Claude / LLMs |
| Lighting Execution | Hue / HA | Crestron | AI Agents |

## 04 — Mode Taxonomy & Experience States
- **NORMAL**: Architectural living; no performative intent.
- **LISTEN**: Focused high-fidelity recorded music listening.
- **WATCH**: Narrative consumption (Film, TV, Sports). Sacrosanct mode.
- **ENTERTAIN**: Social, energetic playback-first hosting.
- **LIVE_JAM / SHOW**: Musician-led creation or authored performance.
- **INTERLUDE**: Intentional pause between expressive modes.

## 05 — Hue Sync Role Architecture
- **SYNC_PRIMARY_SHOW**: Attention-leading, high responsiveness, theatrical.
- **SYNC_AMBIENT_MUSIC**: Spatial breathing, perimeter energy, lower contrast.
- **SYNC_STATIC_ARCH**: Architectural continuity; never synced; the visual "floor".

## 06 — Audio, Visual, and Telemetry Flows
- **Audio Playback**: Sonos/Anthem → Crestron → Speakers.
- **Live Sensing**: Mics → MixPre → FX Mac (USB). Never routed to speakers.
- **Visual Program**: FX (NDI) + GenAI Packs → Show Mac (Compositing) → VRROOM → LG OLED.

## 07 — Show System (TouchDesigner) Design
The Show System is a disciplined visual instrument. It executes API requests (Activate Look, Set Bias) but does not reason. It is the sole analyzer for Hue Sync visuals.

## 08 — FX System (Audio → Motion Engine)
FX translates sound into motion and texture (NDI layers). It maps audio features (RMS, BPM, Spectral) to vector fields. It has no knowledge of "house modes."

## 09 — GenAI Visual Foundry
Generative visuals created offline and promoted to assets.
- **Thematic Packs**: The atomic unit of deployment.
- **Manifest.json**: Mandatory metadata defining "vibe," BPM compatibility, and layer priority.

## 10 — Agentic Control Model
- **LEA (Local Executive Agent)**: The single executive intelligence on the Mech Mac.
- **Sub-Agents**: Specialist voices (ADJ, Visual Taste) that propose changes to the LEA.

## 10A — Agentic Disc Jockey (ADJ)
(Sub-agent of LEA for music-driven environment decisions)

## 11 — Crestron & Home Assistant Integration
The Execution Contract:
- **Agent (Mech)**: Sends an intent via REST API.
- **Home Assistant**: Validates intent against the Safety Allowlist.
- **Crestron**: Receives the command (via XSig or TCP) and executes the physical change.

## 11B — Technical Integration Schema (For Claude Code)

### B.1 Entity Naming Convention
All entities exposed to AI agents must follow the prefix: `agent_controlled_[domain]_[name]`.
Example: `switch.agent_controlled_lighting_enable`.

### B.2 Safety Allowlist (Domain Gatekeeping)
Claude Code is restricted to interacting with only these domains:
- `light.*` (Excluding Master Bedroom and Security lighting)
- `media_player.*` (Transport control only; no volume over 70%)
- `input_select.villa_mode` (The primary bridge to Crestron)
- `sensor.*` (Telemetry only)

### B.3 The Action Vocabulary
The following commands are the only valid outputs from an Agent:
- `set_vr_mode(MODE_NAME)`
- `adjust_visual_bias(FLOAT 0.0-1.0)`
- `trigger_visual_stinger(STINGER_ID)`
- `set_lighting_intensity(FLOAT 0.0-1.0)`
- `load_thematic_pack(PACK_ID)`

## 12 — Operator Interfaces
- **Physical (Crestron)**: Supreme Authority.
- **Azmisi**: Creative Conductor's Baton.
- **Voice**: Natural language intent.

## 13 — Autonomy Phases
- **Phase 1 (Manual)**: AI observes and suggests via UI.
- **Phase 2 (Assisted)**: AI executes with a human "Confirm" button.
- **Phase 3 (Bounded)**: AI executes within pre-set "Safe Windows" (e.g., 6 PM - 10 PM).
- **Phase 4 (Expressive)**: Full agentic flow during LIVE_JAM modes.

## 14 — Logging, Learning, and Evaluation
Villa Romanza learns with people. Taste models are Participant-Scoped, local, and can be reset at any time by the user.

## 15 — Recovery & Fallback Runbooks

| Failure | System Response |
|---|---|
| FX Offline | Show Mac switches to "Static Ambient" loops |
| Mech Offline | HA disables agent_controlled switches; house stays in current mode |
| Show Offline | Crestron triggers "Emergency Architectural" lighting (Warm White) |
| Network Lag | Command buffer cleared; no "catch-up" execution allowed |
