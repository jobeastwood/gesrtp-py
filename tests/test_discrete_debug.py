#!/usr/bin/env python3
"""
gesrtp-py - GE-SRTP PLC Driver
Copyright (c) 2025 Jobe Eli Eastwood
Houston, TX

Author: Jobe Eli Eastwood <jobeastwood@hotmail.com>
Project: https://github.com/jobeastwood/gesrtp-py
License: MIT

---

Debug test for discrete memory operations.
Investigates why discrete I/O returns empty payloads.
"""

import logging
from src.driver import GE_SRTP_Driver
from src import protocol

# Configure logging to show detailed debug info
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    plc_ip = "172.16.12.127"
    cpu_slot = 2

    print("="*60)
    print("DEBUG: Discrete Memory Operations")
    print("="*60)

    plc = GE_SRTP_Driver(plc_ip, slot=cpu_slot)
    plc.connect()

    # Test discrete input - bit mode with minimum length 32
    print("\n[TEST 1] Discrete Input (%I) - Bit Mode, count=1, request_length=32")
    try:
        result = plc.read_discrete_input(0, count=1, mode='bit')
        print(f"SUCCESS: {result}")
    except Exception as e:
        print(f"FAILED: {e}")

    # Test discrete input - byte mode with minimum length 4
    print("\n[TEST 2] Discrete Input (%I) - Byte Mode, count=1, request_length=4")
    try:
        result = plc.read_discrete_input(0, count=1, mode='byte')
        print(f"SUCCESS: {result}")
    except Exception as e:
        print(f"FAILED: {e}")

    # Test with larger counts
    print("\n[TEST 3] Discrete Input (%I) - Bit Mode, count=8")
    try:
        result = plc.read_discrete_input(0, count=8, mode='bit')
        print(f"SUCCESS: {result}")
    except Exception as e:
        print(f"FAILED: {e}")

    # Test discrete output
    print("\n[TEST 4] Discrete Output (%Q) - Byte Mode, count=4")
    try:
        result = plc.read_discrete_output(0, count=4, mode='byte')
        print(f"SUCCESS: {result}")
    except Exception as e:
        print(f"FAILED: {e}")

    # Test internal memory
    print("\n[TEST 5] Internal Memory (%M) - Byte Mode, count=4")
    try:
        result = plc.read_discrete_internal(0, count=4, mode='byte')
        print(f"SUCCESS: {result}")
    except Exception as e:
        print(f"FAILED: {e}")

    plc.disconnect()
    print("\n" + "="*60)
    print("Debug test complete")
    print("="*60)


if __name__ == "__main__":
    main()
