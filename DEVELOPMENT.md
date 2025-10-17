# gesrtp-py - Developer Guide

**Project Status**: ✅ **PRODUCTION READY - ALL FEATURES WORKING**
**Version**: 1.1.0
**Last Updated**: 2025-10-17

---

## Project Overview

A **complete, production-ready** Python driver for GE Programmable Logic Controllers using the proprietary GE-SRTP (Service Request Transport Protocol). This driver enables direct network-based communication with GE RX3i PLCs for forensic memory acquisition and industrial automation purposes.

### Current Status

🎉 **PROJECT COMPLETE!** All intended features have been implemented, tested, and verified on real hardware.

- **Code**: 2,500+ lines of production Python
- **Memory Types**: 9 types with 15 access modes - **ALL WORKING**
- **Hardware Tested**: GE PACSystems EPXCPE210 (Firmware 10.30) and IC695CPE330 (Firmware 10.85)
- **Documentation**: Comprehensive (10 markdown files including CHANGELOG.md)
- **Test Scripts**: 3 organized tests with comprehensive documentation
- **Example Scripts**: 3 professional examples with numbered naming + README
- **Version Control**: Semantic versioning with detailed changelog

---

## Quick Start for Developers

### For New Contributors

1. **Read docs/overview.md** - Complete project summary and achievements
2. **Read docs/protocol.md** - 5 critical protocol findings
3. **Read docs/todo.md** - See what's complete and what's optional for future
4. **Study examples/** - Working code demonstrating all features

### For Maintenance/Enhancement

The driver is **feature-complete**. Future work is **optional enhancement** only:
- Unit testing infrastructure (pytest)
- Advanced forensic module
- Symbolic tag addressing support
- Code quality improvements

See `docs/todo.md` "Optional Future Enhancements" section for details.

---

## Project Context

### Protocol Background
- **Protocol**: GE-SRTP (Service Request Transport Protocol)
- **Developer**: General Electric (GE Intelligent Platforms)
- **Purpose**: Data exchange between GE PLCs and computer-based clients
- **Transport**: TCP/IP over Ethernet, port 18245
- **Status**: Proprietary, no official public documentation
- **Key Characteristic**: Little-endian byte ordering

### Target Hardware
- **PLC Model**: GE PACSystems EPXCPE210
- **CPU Location**: Rack 0, Slot 0 (critical for mailbox addressing!)
- **Firmware**: 10.30 [EJTT]
- **IP Address**: 172.16.12.124
- **Port**: 18245 (default GE-SRTP port)
- **Program Status**: NO PROGRAM LOADED (clean slate for testing)
- **Network**: Isolated industrial network

**Full hardware details**: See `docs/hardware.md`

### Security Warning
⚠️ **CRITICAL**: This protocol has minimal security by default. PLCs in default configuration have NO AUTHENTICATION. Write operations (NOT implemented in this driver) can cause physical damage to equipment or endanger workers.

**This driver is READ-ONLY by design for safety.**

---

## Project Structure

```
gesrtp-py/
├── README.md                          # Main user guide
├── DEVELOPMENT.md                     # This file - developer guide
├── CHANGELOG.md                       # Version history and changes (NEW v1.1.0)
├── VERSION                            # Current version number (NEW v1.1.0)
├── requirements.txt                   # Python dependencies (none - pure Python!)
│
├── docs/                              # Documentation directory (NEW v1.1.0)
│   ├── overview.md                    # Complete project summary
│   ├── protocol.md                    # 5 major technical discoveries
│   ├── hardware.md                    # Hardware configuration details
│   ├── wireshark.md                   # Wireshark capture guide
│   ├── symbolic_addressing.md         # Symbolic addressing investigation
│   └── todo.md                        # Project status and task tracking
│
├── src/                               # Source code (1,720 lines)
│   ├── __init__.py                    # Package initialization (version 1.1.0)
│   ├── protocol.py                    # Protocol constants (service codes, selectors)
│   ├── exceptions.py                  # Custom exception hierarchy
│   ├── packet.py                      # 56-byte packet builder/parser
│   ├── connection.py                  # TCP socket with multi-packet handling
│   └── driver.py                      # Main driver with all read operations
│
├── tests/                             # Professional test suite (v1.1.0)
│   ├── README.md                      # Complete test documentation (NEW)
│   ├── 01_connection_basic.py         # Basic connectivity test (renamed)
│   ├── 02_memory_all_types.py         # All memory types test (renamed)
│   └── 03_memory_comprehensive_0_64.py # Comprehensive 0-64 test (NEW)
│
├── examples/                          # Professional examples (v1.1.0)
│   ├── README.md                      # Improved example documentation
│   ├── 01_basic_usage.py              # Beginner: Simple reads (renamed)
│   ├── 02_realtime_monitor.py         # Intermediate: Live monitoring (rewritten!)
│   └── 03_forensic_dump.py            # Advanced: Memory dump (renamed)
│
├── reference/                         # Reference materials
│   ├── Leveraging_the_SRTP_protocol_for_over-the-network_.pdf
│   └── FST_DFS_GE_SRTP.pdf
│
└── logs/                              # Runtime logs (created automatically)
```

### What's New in v1.1.0

**Major Improvements:**
- 🔥 **Completely rewritten real-time monitor** with in-place updates (no scrolling!)
- ✅ **New comprehensive test** for addresses 0-64 across all memory types
- 📚 **Professional test documentation** (tests/README.md)
- 📝 **CHANGELOG.md** following industry standard
- 🔢 **Numbered file organization** for tests and examples (01_, 02_, 03_)
- ⭐ **Difficulty ratings** for examples (beginner to advanced)
- 🎯 **Improved organization** and user experience

**All tests passed on new EPXCPE210 hardware!**

---

## Completed Implementation

### Core Modules ✅

All 5 core modules are complete and production-ready:

| Module | Lines | Status | Description |
|--------|-------|--------|-------------|
| `protocol.py` | 270 | ✅ | All service codes, segment selectors, constants |
| `exceptions.py` | 130 | ✅ | Complete exception hierarchy |
| `packet.py` | 370 | ✅ | 56-byte packet builder and parser |
| `connection.py` | 260 | ✅ | TCP socket with multi-packet response handling |
| `driver.py` | 690 | ✅ | All memory type read operations |

### Memory Types ✅

All 9 memory types with 15 access modes are working and verified:

| Type | Bit Mode | Byte Mode | Word Mode | Status |
|------|----------|-----------|-----------|--------|
| %R (Registers) | - | - | ✅ | **VERIFIED** |
| %AI (Analog Input) | - | - | ✅ | **VERIFIED** |
| %AQ (Analog Output) | - | - | ✅ | **VERIFIED** |
| %I (Discrete Input) | ✅ | ✅ | - | **VERIFIED** |
| %Q (Discrete Output) | ✅ | ✅ | - | **VERIFIED** |
| %M (Internal Memory) | ✅ | ✅ | - | **VERIFIED** |
| %T (Temporary Memory) | ✅ | ✅ | - | **VERIFIED** |
| %S (System Memory) | ✅ | ✅ | - | **VERIFIED** |
| %G (Global Memory) | ✅ | ✅ | - | **VERIFIED** |

### PLC Diagnostics ✅

All diagnostic functions implemented and tested:
- `get_plc_status()` - PLC short status query
- `get_controller_info()` - Controller type and ID
- `get_program_names()` - Control program names
- `get_plc_datetime()` - PLC date/time
- `get_fault_table()` - Fault information

---

## Major Protocol Discoveries

During development, we made **5 critical discoveries** not documented in academic literature:

### Discovery #1: All-Zeros Initialization ✅
**Finding**: Initialization must be exactly 56 bytes of zeros (not the pattern in reference implementations)
**Source**: DFRWS 2017 paper quote: "initialize bit streams of all zeros"
**Implementation**: `protocol.py` - `INIT_PACKET_1 = bytes(56)`

### Discovery #2: Multi-Packet TCP Responses ✅
**Finding**: PLC sends responses in TWO separate TCP packets:
1. First packet: 56-byte header (with byte 4 indicating payload length)
2. Second packet: Payload data (if any)

**New Finding**: Message type 0x94 (ACK_WITH_DATA) not documented in DFRWS paper
**Implementation**: `connection.py` - `_receive_data()` method

### Discovery #3: CPU Slot-Specific Addressing ✅
**Finding**: Mailbox destination (bytes 36-39) must specify correct CPU slot
**Formula**: First byte = `slot × 0x10`
**Current Test PLC**: Slot 0 → `0x00 0x0E 0x00 0x00` (previously tested with slot 2 → `0x20 0x0E 0x00 0x00`)
**Implementation**: `protocol.py` - `get_mailbox_destination(slot)` function

### Discovery #4: 0-Based Protocol Addressing ✅
**Finding**: Protocol uses 0-based addressing; PLC UI uses 1-based
**Mapping**: %R1 on PLC = address 0 in protocol
**Formula**: Protocol Address = PLC Register Number - 1
**Documentation**: `PROTOCOL_DISCOVERIES.md` section 4

### Discovery #5: RX3i-Specific Minimum Lengths ✅
**Finding**: GE RX3i requires HIGHER minimums than Series 90-30:
- Word operations: 4 words (same as 90-30)
- Byte operations: **8 bytes** (higher than 90-30's 4 bytes)
- Bit operations: **64 bits** (higher than 90-30's 32 bits)

**Impact**: This discovery unlocked ALL discrete I/O functionality!
**Implementation**: All read methods in `driver.py`

**Complete technical details**: See `docs/protocol.md`

---

## Protocol Specifications

### Packet Structure (56-byte header)

```
Byte 0:    Type (0x02=Request, 0x03=Response)
Byte 1:    Reserved (0x00)
Byte 2:    Sequence Number
Byte 3:    Reserved (0x00)
Byte 4:    Payload Length (DISCOVERED - not in DFRWS paper!)
Bytes 5-8: Reserved (0x00)
Byte 9:    Reserved (0x01)
Bytes 10-16: Reserved (0x00)
Byte 17:   Reserved (0x01)
Bytes 18-25: Reserved (0x00)
Byte 26:   Time - seconds
Byte 27:   Time - minutes
Byte 28:   Time - hours
Byte 29:   Reserved (0x00)
Byte 30:   Sequence Number (duplicate)
Byte 31:   Message Type (0xC0=Request, 0x94=ACK_WITH_DATA, 0xD4=ACK, 0xD1=Error)
Bytes 32-35: Mailbox Source (0x00 00 00 00)
Bytes 36-39: Mailbox Destination (slot-specific: slot * 0x10, 0x0E, 0x00, 0x00)
Byte 40:   Packet Number (0x01)
Byte 41:   Total Packets (0x01)
Byte 42:   Service Request Code
Byte 43:   Segment Selector
Byte 44:   Data Offset LSB (little-endian)
Byte 45:   Data Offset MSB
Byte 46:   Data Length LSB (little-endian)
Byte 47:   Data Length MSB
Bytes 48-55: Reserved (0x00)
```

### Service Request Codes (Implemented)

```
0x00 - PLC Short Status Request ✅
0x03 - Return Control Program Names ✅
0x04 - Read System Memory ✅
0x25 - Return PLC Time/Date ✅
0x38 - Return Fault Table ✅
0x43 - Return Controller Type and ID Information ✅
```

### Service Codes (NOT Implemented - Write Operations)
```
0x07 - Write System Memory ⚠️ DANGEROUS - NOT IMPLEMENTED
0x08 - Write Task Memory ⚠️ DANGEROUS - NOT IMPLEMENTED
0x09 - Write Program Block Memory ⚠️ DANGEROUS - NOT IMPLEMENTED
0x23 - Set PLC State (RUN/STOP) ⚠️ DANGEROUS - NOT IMPLEMENTED
0x24 - Set PLC Time/Date (write operation)
0x39 - Clear Fault Table (write operation)
```

### Segment Selectors (All Implemented)

**Word Access (Register/Analog Memory)**:
- `0x08` - Registers (%R) - 16-bit word mode
- `0x0A` - Analog Inputs (%AI) - word mode
- `0x0C` - Analog Outputs (%AQ) - word mode

**Byte Access (Discrete Memory)**:
- `0x10` - Discrete Inputs (%I) - byte mode
- `0x12` - Discrete Outputs (%Q) - byte mode
- `0x16` - Discrete Internals (%M) - byte mode
- `0x14` - Discrete Temporaries (%T) - byte mode
- `0x18` - System A Discrete (%SA) - byte mode
- `0x1A` - System B Discrete (%SB) - byte mode
- `0x1C` - System C Discrete (%SC) - byte mode
- `0x1E` - System S Discrete (%S) - byte mode
- `0x38` - Genius Global Data (%G) - byte mode

**Bit Access (Discrete Memory)**:
- `0x46` - Discrete Inputs (%I) - bit mode
- `0x48` - Discrete Outputs (%Q) - bit mode
- `0x4C` - Discrete Internals (%M) - bit mode
- `0x4A` - Discrete Temporaries (%T) - bit mode
- `0x4E` - System A Discrete (%SA) - bit mode
- `0x50` - System B Discrete (%SB) - bit mode
- `0x52` - System C Discrete (%SC) - bit mode
- `0x54` - System S Discrete (%S) - bit mode
- `0x56` - Genius Global Data (%G) - bit mode

---

## Usage Examples

### Basic Read (0-Based Addressing!)

```python
from src.driver import GE_SRTP_Driver

# IMPORTANT: Specify correct CPU slot! (slot 0 for current test PLC)
# IMPORTANT: Use 0-based addressing! (Protocol Address = PLC Register Number - 1)

with GE_SRTP_Driver('172.16.12.124', slot=0) as plc:
    # Read %R1 (address 0)
    r1 = plc.read_register(0)
    print(f"%R1 = {r1}")

    # Read %R100 (address 99)
    r100 = plc.read_register(99)

    # Read multiple registers %R1-R10 (addresses 0-9)
    values = plc.read_register(0, count=10)

    # Read analog input %AI2 (address 1)
    ai2 = plc.read_analog_input(1)

    # Read discrete input %I1 (address 0)
    i1 = plc.read_discrete_input(0, mode='bit')
```

### All Memory Types

```python
# Registers (word mode)
plc.read_register(address, count=1)

# Analog I/O (word mode)
plc.read_analog_input(address, count=1)
plc.read_analog_output(address, count=1)

# Discrete I/O (bit or byte mode)
plc.read_discrete_input(address, count=1, mode='bit')
plc.read_discrete_output(address, count=1, mode='byte')
plc.read_discrete_internal(address, count=1, mode='bit')
plc.read_discrete_temp(address, count=1, mode='bit')

# System memory (bit or byte mode)
plc.read_system_memory('S', address, count, mode='byte')  # %S
plc.read_system_memory('SA', address, count, mode='byte')  # %SA
plc.read_system_memory('SB', address, count, mode='byte')  # %SB
plc.read_system_memory('SC', address, count, mode='byte')  # %SC

# Global memory (bit or byte mode)
plc.read_global_memory(address, count=1, mode='bit')

# PLC diagnostics
plc.get_plc_status()
plc.get_controller_info()
plc.get_program_names()
plc.get_plc_datetime()
plc.get_fault_table()
```

---

## Development Guidelines

### For Maintenance

The codebase is complete and stable. When maintaining:

1. **Preserve Safety**: Do NOT add write operations without extensive discussion
2. **Test Thoroughly**: All changes should be tested on real hardware
3. **Document Discoveries**: If you find new protocol behavior, document it
4. **Update docs/todo.md**: Mark enhancements as completed when implemented

### For Enhancements

See `docs/todo.md` "Optional Future Enhancements" section for ideas:

**High Priority**:
- Unit test suite (pytest)
- Mock PLC for testing
- API documentation generation

**Medium Priority**:
- Advanced forensic module
- 1-based addressing helpers
- Symbolic tag support (see `docs/symbolic_addressing.md`)

**Low Priority**:
- Web dashboard
- Multi-PLC support
- Write operations (⚠️ NOT RECOMMENDED)

### Code Style

The codebase follows:
- PEP 8 Python style guidelines
- Type hints for function signatures
- Comprehensive docstrings
- Descriptive variable names
- Single-purpose functions

### Testing Strategy

**Current Testing** (Manual with Real Hardware):
- All memory types tested and verified
- Example scripts tested
- Integration testing on GE RX3i IC695CPE330

**Future Testing** (Optional):
- Unit tests with pytest
- Mock PLC responses
- CI/CD pipeline
- Code coverage reporting

---

## Critical Information for Future Development

### Initialization Sequence

**CORRECT (Implemented)**:
```python
INIT_PACKET_1 = bytes(56)  # All zeros
INIT_PACKET_2 = bytes(56)  # All zeros
```

Expected responses:
- After packet 1: byte[0] = 0x01
- After packet 2: Connection ready

### Multi-Packet Reception

**CRITICAL**: PLC sends responses in TWO TCP packets:

```python
def _receive_data(self):
    # First recv: 56-byte header
    header = self.sock.recv(56)

    # Check byte 4 for payload length
    payload_length = header[4]

    if payload_length > 0:
        # Second recv: payload data
        payload = self.sock.recv(payload_length)
        return header + payload
    else:
        return header
```

### Minimum Length Requirements

**RX3i-Specific** (different from Series 90-30!):

| Access Mode | Minimum Length |
|-------------|----------------|
| Word (registers, analog) | 4 words |
| Byte (discrete) | 8 bytes |
| Bit (discrete) | 64 bits |

**Implementation**:
```python
# Enforce minimums, return only requested count
request_length = max(count, minimum)
response = self._send_request_and_receive(..., data_length=request_length)
values = response.extract_values()
return values[:count]  # Trim to requested count
```

### Slot Addressing

**CRITICAL**: Mailbox destination must match CPU slot:

```python
def get_mailbox_destination(slot: int = 1) -> bytes:
    """Generate mailbox destination for specific slot."""
    return bytes([slot * 0x10, 0x0E, 0x00, 0x00])
```

**Current Test PLC**: Slot 0 → `0x00 0x0E 0x00 0x00` (previously tested with slot 2 → `0x20 0x0E 0x00 0x00`)

### 0-Based Addressing

**Protocol uses 0-based addressing**. To read %R1 from PLC UI, use address 0:
- %R1 → address 0
- %R2 → address 1
- %R100 → address 99

Formula: `Protocol Address = PLC Register Number - 1`

---

## Security and Safety

### Read-Only Design ✅

This driver is **intentionally read-only** for safety:
- ✅ Cannot modify PLC program
- ✅ Cannot change PLC state (RUN/STOP)
- ✅ Cannot write to memory
- ✅ Cannot clear faults
- ✅ Cannot upload/download programs

### Security Warnings ⚠️

- **No Authentication**: GE-SRTP has minimal security by default
- **Use on Isolated Networks Only**: Never expose PLCs to internet
- **Legal Compliance Required**: Ensure authorization before accessing PLCs
- **Monitor Access**: Log all driver usage for audit trails

### Physical Safety (If Write Operations Ever Considered)

⚠️ **DANGER**: Write operations can cause:
- Equipment damage ($$$ to $$$$$ repairs)
- Worker injury or death
- Process shutdowns
- Environmental incidents

**If write operations are ever considered**, they MUST include:
- Explicit confirmation for EVERY write
- Comprehensive logging (who, what, when)
- Dry-run mode (test without executing)
- Rollback capability if possible
- Rate limiting
- Privilege level checking
- Emergency stop/disconnect

---

## Reference Materials

### Primary Sources
- **DFRWS 2017 Paper**: "Leveraging the SRTP protocol for over-the-network memory acquisition of a GE Fanuc Series 90-30"
- **FieldServer Datasheet**: FST_DFS_GE_SRTP.pdf

### Reference Implementations
- **TheMadHatt3r/ge-ethernet-SRTP**: Python (read-only)
- **kkuba91/uGESRTP**: C++ implementation
- **Palatis/packet-ge-srtp**: Wireshark dissector

### Project Documentation
- `README.md` - User guide
- `docs/overview.md` - Complete project summary
- `docs/protocol.md` - 5 major technical discoveries
- `docs/hardware.md` - RX3i hardware details
- `docs/symbolic_addressing.md` - Future enhancement guide
- `docs/wireshark.md` - Protocol debugging

---

## Success Metrics

All project goals achieved:

| Metric | Target | Status |
|--------|--------|--------|
| Core modules | 5 | ✅ 5 (100%) |
| Memory types | 9 | ✅ 9 (100%) |
| Access modes | 15 | ✅ 15 (100%) |
| Hardware testing | Required | ✅ Complete |
| Documentation | Comprehensive | ✅ Complete |
| Production ready | Yes | ✅ **YES** |

---

## Key Lessons Learned

For future protocol reverse engineering projects:

1. **Academic papers are invaluable but incomplete** - Real hardware testing reveals critical details
2. **Multi-packet responses are tricky** - TCP streaming behavior requires careful handling
3. **Hardware configuration matters** - Slot number, firmware version affect behavior
4. **Model-specific variations exist** - RX3i differs from Series 90-30
5. **Document everything** - Future developers will thank you
6. **Test incrementally** - Verify each discovery before moving on
7. **Ask about hardware** - Physical configuration is critical
8. **Use Wireshark** - Packet captures reveal undocumented behavior

---

## Versioning Strategy

The project follows **Semantic Versioning** (semver.org):

**Version Format**: `MAJOR.MINOR.PATCH` (e.g., 1.1.0)

- **MAJOR** version: Incompatible API changes (breaking changes)
- **MINOR** version: New functionality in backwards compatible manner
- **PATCH** version: Backwards compatible bug fixes

**Version Tracking Files**:
1. `VERSION` - Single-line version number (1.1.0)
2. `CHANGELOG.md` - Industry standard changelog following "Keep a Changelog" format
3. `src/__init__.py` - `__version__ = "1.1.0"` attribute

**When to Increment**:
- **MAJOR (1.0.0 → 2.0.0)**: Change API signatures, remove features, change addressing scheme
- **MINOR (1.0.0 → 1.1.0)**: Add new features, add new memory types, improve examples
- **PATCH (1.0.0 → 1.0.1)**: Fix bugs, update documentation, performance improvements

**Version History**:
- **v1.0.0** (2025-10-16) - Initial production release on IC695CPE330
- **v1.1.0** (2025-10-17) - New test rig, improved examples/tests, comprehensive testing

**Changelog Management**:
- All changes tracked in `CHANGELOG.md`
- "Unreleased" section for work in progress
- Move to version section on release
- Categories: Added, Changed, Deprecated, Removed, Fixed, Security

**Git Tags**:
- Tag releases with `v1.1.0` format
- Push tags to remote: `git push --tags`
- View tags: `git tag -l`

---

## Important Reminders

1. **This Driver is Complete**: All intended features are working
2. **Read-Only by Design**: Write operations NOT implemented for safety
3. **Hardware Specific**: Tested on GE RX3i IC695CPE330 (Firmware 10.85)
4. **0-Based Addressing**: Remember address = register_number - 1
5. **Slot 2 Required**: This PLC has CPU in slot 2
6. **Pure Python**: No external dependencies
7. **Production Ready**: Safe for forensic use, monitoring, research
8. **Well Documented**: 8 markdown files cover all aspects

---

**Project Status**: ✅ Production Ready
**Completion**: 100%
**Last Updated**: 2025-10-17
**Current Hardware**: GE PACSystems EPXCPE210 (Firmware 10.30) at 172.16.12.124:18245 (slot 0)
**Previous Hardware**: GE RX3i IC695CPE330 (Firmware 10.85) at 172.16.12.127:18245 (slot 2)
**Primary Use Case**: Forensic memory acquisition and PLC monitoring (read-only)

---

🎉 **MISSION ACCOMPLISHED!**

For questions or enhancements, consult `docs/overview.md` and `docs/protocol.md`.
