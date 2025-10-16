#!/usr/bin/env python3
"""
gesrtp-py - GE-SRTP PLC Driver
Copyright (c) 2025 Jobe Eli Eastwood
Houston, TX

Author: Jobe Eli Eastwood <jobeastwood@hotmail.com>
Project: https://github.com/jobeastwood/gesrtp-py
License: MIT

---

Test discrete I/O with correct addressing based on PAC Machine Edition configuration.

From PAC Machine Edition:
- %I00001–%I00016 (Discrete Inputs from IC694MDL240)
- %Q00001–%Q00016 (Discrete Outputs from IC694MDL916)

Protocol addressing: GE-SRTP uses 0-based, so:
- %I00001 in PAC ME → address 0 in protocol? OR address 1?
- Need to test both!
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.driver import GE_SRTP_Driver


def main():
    PLC_IP = "172.16.12.127"
    CPU_SLOT = 2

    print("="*80)
    print("TESTING DISCRETE I/O WITH CORRECT ADDRESSING")
    print("="*80)
    print(f"PLC: {PLC_IP}")
    print(f"CPU Slot: {CPU_SLOT}")
    print()
    print("Based on PAC Machine Edition config:")
    print("  Discrete Inputs:  %I00001-%I00016 (IC694MDL240, Slot 8)")
    print("  Discrete Outputs: %Q00001-%Q00016 (IC694MDL916, Slot 9)")
    print("="*80)

    plc = GE_SRTP_Driver(PLC_IP, slot=CPU_SLOT)
    plc.connect()
    print("✓ Connected to PLC\n")

    # Test 1: Try address 0 (which might map to %I00001 in 0-based protocol)
    print("[TEST 1] Discrete Input - Address 0 (might be %I00001)")
    print("-" * 80)
    try:
        result = plc.read_discrete_input(0, count=8, mode='byte')
        print(f"  Address 0, byte mode: {result}")
        if result:
            print(f"  SUCCESS! Got data: {[f'0x{b:02X}' for b in result] if isinstance(result, list) else f'0x{result:02X}'}")
        else:
            print("  Empty result")
    except Exception as e:
        print(f"  ERROR: {e}")

    # Test 2: Try address 1 (in case discrete I/O has offset)
    print("\n[TEST 2] Discrete Input - Address 1")
    print("-" * 80)
    try:
        result = plc.read_discrete_input(1, count=8, mode='byte')
        print(f"  Address 1, byte mode: {result}")
        if result:
            print(f"  SUCCESS! Got data: {[f'0x{b:02X}' for b in result] if isinstance(result, list) else f'0x{result:02X}'}")
        else:
            print("  Empty result")
    except Exception as e:
        print(f"  ERROR: {e}")

    # Test 3: Try bit mode at address 0
    print("\n[TEST 3] Discrete Input - Address 0, Bit Mode")
    print("-" * 80)
    try:
        result = plc.read_discrete_input(0, count=16, mode='bit')
        print(f"  Address 0, 16 bits: {result}")
        if result:
            print(f"  SUCCESS! Got {len(result)} bits")
            # Show bit pattern
            bit_string = ''.join('1' if b else '0' for b in result)
            print(f"  Bit pattern: {bit_string}")
        else:
            print("  Empty result")
    except Exception as e:
        print(f"  ERROR: {e}")

    # Test 4: Try bit mode at address 1
    print("\n[TEST 4] Discrete Input - Address 1, Bit Mode")
    print("-" * 80)
    try:
        result = plc.read_discrete_input(1, count=16, mode='bit')
        print(f"  Address 1, 16 bits: {result}")
        if result:
            print(f"  SUCCESS! Got {len(result)} bits")
            bit_string = ''.join('1' if b else '0' for b in result)
            print(f"  Bit pattern: {bit_string}")
        else:
            print("  Empty result")
    except Exception as e:
        print(f"  ERROR: {e}")

    # Test 5: Discrete Outputs
    print("\n[TEST 5] Discrete Output - Address 0, Byte Mode")
    print("-" * 80)
    try:
        result = plc.read_discrete_output(0, count=8, mode='byte')
        print(f"  Address 0, byte mode: {result}")
        if result:
            print(f"  SUCCESS! Got data: {[f'0x{b:02X}' for b in result] if isinstance(result, list) else f'0x{result:02X}'}")
        else:
            print("  Empty result")
    except Exception as e:
        print(f"  ERROR: {e}")

    # Test 6: Internal memory %M
    print("\n[TEST 6] Internal Memory (%M) - Address 0 and 1")
    print("-" * 80)
    for addr in [0, 1]:
        try:
            result = plc.read_discrete_internal(addr, count=8, mode='byte')
            print(f"  Address {addr}, byte mode: {result}")
            if result:
                print(f"    SUCCESS! Got data: {[f'0x{b:02X}' for b in result] if isinstance(result, list) else f'0x{result:02X}'}")
        except Exception as e:
            print(f"    Address {addr} ERROR: {e}")

    # Test 7: Try a range of addresses to find where data starts
    print("\n[TEST 7] Scanning Addresses 0-10 for Discrete Inputs (Byte Mode)")
    print("-" * 80)
    for addr in range(11):
        try:
            result = plc.read_discrete_input(addr, count=1, mode='byte')
            if result and result != 0:
                print(f"  Address {addr:2d}: 0x{result:02X} ← DATA FOUND!")
            elif result == 0:
                print(f"  Address {addr:2d}: 0x00 (zero)")
            else:
                print(f"  Address {addr:2d}: Empty")
        except:
            print(f"  Address {addr:2d}: Error")

    plc.disconnect()

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("\nIf all tests returned empty:")
    print("  → Discrete I/O may need different base address or segment selector")
    print("  → Or addressing scheme is different for IC694 modules in RX3i")
    print("\nIf some tests worked:")
    print("  → We found the correct address offset!")
    print("  → Update driver to use correct base addresses")
    print("="*80)


if __name__ == "__main__":
    main()
