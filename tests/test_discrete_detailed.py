#!/usr/bin/env python3
"""
gesrtp-py - GE-SRTP PLC Driver
Copyright (c) 2025 Jobe Eli Eastwood
Houston, TX

Author: Jobe Eli Eastwood <jobeastwood@hotmail.com>
Project: https://github.com/jobeastwood/gesrtp-py
License: MIT

---

Detailed Discrete I/O Testing with Packet Logging

This script tests discrete I/O with verbose packet dumps to help understand
what the PLC is responding with.
"""

import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.driver import GE_SRTP_Driver
from src import protocol

# Configure very detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def hex_dump(data, label=""):
    """Pretty print hex dump of packet data."""
    if label:
        print(f"\n{label}:")
    print("=" * 80)

    # Header
    print("Offset  00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F  ASCII")
    print("-" * 80)

    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_part = ' '.join(f'{b:02X}' for b in chunk)
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print(f"{i:06X}  {hex_part:<48}  {ascii_part}")

    print("=" * 80)


def analyze_response_header(data):
    """Analyze the response packet header."""
    if len(data) < 56:
        print(f"⚠ WARNING: Packet too short! ({len(data)} bytes, expected >= 56)")
        return

    print("\nPacket Analysis:")
    print("-" * 80)
    print(f"Byte 0 (Packet Type):     0x{data[0]:02X} {'(Response)' if data[0] == 0x03 else '(Unknown)'}")
    print(f"Byte 2 (Sequence):        0x{data[2]:02X} ({data[2]})")
    print(f"Byte 4 (Payload Length):  0x{data[4]:02X} ({data[4]} bytes) {'← KEY: EMPTY!' if data[4] == 0 else '← Has data!'}")
    print(f"Byte 30 (Sequence):       0x{data[30]:02X} ({data[30]})")
    print(f"Byte 31 (Message Type):   0x{data[31]:02X}", end='')

    if data[31] == 0xD4:
        print(" (ACK - No Data)")
    elif data[31] == 0x94:
        print(" (ACK - With Data)")
    elif data[31] == 0xD1:
        print(" (ERROR!)")
    else:
        print(" (Unknown)")

    print(f"Bytes 36-39 (Mailbox):    {' '.join(f'0x{data[i]:02X}' for i in range(36, 40))}", end='')
    print(f" {'← Slot 2' if data[36] == 0x20 else '← Wrong slot!'}")

    print(f"Byte 42 (Service Code):   0x{data[42]:02X}")
    print(f"Byte 43 (Segment Sel):    0x{data[43]:02X}")

    offset = data[44] | (data[45] << 8)
    length = data[46] | (data[47] << 8)
    print(f"Bytes 44-45 (Offset):     {offset}")
    print(f"Bytes 46-47 (Length):     {length}")
    print("-" * 80)


def test_discrete_with_packets():
    """Test discrete I/O with full packet dumps."""

    PLC_IP = "172.16.12.127"
    CPU_SLOT = 2

    print("=" * 80)
    print("DETAILED DISCRETE I/O PACKET ANALYSIS")
    print("=" * 80)
    print(f"PLC: {PLC_IP}")
    print(f"CPU Slot: {CPU_SLOT}")
    print()

    plc = GE_SRTP_Driver(PLC_IP, slot=CPU_SLOT)
    plc.connect()
    print("✓ Connected to PLC\n")

    # Test 1: Register read (known working) for comparison
    print("\n" + "="*80)
    print("TEST 1: Register Read (Baseline - Known Working)")
    print("="*80)
    print("Reading %R1 (address 0)...")

    try:
        value = plc.read_register(0)
        print(f"✓ SUCCESS: %R1 = {value}")
    except Exception as e:
        print(f"✗ FAILED: {e}")

    # Test 2: Discrete Input - Byte Mode
    print("\n" + "="*80)
    print("TEST 2: Discrete Input - Byte Mode")
    print("="*80)
    print("Request: Read 4 bytes from %I (address 0)")
    print(f"Segment Selector: 0x10 (DISCRETE_INPUTS_BYTE)")
    print(f"Data Length: 4 bytes (minimum requirement)")

    try:
        result = plc.read_discrete_input(0, count=4, mode='byte')
        print(f"✓ Result: {result}")
        if len(result) == 0:
            print("⚠ WARNING: Empty result (PLC sent no data)")
    except Exception as e:
        print(f"✗ FAILED: {e}")

    # Test 3: Discrete Input - Bit Mode
    print("\n" + "="*80)
    print("TEST 3: Discrete Input - Bit Mode")
    print("="*80)
    print("Request: Read 32 bits from %I (address 0)")
    print(f"Segment Selector: 0x46 (DISCRETE_INPUTS_BIT)")
    print(f"Data Length: 32 bits (minimum requirement)")

    try:
        result = plc.read_discrete_input(0, count=32, mode='bit')
        print(f"✓ Result: {result}")
        if len(result) == 0:
            print("⚠ WARNING: Empty result (PLC sent no data)")
    except Exception as e:
        print(f"✗ FAILED: {e}")

    # Test 4: Discrete Output - Byte Mode
    print("\n" + "="*80)
    print("TEST 4: Discrete Output - Byte Mode")
    print("="*80)
    print("Request: Read 4 bytes from %Q (address 0)")
    print(f"Segment Selector: 0x12 (DISCRETE_OUTPUTS_BYTE)")

    try:
        result = plc.read_discrete_output(0, count=4, mode='byte')
        print(f"✓ Result: {result}")
        if len(result) == 0:
            print("⚠ WARNING: Empty result (PLC sent no data)")
    except Exception as e:
        print(f"✗ FAILED: {e}")

    # Test 5: Internal Memory - Byte Mode
    print("\n" + "="*80)
    print("TEST 5: Internal Memory (%M) - Byte Mode")
    print("="*80)
    print("Request: Read 4 bytes from %M (address 0)")
    print(f"Segment Selector: 0x16 (DISCRETE_INTERNALS_BYTE)")

    try:
        result = plc.read_discrete_internal(0, count=4, mode='byte')
        print(f"✓ Result: {result}")
        if len(result) == 0:
            print("⚠ WARNING: Empty result (PLC sent no data)")
    except Exception as e:
        print(f"✗ FAILED: {e}")

    plc.disconnect()

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("\nKey Observations:")
    print("1. Check debug logs above for packet dumps")
    print("2. Look for 'Byte 4 (Payload Length)' in responses")
    print("3. If Byte 4 = 0, PLC has no data (hardware not configured)")
    print("4. If Byte 31 = 0xD1, segment selector might be wrong")
    print("\nNext Steps:")
    print("1. Use Wireshark to capture packets for deeper analysis")
    print("2. Check PAC Machine Edition for actual I/O configuration")
    print("3. Verify which I/O modules are physically installed")
    print("="*80)


if __name__ == "__main__":
    test_discrete_with_packets()
