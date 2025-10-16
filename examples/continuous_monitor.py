#!/usr/bin/env python3
"""
gesrtp-py - GE-SRTP PLC Driver
Copyright (c) 2025 Jobe Eli Eastwood
Houston, TX

Author: Jobe Eli Eastwood <jobeastwood@hotmail.com>
Project: https://github.com/jobeastwood/gesrtp-py
License: MIT

---

Continuous PLC Monitoring Example

Monitors PLC registers and analog I/O for changes and displays them in real-time.
Useful for debugging and understanding PLC behavior.
"""

import sys
import os
import time
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.driver import GE_SRTP_Driver


def monitor_registers(plc, start_address, count, interval=1.0):
    """
    Monitor registers for changes.

    Args:
        plc: Connected GE_SRTP_Driver instance
        start_address: Starting register address
        count: Number of registers to monitor
        interval: Polling interval in seconds
    """
    print(f"\nMonitoring %R{start_address+1}-%R{start_address+count} (addresses {start_address}-{start_address+count-1})")
    print(f"Polling interval: {interval}s")
    print("Press Ctrl+C to stop")
    print("-" * 80)

    # Store previous values
    previous_values = None

    try:
        iteration = 0
        while True:
            iteration += 1

            # Read current values
            current_values = plc.read_register(start_address, count=count)

            # Check for changes
            if previous_values is None:
                # First read - just display
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                print(f"[{timestamp}] Initial values:")
                for i, value in enumerate(current_values):
                    reg_num = start_address + i + 1  # Convert to 1-based for display
                    addr = start_address + i
                    print(f"  %R{reg_num:3d} (addr {addr:3d}) = {value:6d}")
            else:
                # Check for changes
                changes = []
                for i, (prev, curr) in enumerate(zip(previous_values, current_values)):
                    if prev != curr:
                        reg_num = start_address + i + 1
                        addr = start_address + i
                        changes.append((reg_num, addr, prev, curr))

                if changes:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    print(f"\n[{timestamp}] Changes detected:")
                    for reg_num, addr, prev, curr in changes:
                        delta = curr - prev
                        print(f"  %R{reg_num:3d} (addr {addr:3d}): {prev:6d} → {curr:6d} (Δ {delta:+d})")

            previous_values = current_values

            # Wait before next poll
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user")
        print(f"Total iterations: {iteration}")


def monitor_analog_io(plc, count=5, interval=1.0):
    """
    Monitor analog I/O for changes.

    Args:
        plc: Connected GE_SRTP_Driver instance
        count: Number of analog inputs/outputs to monitor
        interval: Polling interval in seconds
    """
    print(f"\nMonitoring %AI1-%AI{count} and %AQ1-%AQ{count} (addresses 0-{count-1})")
    print(f"Polling interval: {interval}s")
    print("Press Ctrl+C to stop")
    print("-" * 80)

    previous_ai = None
    previous_aq = None

    try:
        iteration = 0
        while True:
            iteration += 1

            # Read current values
            current_ai = plc.read_analog_input(0, count=count)
            current_aq = plc.read_analog_output(0, count=count)

            # Check for changes
            if previous_ai is None:
                # First read
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                print(f"[{timestamp}] Initial values:")
                print("  Analog Inputs:")
                for i, value in enumerate(current_ai):
                    print(f"    %AI{i+1:2d} (addr {i}) = {value:6d}")
                print("  Analog Outputs:")
                for i, value in enumerate(current_aq):
                    print(f"    %AQ{i+1:2d} (addr {i}) = {value:6d}")
            else:
                # Check for changes
                ai_changes = []
                aq_changes = []

                for i, (prev, curr) in enumerate(zip(previous_ai, current_ai)):
                    if prev != curr:
                        ai_changes.append((i, prev, curr))

                for i, (prev, curr) in enumerate(zip(previous_aq, current_aq)):
                    if prev != curr:
                        aq_changes.append((i, prev, curr))

                if ai_changes or aq_changes:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    print(f"\n[{timestamp}] Changes detected:")

                    if ai_changes:
                        print("  Analog Inputs:")
                        for addr, prev, curr in ai_changes:
                            delta = curr - prev
                            print(f"    %AI{addr+1:2d} (addr {addr}): {prev:6d} → {curr:6d} (Δ {delta:+d})")

                    if aq_changes:
                        print("  Analog Outputs:")
                        for addr, prev, curr in aq_changes:
                            delta = curr - prev
                            print(f"    %AQ{addr+1:2d} (addr {addr}): {prev:6d} → {curr:6d} (Δ {delta:+d})")

            previous_ai = current_ai
            previous_aq = current_aq

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user")
        print(f"Total iterations: {iteration}")


def main():
    PLC_IP = "172.16.12.127"
    CPU_SLOT = 2

    print("="*80)
    print("GE-SRTP Driver - Continuous Monitoring Example")
    print("="*80)
    print(f"PLC: {PLC_IP}")
    print(f"CPU Slot: {CPU_SLOT}")
    print()

    # Connect to PLC
    plc = GE_SRTP_Driver(PLC_IP, slot=CPU_SLOT)
    plc.connect()
    print("✓ Connected to PLC")

    # Choose what to monitor
    print("\nMonitoring options:")
    print("  1. Monitor registers %R1-%R10")
    print("  2. Monitor analog I/O (%AI1-%AI5 and %AQ1-%AQ5)")
    print("  3. Monitor custom register range")

    choice = input("\nSelect option (1-3): ").strip()

    try:
        if choice == '1':
            monitor_registers(plc, start_address=0, count=10, interval=0.5)

        elif choice == '2':
            monitor_analog_io(plc, count=5, interval=0.5)

        elif choice == '3':
            start = int(input("Enter starting register number (1-based, e.g., 100 for %R100): "))
            count = int(input("Enter number of registers to monitor: "))
            interval = float(input("Enter polling interval in seconds (e.g., 0.5): "))

            # Convert from 1-based to 0-based addressing
            start_address = start - 1

            monitor_registers(plc, start_address=start_address, count=count, interval=interval)

        else:
            print("Invalid choice")

    finally:
        plc.disconnect()
        print("\n✓ Disconnected from PLC")
        print("\n" + "="*80)
        print("Monitoring complete!")
        print("="*80)


if __name__ == "__main__":
    main()
