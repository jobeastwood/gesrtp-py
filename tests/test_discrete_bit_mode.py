#!/usr/bin/env python3
"""
gesrtp-py - GE-SRTP PLC Driver
Copyright (c) 2025 Jobe Eli Eastwood
Houston, TX

Author: Jobe Eli Eastwood <jobeastwood@hotmail.com>
Project: https://github.com/jobeastwood/gesrtp-py
License: MIT

---

Debug bit mode discrete I/O reading.
Byte mode works, but bit mode returns empty. Let's find out why.
"""

import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.driver import GE_SRTP_Driver

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)


def main():
    PLC_IP = "172.16.12.127"
    CPU_SLOT = 2

    print("="*80)
    print("BIT MODE DEBUGGING")
    print("="*80)

    plc = GE_SRTP_Driver(PLC_IP, slot=CPU_SLOT)
    plc.connect()

    # Test different bit counts to see what works
    test_cases = [
        (1, "Single bit - below minimum"),
        (8, "8 bits - 1 byte worth"),
        (16, "16 bits - 2 bytes worth"),
        (32, "32 bits - minimum we set"),
        (64, "64 bits - 8 bytes worth"),
        (128, "128 bits - 16 bytes worth"),
    ]

    for count, description in test_cases:
        print(f"\n[TEST] Reading {count} bits - {description}")
        print("-" * 80)
        try:
            result = plc.read_discrete_input(0, count=count, mode='bit')
            if result:
                print(f"  ✓ SUCCESS! Got {len(result)} bits")
                if len(result) <= 32:
                    # Show bit pattern for small results
                    bit_string = ''.join('1' if b else '0' for b in result)
                    print(f"  Bit pattern: {bit_string}")
                    # Show as hex bytes
                    if len(result) >= 8:
                        byte_val = sum(result[i] << i for i in range(min(8, len(result))))
                        print(f"  As byte: 0x{byte_val:02X}")
            else:
                print(f"  ✗ Empty result (length={len(result)})")
        except Exception as e:
            print(f"  ✗ ERROR: {e}")

    plc.disconnect()

    print("\n" + "="*80)
    print("If all bit mode tests failed:")
    print("  → Bit mode may not be supported on this PLC/firmware")
    print("  → OR bit mode requires different segment selector")
    print("  → Use byte mode instead - it's working perfectly!")
    print("="*80)


if __name__ == "__main__":
    main()
