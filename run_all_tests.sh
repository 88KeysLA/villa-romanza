#!/bin/bash
# Villa Romanza — Master Test Runner
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

cd "$(dirname "$0")"

echo -e "${BOLD}========================================${NC}"
echo -e "${BOLD}  VILLA ROMANZA TEST SUITE${NC}"
echo -e "${BOLD}========================================${NC}"
echo ""

# Defaults
RUN_UNIT=true
RUN_SYSTEM=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --unit-only) RUN_UNIT=true; RUN_SYSTEM=false; shift ;;
        --system-only) RUN_UNIT=false; RUN_SYSTEM=true; shift ;;
        --all) RUN_UNIT=true; RUN_SYSTEM=true; shift ;;
        *) echo "Usage: $0 [--unit-only|--system-only|--all]"; exit 1 ;;
    esac
done

OVERALL=0

# --- Unit Tests ---
if [ "$RUN_UNIT" = true ]; then
    echo -e "${BLUE}[1] Unit Tests (no network)${NC}"
    echo -e "${BLUE}────────────────────────────────────────${NC}"
    if PYTHONPATH=sonos-mcp/src pytest -v -m unit 2>&1; then
        echo -e "${GREEN}Unit tests passed${NC}"
    else
        echo -e "${RED}Unit tests failed${NC}"
        OVERALL=1
    fi
    echo ""
fi

# --- System Health Tests ---
if [ "$RUN_SYSTEM" = true ]; then
    echo -e "${BLUE}[2] System Health Tests (network)${NC}"
    echo -e "${BLUE}────────────────────────────────────────${NC}"
    if [ -z "$HA_TOKEN" ]; then
        echo -e "${YELLOW}HA_TOKEN not set — skipping HA tests${NC}"
        echo -e "${YELLOW}Set with: export HA_TOKEN='your-token'${NC}"
        echo ""
        # Still run non-HA system tests
        if PYTHONPATH=sonos-mcp/src pytest tests/test_system_health.py -v -m "network and not ha" 2>&1; then
            echo -e "${GREEN}Network tests passed${NC}"
        else
            echo -e "${YELLOW}Some network tests failed${NC}"
            OVERALL=1
        fi
    else
        if PYTHONPATH=sonos-mcp/src pytest tests/test_system_health.py -v 2>&1; then
            echo -e "${GREEN}System health tests passed${NC}"
        else
            echo -e "${YELLOW}Some system health tests failed${NC}"
            OVERALL=1
        fi
    fi
    echo ""
fi

# --- Summary ---
echo -e "${BOLD}========================================${NC}"
if [ $OVERALL -eq 0 ]; then
    echo -e "${GREEN}${BOLD}All tests passed${NC}"
else
    echo -e "${YELLOW}${BOLD}Some tests failed — review output above${NC}"
fi
echo -e "${BOLD}========================================${NC}"
exit $OVERALL
