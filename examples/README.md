# GE-SRTP Driver Examples

This directory contains example scripts demonstrating how to use the GE-SRTP PLC driver.

## Available Examples

### 1. basic_usage.py
**Simple register reading demonstration**

Shows three methods of using the driver:
- Manual connect/disconnect
- Context manager (recommended)
- Reading analog I/O

**Usage:**
```bash
python3 basic_usage.py
```

**Key Concepts:**
- 0-based addressing (read %R1 using address 0)
- Single vs batch reads
- Context manager auto-disconnect

---

### 2. continuous_monitor.py
**Real-time monitoring of PLC memory**

Monitors registers or analog I/O for changes and displays them with timestamps.

**Usage:**
```bash
python3 continuous_monitor.py
```

**Features:**
- Change detection (only shows when values change)
- Configurable polling interval
- Delta calculation
- Monitor registers or analog I/O
- Custom address ranges

**Use Cases:**
- Debugging PLC logic
- Understanding process behavior
- Verifying PLC programming changes
- Real-time data logging

---

### 3. memory_dump.py
**Forensic memory acquisition**

Performs comprehensive memory dump to JSON file.

**Usage:**
```bash
python3 memory_dump.py
```

**Captures:**
- Register memory (%R1-%R100)
- Analog I/O (%AI, %AQ)
- PLC diagnostics (status, controller info, program names, datetime, faults)
- Metadata (timestamp, PLC IP, slot number)

**Output:**
JSON file named `plc_dump_<IP>_<timestamp>.json`

**Use Cases:**
- Forensic analysis
- PLC backup before changes
- Incident response
- Baseline documentation
- Change tracking

---

## Important Notes

### Addressing

The GE-SRTP protocol uses **0-based addressing**, while PLC programming software uses 1-based:

| PLC Display | Protocol Address | Driver Call |
|-------------|------------------|-------------|
| %R1 | 0 | `plc.read_register(0)` |
| %R2 | 1 | `plc.read_register(1)` |
| %R100 | 99 | `plc.read_register(99)` |
| %AI1 | 0 | `plc.read_analog_input(0)` |

**Formula**: `protocol_address = plc_register_number - 1`

See `../ADDRESSING_SCHEME.md` for detailed explanation.

### CPU Slot Configuration

**CRITICAL**: You must specify the correct CPU slot number!

```python
# If CPU is in slot 1 (default):
plc = GE_SRTP_Driver('192.168.1.100', slot=1)

# If CPU is in slot 2 (like the test PLC):
plc = GE_SRTP_Driver('172.16.12.127', slot=2)
```

Wrong slot number = PLC acknowledges but returns no data!

See `../SLOT_ADDRESSING_FINDINGS.md` for details.

### Hardware Dependencies

**Working on all PLCs:**
- %R (Registers) - Always available in CPU memory
- %M, %T (Internal/Temp Memory) - Always available in CPU memory
- %S, %SA, %SB, %SC (System Memory) - Always available in CPU memory
- PLC diagnostics (status, info, datetime) - Always available

**Requires hardware modules:**
- %AI/%AQ (Analog I/O) - Requires analog I/O modules
- %I/%Q (Discrete I/O) - Requires discrete I/O modules

The test PLC (172.16.12.127) has complete I/O configuration:
- ✅ Analog Input: IC694ALG223 (16 Ch) in Slot 6
- ✅ Analog Output: IC694ALG392 (8 Ch) in Slot 7
- ✅ Discrete Input: IC694MDL240 (16 Ch, 120 VAC) in Slot 8
- ✅ Discrete Output: IC694MDL916 (16 Ch, 24 VDC) in Slot 9

**Result**: ALL memory types working! ✅

See `../HARDWARE_CONFIG.md` for complete hardware configuration.

---

## Modifying Examples

### Change PLC IP Address

Edit the script and modify:
```python
PLC_IP = "172.16.12.127"  # Change to your PLC's IP
CPU_SLOT = 2              # Change to your CPU's slot number
```

### Change Register Range

For `memory_dump.py`, modify the dump range:
```python
# Default: dumps %R1-%R100
dump_data["data"]["registers"] = dump_registers(plc, start=0, end=99)

# To dump %R1-%R1000:
dump_data["data"]["registers"] = dump_registers(plc, start=0, end=999)
```

### Change Monitoring Interval

For `continuous_monitor.py`:
```python
# Default: 0.5 second polling
monitor_registers(plc, start_address=0, count=10, interval=0.5)

# Faster: 0.1 second (10 Hz)
monitor_registers(plc, start_address=0, count=10, interval=0.1)

# Slower: 2 seconds
monitor_registers(plc, start_address=0, count=10, interval=2.0)
```

---

## Security Warnings

⚠️ **IMPORTANT**:
- These scripts are **READ-ONLY** (safe to run)
- No write operations are implemented
- Use on **isolated networks** only
- GE-SRTP has **minimal security** by default
- Unauthorized PLC access may be **illegal**

---

## Troubleshooting

### "Connection refused" or timeout
- Check PLC IP address
- Verify network connectivity: `ping <PLC_IP>`
- Ensure PLC is powered on
- Check firewall rules (port 18245)

### "Empty payload" or "IndexError"
- Verify CPU slot number is correct
- Check if memory type is available on your PLC model
- For discrete I/O, verify hardware modules are installed

### Values seem wrong (off by 1)
- Remember: protocol uses 0-based addressing!
- To read %R1 from PLC, use address 0
- To read %R100 from PLC, use address 99

---

## Further Reading

- `../README.md` - Main driver documentation
- `../ADDRESSING_SCHEME.md` - Addressing explained in detail
- `../SLOT_ADDRESSING_FINDINGS.md` - CPU slot configuration
- `../MULTI_PACKET_DISCOVERY.md` - Protocol internals
- `../SESSION_SUMMARY.md` - Complete development log

---

**Last Updated**: 2025-10-16
**Driver Version**: 1.0.0 (Production Ready)
**Test PLC**: GE RX3i IC695CPE330 (Firmware 10.85) at 172.16.12.127:18245
**Status**: ✅ All example scripts tested and working

