# PLC Hardware Configuration

## Current Test Rig: GE PACSystems EPXCPE210

**Date Confirmed**: 2025-10-17
**Status**: ✅ New test environment configuration

---

## Complete Rack Configuration

| Rack | Slot | Module | Description | Firmware | Status |
|------|------|--------|-------------|----------|--------|
| 0 | 0 | EPXCPE210 | CPU with integrated Ethernet | 10.30 | ✅ |
| 0 | 0.1 | IC695EFM001 | Integrated Ethernet (part of CPU) | 10.30 | ✅ |
| 0 | 1 | EP-12F4 | I/O Module | 0.00.00 | ✅ |
| 0 | 2 | EP-2714 | I/O Module | 0.00.03 | ✅ |

**Backplane**: Integrated PACSystems backplane

**Note**: The EPXCPE210 is a compact CPU with integrated Ethernet functionality. The CPU is in slot 0, which is important for SRTP mailbox addressing.

---

## CPU Details

**Model**: EPXCPE210 (PACSystems)
- **Series**: GE PACSystems RX3i
- **Type**: Programmable Automation Controller (PAC)
- **Firmware Version**: 10.30 [EJTT]
- **Boot Firmware**: -
- **Hardware Version**: 1.03
- **Serial Number**: R867467
- **Catalog Number**: EPXCPE210-AAAA
- **Physical Slot**: 0
- **Addressing Slot**: 0 (**critical for SRTP mailbox addressing!**)
- **Network**: Ethernet (172.16.12.124:18245)

### EPXCPE210 Specifications

The EPXCPE210 is a compact PACSystems CPU with integrated Ethernet:
- **Memory**: User memory for control programs
- **Speed**: Fast scan times for real-time control
- **Communications**:
  - Integrated Ethernet (10/100 Mbps)
  - SRTP protocol support ✅
- **I/O Capacity**: Expandable with I/O modules
- **Programming**: Proficy Machine Edition
- **Special Note**: **NO PROGRAM LOADED** - Clean slate for testing

---

## I/O Module Details

### Slot 1: EP-12F4

**Model**: EP-12F4
- **Primary Firmware**: 0.00.00
- **Hardware Version**: 1.02.00
- **Serial Number**: AQ1L40PC7300193
- **Catalog Number**: EP-12F4
- **Status**: Available for testing

### Slot 2: EP-2714

**Model**: EP-2714
- **Primary Firmware**: 0.00.03
- **Hardware Version**: 1.10.00
- **Serial Number**: AS4D40PC7300083
- **Catalog Number**: EP-2714
- **Status**: Available for testing

---

## Why Slot 0 is Critical

**Mailbox Addressing Formula**: `first_byte = slot × 0x10`

For this CPU in slot 0:
```
Mailbox destination = 0x00 0x0E 0x00 0x00
                       ↑
                       0 × 0x10 = 0x00
```

**Impact**:
- Using slot 1 (default `0x10 0x0E 0x00 0x00`) would result in:
  - ✓ PLC acknowledges requests
  - ✗ Returns empty payloads (wrong routing)

**Implementation**: `GE_SRTP_Driver('172.16.12.124', slot=0)`

See `docs/protocol.md` section 3 for detailed explanation.

---

## Testing Advantages

### Clean Slate Benefits ✅

This new test rig has **NO PROGRAM LOADED**, which provides significant advantages:

1. **Predictable State**: No running logic to interfere with tests
2. **Known Memory Values**: Memory areas will be in default/zero state
3. **Better Testing**: Can verify protocol behavior without program interference
4. **Safer Experimentation**: No risk of disrupting active processes
5. **Baseline Establishment**: Can establish protocol behavior from scratch

---

## SRTP Protocol Compatibility

**Status**: ✅ **EXPECTED TO BE FULLY COMPATIBLE**

The PACSystems RX3i series uses the same GE-SRTP protocol as:
- Series 90-30
- Series 90-70
- VersaMax
- Other PACSystems RX3i CPUs (including IC695CPE330)

This driver is expected to work perfectly because:
1. PACSystems implements standard GE-SRTP over TCP port 18245
2. Firmware 10.30 should support all standard SRTP features
3. Protocol behavior should match DFRWS 2017 specification (with discovered additions)

**Key Discovery**: RX3i requires **higher minimum lengths** than Series 90-30:
- Word operations: 4 words (same as 90-30)
- Byte operations: 8 bytes (higher than 90-30)
- Bit operations: 64 bits (higher than 90-30)

See `docs/protocol.md` section 5 for complete details.

---

## Network Configuration

**IP Address**: 172.16.12.124
**Port**: 18245 (default SRTP port)
**Protocol**: TCP/IP over Ethernet
**Network Type**: Isolated industrial network
**Access**: Development workstation on same network

---

## Connection String

For this specific PLC, use:

```python
from src.driver import GE_SRTP_Driver

# CRITICAL: slot=0 parameter is MANDATORY for this hardware!
plc = GE_SRTP_Driver('172.16.12.124', slot=0)
plc.connect()

# Read memory types
r1 = plc.read_register(0)                    # %R1 (word mode)
ai1 = plc.read_analog_input(0)               # %AI1 (word mode)
aq1 = plc.read_analog_output(0)              # %AQ1 (word mode)
i1 = plc.read_discrete_input(0, mode='bit')  # %I1 (bit mode)
q1 = plc.read_discrete_output(0, mode='byte') # %Q1 (byte mode)
```

**CRITICAL**: `slot=0` parameter is mandatory for this hardware!

---

## Firmware Compatibility

**CPU Firmware**: 10.30 [EJTT]

This driver is compatible with PACSystems firmware:
- ✅ Version 10.x series (previously tested with 10.85, now testing with 10.30)
- Likely ✅ Version 9.x series
- Likely ✅ Version 8.x series
- Unknown: Earlier versions (< 8.0)

The SRTP protocol has been stable across firmware versions.

---

## Physical Installation

Visual representation of the rack:

```
┌─────────────┬─────────────┬─────────────┐
│   Slot 0    │   Slot 1    │   Slot 2    │
│ EPXCPE210   │   EP-12F4   │   EP-2714   │
│  CPU with   │  I/O Module │  I/O Module │
│ Integrated  │             │             │
│  Ethernet   │             │             │
└─────────────┴─────────────┴─────────────┘
```

**Note**: The EPXCPE210 is a compact, single-wide CPU with integrated Ethernet in slot 0. This is different from the previous IC695CPE330 which was a double-wide module in slots 2-3.

---

## Module Part Numbers Summary

| Type | Part Number | Description |
|------|-------------|-------------|
| CPU | EPXCPE210-AAAA | Compact CPU with integrated Ethernet |
| Integrated Ethernet | IC695EFM001 | Part of EPXCPE210 CPU |
| I/O Module | EP-12F4 | 12-point I/O module |
| I/O Module | EP-2714 | 27-point I/O module |

---

## Comparison with Previous Test Hardware

### Previous Hardware (IC695CPE330)
- **Model**: IC695CPE330
- **IP**: 172.16.12.127
- **Slot**: 2 (double-wide module, slots 2-3)
- **Firmware**: 10.85
- **Program**: Production program loaded
- **12-slot backplane with multiple I/O modules**

### Current Hardware (EPXCPE210)
- **Model**: EPXCPE210
- **IP**: 172.16.12.124
- **Slot**: 0 (single-wide, compact design)
- **Firmware**: 10.30
- **Program**: **NO PROGRAM LOADED** ✅
- **Compact configuration with 2 I/O modules**

**Key Difference**: Slot 0 vs Slot 2 - All code examples and tests need updating!

---

## Documentation References

### GE Documentation
- **CPU Manual**: EPXCPE210 User Manual
- **Hardware Installation**: PACSystems Installation Manual
- **Programming**: PACSystems Programming Manual
- **SRTP Protocol**: See reference PDFs in `reference/` directory

### Driver Documentation
- `docs/overview.md` - Complete project summary
- `docs/protocol.md` - 5 major technical discoveries
- `README.md` - User guide
- `docs/todo.md` - Project status and completion tracking

---

## Summary

**PLC Model**: GE PACSystems EPXCPE210
**Location**: 172.16.12.124:18245
**CPU Slot**: 0 (**mandatory parameter - CHANGED FROM PREVIOUS SLOT 2**)
**Firmware**: 10.30 [EJTT]
**Hardware Version**: 1.03
**Serial Number**: R867467
**Configuration**: Compact with 2 I/O modules
**Program Status**: **NO PROGRAM LOADED** - Clean testing environment
**Driver Status**: ✅ **EXPECTED TO BE FULLY COMPATIBLE**

**Installed Modules**:
- ✅ Integrated Ethernet (IC695EFM001 as part of CPU)
- ✅ EP-12F4 I/O module (Slot 1)
- ✅ EP-2714 I/O module (Slot 2)

**Driver Features**:
- ✅ All 9 memory types supported (%R, %AI, %AQ, %I, %Q, %M, %T, %S, %G)
- ✅ All 15 access modes available (word, byte, bit)
- ✅ PLC diagnostics functions
- ✅ Multi-packet TCP response handling
- ✅ Slot-specific mailbox addressing
- ✅ RX3i-specific minimum length enforcement

**Testing Status**: Ready for comprehensive testing with clean PLC state.

---

**Last Updated**: 2025-10-17
**Configuration**: New test rig with clean slate (no program loaded)
**Documentation**: See `docs/overview.md` for complete details
