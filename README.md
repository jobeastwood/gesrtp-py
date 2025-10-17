# gesrtp-py

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Status](https://img.shields.io/badge/status-production-brightgreen.svg)

A Python driver for communicating with GE Programmable Logic Controllers using the proprietary GE-SRTP (Service Request Transport Protocol).

## Status: ✅ Production Ready

**Current Version:** 1.0.0

### Implementation Status

#### ✅ Complete and Tested on Real Hardware

All core modules have been implemented, tested, and verified on a live GE RX3i PLC:

- **`protocol.py`** - All service codes, segment selectors, and constants
- **`exceptions.py`** - Complete exception hierarchy
- **`packet.py`** - 56-byte SRTP packet builder and parser
- **`connection.py`** - TCP socket management with multi-packet response handling
- **`driver.py`** - Complete driver with all read operations

#### ✅ All Memory Types Working

- **Register Memory** (`%R`) - Read single or multiple 16-bit registers ✓
- **Analog I/O** (`%AI`, `%AQ`) - Read analog input/output values ✓
- **Discrete I/O** (`%I`, `%Q`) - Read digital inputs/outputs (bit and byte modes) ✓
- **Internal/Temp Memory** (`%M`, `%T`) - Read internal coils and temporary memory ✓
- **System Memory** (`%S`, `%SA`, `%SB`, `%SC`) - Read system status and fault data ✓
- **Global Memory** (`%G`) - Read Genius global data ✓
- **PLC Diagnostics** - Status, controller info, program names, date/time, fault table ✓

**Total**: 9 memory types, 15 access modes - **ALL VERIFIED WORKING** on GE PACSystems hardware

#### ✅ Key Protocol Discoveries

Through systematic testing with real hardware, we discovered and documented:

1. **All-Zeros Initialization** - 56-byte all-zero packet required
2. **Multi-Packet TCP Responses** - PLC sends header and payload separately
3. **CPU Slot Addressing** - Mailbox destination must match CPU slot
4. **0-Based Protocol Addressing** - Protocol uses 0-based, UI uses 1-based
5. **RX3i Minimum Lengths** - Higher minimums than Series 90-30

See `docs/protocol.md` for complete technical details of all discoveries.

#### ✅ Example Scripts Included

- **`basic_usage.py`** - Demonstrates basic driver usage and common operations
- **`continuous_monitor.py`** - Real-time PLC monitoring with change detection
- **`memory_dump.py`** - Forensic memory acquisition to JSON

See `examples/README.md` for detailed documentation.

#### 🔬 Future Enhancements (Optional)

- Symbolic tag addressing (investigation guide: `docs/symbolic_addressing.md`)
- Advanced forensic module with snapshot comparison
- Unit test suite with pytest
- Write operations (not recommended for safety)

## Features

### Safety-First Design
- **READ-ONLY**: Write operations intentionally not implemented for safety
- **Non-invasive**: Designed for forensic memory acquisition
- **Extensive logging**: Debug-level logging throughout for troubleshooting

### Supported PLC Models
- GE Fanuc Series 90-30
- GE Fanuc Series 90-70
- GE RX3i / RX7i
- Most GE PLCs with Ethernet and SRTP support

### Memory Types Supported
| Type | Description | Access Modes |
|------|-------------|--------------|
| %R | Registers (16-bit signed integers) | Word |
| %AI | Analog Inputs | Word |
| %AQ | Analog Outputs | Word |
| %I | Discrete Inputs | Bit, Byte |
| %Q | Discrete Outputs | Bit, Byte |
| %M | Discrete Internals | Bit, Byte |
| %T | Discrete Temporaries | Bit, Byte |
| %S/%SA/%SB/%SC | System Memory | Bit, Byte |
| %G | Genius Global Data | Bit, Byte |

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### ⚠️ Important: 0-Based Addressing

The GE-SRTP protocol uses **0-based addressing**. To read %R1 from your PLC, use address 0:
- **%R1** → `read_register(0)`
- **%R2** → `read_register(1)`
- **%R100** → `read_register(99)`

Formula: **Protocol Address = PLC Register Number - 1**

See `ADDRESSING_SCHEME.md` for detailed explanation.

### Basic Example

```python
from src.driver import GE_SRTP_Driver

# Connect to PLC (specify slot if CPU is not in slot 1)
# Current test PLC: slot=0 at 172.16.12.124
plc = GE_SRTP_Driver('172.16.12.124', slot=0)
plc.connect()

# Read %R1 and %R2 (use addresses 0 and 1)
r1 = plc.read_register(0)   # %R1
r2 = plc.read_register(1)   # %R2
print(f"%R1 = {r1}, %R2 = {r2}")

# Read %R100 (use address 99)
value = plc.read_register(99)
print(f"Register %R100 = {value}")

# Read multiple registers (%R100-%R109 = addresses 99-108)
values = plc.read_register(99, count=10)
print(f"Registers %R100-%R109: {values}")

# Read discrete inputs
input_state = plc.read_discrete_input(1, mode='bit')
print(f"Discrete Input %I1 = {input_state}")

# Get PLC status
status = plc.get_plc_status()
print(f"PLC Status: {status}")

# Disconnect
plc.disconnect()
```

### Context Manager

```python
with GE_SRTP_Driver('172.16.12.124', slot=0) as plc:
    value = plc.read_register(100)
    print(f"%R100 = {value}")
# Automatically disconnects
```

## Protocol Details

### Connection Process
1. TCP connection to port 18245
2. Two-packet initialization handshake
3. Service requests/responses

### Packet Structure
- 56-byte header (little-endian)
- Variable-length payload
- Sequence number tracking
- Error detection via response codes

### Service Codes
- `0x00` - PLC Short Status
- `0x03` - Return Program Names
- `0x04` - Read System Memory
- `0x43` - Controller Type/ID
- And more... (see `src/protocol.py`)

## Development

### Project Structure
```
plc_project/
├── src/                    # Source code
│   ├── protocol.py         # Protocol constants
│   ├── exceptions.py       # Custom exceptions
│   ├── packet.py           # Packet builder/parser
│   ├── connection.py       # TCP connection management
│   ├── driver.py           # Main driver class
│   └── forensic.py         # (TODO) Forensic features
├── tests/                  # Unit tests
├── examples/               # Example scripts
├── docs/                   # Documentation
├── reference/              # Reference materials
├── logs/                   # Runtime logs
├── requirements.txt        # Dependencies
└── README.md              # This file
```

### Running Tests

```bash
# Basic connection test
python3 test_connection.py

# Unit tests (TODO)
pytest tests/ -v

# With coverage (TODO)
pytest --cov=src tests/
```

## Quick Start

### Installation

```bash
# Clone or download this repository
cd plc_project

# No external dependencies required - uses Python standard library only!
python3 examples/basic_usage.py
```

### Your First Read

```python
from src.driver import GE_SRTP_Driver

# Connect to PLC (specify slot if CPU not in slot 1)
with GE_SRTP_Driver('172.16.12.124', slot=0) as plc:
    # Read %R1 (remember: 0-based addressing!)
    value = plc.read_register(0)
    print(f"%R1 = {value}")
```

That's it! No dependencies, no configuration files, just pure Python.

## Documentation

### Core Documentation
- **`README.md`** (this file) - Overview and quick start
- **`docs/overview.md`** - Complete project summary, status, and development journey
- **`docs/protocol.md`** - All 5 major protocol discoveries with technical details

### Hardware & Configuration
- **`docs/hardware.md`** - Complete RX3i hardware configuration

### Future Enhancements
- **`docs/symbolic_addressing.md`** - How to add symbolic tag support
- **`docs/wireshark.md`** - Protocol analysis and debugging

### Development Resources
- **`development.md`** - Developer guide and project insights
- **`docs/todo.md`** - Task tracking

## Security Warnings

⚠️ **CRITICAL SECURITY INFORMATION:**

- This protocol has **MINIMAL SECURITY** by default
- Most PLCs have **NO AUTHENTICATION** in default configuration
- Use ONLY on **ISOLATED NETWORKS**
- Read operations are generally safe
- **NEVER** implement write operations without comprehensive safety features
- Write operations can cause:
  - Equipment damage ($$$ to $$$$$ repairs)
  - Worker injury or death
  - Process shutdowns
  - Environmental incidents

## Reference Materials

- **Academic Paper**: "Leveraging the SRTP protocol for over-the-network memory acquisition of a GE Fanuc Series 90-30" (DFRWS 2017)
- **Reference Implementation**: https://github.com/TheMadHatt3r/ge-ethernet-SRTP
- **C++ Implementation**: https://github.com/kkuba91/uGESRTP
- **Wireshark Dissector**: https://github.com/Palatis/packet-ge-srtp

## Technical Specifications

- **Protocol**: GE-SRTP (Service Request Transport Protocol)
- **Transport**: TCP/IP
- **Default Port**: 18245
- **Byte Order**: Little-endian
- **Packet Size**: 56-byte header + variable payload
- **Max Register Read**: 125 words per request

## License

MIT License - See LICENSE file for details

## Contributing

This is a defensive security / forensic tool. Contributions should focus on:
- Read operations only
- Error handling improvements
- Documentation
- Test coverage
- Safety features

## Disclaimer

This software is provided for educational, research, and defensive security purposes only. Users are responsible for compliance with all applicable laws and regulations. The authors assume no liability for misuse or damages caused by this software.

---

**Last Updated**: 2025-10-17
**Status**: Production Ready - All Features Working ✅
**Current Test PLC**: GE PACSystems EPXCPE210 (Firmware 10.30) at 172.16.12.124:18245 (slot 0)
**Previously Tested**: GE RX3i IC695CPE330 (Firmware 10.85) at 172.16.12.127:18245 (slot 2)
**Documentation**: See `docs/overview.md` for complete project details
