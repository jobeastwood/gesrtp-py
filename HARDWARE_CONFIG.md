# PLC Hardware Configuration

## Verified Hardware: GE RX3i IC695CPE330

**Date Confirmed**: 2025-10-16
**Status**: ✅ Complete hardware configuration verified

---

## Complete Rack Configuration

| Rack | Slot | Module | Description | Firmware | Status |
|------|------|--------|-------------|----------|--------|
| 0 | 0 | IC695PSD140 | Power Supply (24 VDC, 40 W) | 1.10 | ✅ |
| 0 | 1 | (Empty) | - | - | - |
| 0 | 2 | IC695CPE330 | CPU (double-wide, occupies slots 2-3) | 10.85 | ✅ |
| 0 | 3 | IC695CPE330 | CPU (continuation of slot 2) | - | ✅ |
| 0 | 4 | IC695ETM001 | Ethernet Module | - | ✅ |
| 0 | 5 | IC695ETM001 | Ethernet Module | - | ✅ |
| 0 | 6 | IC694ALG223 | Analog Input (16 Ch, 0-20 mA) | - | ✅ |
| 0 | 7 | IC694ALG392 | Analog Output (8 Ch, 4-20 mA) | - | ✅ |
| 0 | 8 | IC694MDL240 | Discrete Input (16 Ch, 120 VAC) | - | ✅ |
| 0 | 9 | IC694MDL916 | Discrete Output (16 Ch, 24 VDC) | - | ✅ |

**Backplane**: IC695CHS012 (12-slot universal backplane)

**Note**: The IC695CPE330 CPU is a double-wide module that physically occupies both slots 2 and 3. By convention, the leftmost slot (slot 2) is used as the identifier for SRTP mailbox addressing.

---

## CPU Details

**Model**: IC695CPE330
- **Series**: GE RX3i (PACSystems)
- **Type**: Programmable Automation Controller (PAC)
- **Firmware Version**: 10.85
- **Physical Slots**: 2 and 3 (double-wide module)
- **Addressing Slot**: 2 (leftmost slot, **critical for SRTP mailbox addressing!**)
- **Network**: Ethernet (172.16.12.127:18245)

### IC695CPE330 Specifications

The IC695CPE330 is a high-performance RX3i CPU:
- **Memory**: 20MB user memory
- **Speed**: Fast scan times for real-time control
- **Communications**:
  - Ethernet (10/100 Mbps)
  - Serial ports
  - SRTP protocol support ✅
- **I/O Capacity**: Up to 8K discrete I/O, 8K analog I/O
- **Programming**: Proficy Machine Edition (PAC Machine Edition v10.6)

---

## I/O Module Details

### Ethernet Modules

**Slots 4 & 5**: IC695ETM001
- **Purpose**: Additional Ethernet ports for network connectivity
- **Functionality**: Allow multiple network connections
- **Use Case**: Separate networks for SCADA, programming, field devices

### Analog I/O Modules

**Slot 6**: IC694ALG223 - Analog Input Module
- **Channels**: 16 inputs
- **Input Type**: 0-20 mA current loop
- **Status**: ✅ **VERIFIED WORKING**
- **Test Result**: %AI2 = 20 (live sensor data detected)

**Slot 7**: IC694ALG392 - Analog Output Module
- **Channels**: 8 outputs
- **Output Type**: 4-20 mA current loop
- **Status**: ✅ **VERIFIED WORKING**
- **Test Result**: All outputs reading as 0 (no active control signals)

### Discrete I/O Modules

**Slot 8**: IC694MDL240 - Discrete Input Module
- **Channels**: 16 inputs
- **Input Type**: 120 VAC
- **Status**: ✅ **VERIFIED WORKING**
- **Test Result**: Successfully reading discrete input states (bit & byte modes)
- **Note**: IC694 series modules work in RX3i backplanes

**Slot 9**: IC694MDL916 - Discrete Output Module
- **Channels**: 16 outputs
- **Output Type**: 24 VDC
- **Status**: ✅ **VERIFIED WORKING**
- **Test Result**: Successfully reading discrete output states (bit & byte modes)

---

## Why Slot 2 is Critical

**Mailbox Addressing Formula**: `first_byte = slot × 0x10`

For this CPU in slot 2:
```
Mailbox destination = 0x20 0x0E 0x00 0x00
                       ↑
                       2 × 0x10 = 0x20
```

**Impact**:
- Using slot 1 (default `0x10 0x0E 0x00 0x00`) would result in:
  - ✓ PLC acknowledges requests
  - ✗ Returns empty payloads (wrong routing)

**Implementation**: `GE_SRTP_Driver('172.16.12.127', slot=2)`

See `PROTOCOL_DISCOVERIES.md` section 3 for detailed explanation.

---

## Memory Map (All Working!)

### Word Access Memory Types ✅

| Type | Description | Hardware | Test Result |
|------|-------------|----------|-------------|
| %R | Register Memory | CPU | ✅ VERIFIED (%R1=27546, %R2=18174) |
| %AI | Analog Inputs | IC694ALG223 (Slot 6) | ✅ VERIFIED (%AI2=20, live sensor) |
| %AQ | Analog Outputs | IC694ALG392 (Slot 7) | ✅ VERIFIED (all zeros) |

### Discrete Memory Types ✅

| Type | Description | Hardware | Test Result |
|------|-------------|----------|-------------|
| %I | Discrete Inputs | IC694MDL240 (Slot 8) | ✅ VERIFIED (bit & byte modes) |
| %Q | Discrete Outputs | IC694MDL916 (Slot 9) | ✅ VERIFIED (bit & byte modes) |
| %M | Internal Memory | CPU | ✅ VERIFIED (bit & byte modes) |
| %T | Temporary Memory | CPU | ✅ VERIFIED (bit & byte modes) |
| %S | System Memory | CPU | ✅ VERIFIED (%S, %SA, %SB, %SC) |
| %G | Genius Global | CPU | ✅ VERIFIED (bit & byte modes) |

**Result**: All 9 memory types with 15 access modes - **100% WORKING!**

---

## SRTP Protocol Compatibility

**Status**: ✅ **FULLY COMPATIBLE**

The RX3i series uses the same GE-SRTP protocol as:
- Series 90-30
- Series 90-70
- VersaMax
- Other PACSystems RX3i CPUs

Our driver works perfectly because:
1. RX3i implements standard GE-SRTP over TCP port 18245
2. Firmware 10.85 supports all tested features
3. Protocol behavior matches DFRWS 2017 specification (with discovered additions)

**Key Discovery**: RX3i requires **higher minimum lengths** than Series 90-30:
- Word operations: 4 words (same as 90-30)
- Byte operations: 8 bytes (higher than 90-30)
- Bit operations: 64 bits (higher than 90-30)

See `PROTOCOL_DISCOVERIES.md` section 5 for complete details.

---

## Network Configuration

**IP Address**: 172.16.12.127
**Port**: 18245 (default SRTP port)
**Protocol**: TCP/IP over Ethernet
**Network Type**: Isolated industrial network
**Access**: Raspberry Pi 5 on same network

---

## Connection String

For this specific PLC, use:

```python
from src.driver import GE_SRTP_Driver

# CRITICAL: slot=2 parameter is MANDATORY for this hardware!
plc = GE_SRTP_Driver('172.16.12.127', slot=2)
plc.connect()

# Read all memory types
r1 = plc.read_register(0)                    # %R1 (word mode)
ai2 = plc.read_analog_input(1)                # %AI2 (word mode)
aq1 = plc.read_analog_output(0)               # %AQ1 (word mode)
i1 = plc.read_discrete_input(0, mode='bit')   # %I1 (bit mode)
q1 = plc.read_discrete_output(0, mode='byte') # %Q1 (byte mode)
```

**CRITICAL**: `slot=2` parameter is mandatory for this hardware!

---

## Firmware Compatibility

**CPU Firmware**: 10.85

Our driver is compatible with RX3i firmware:
- ✅ Version 10.x series (tested with 10.85)
- Likely ✅ Version 9.x series
- Likely ✅ Version 8.x series
- Unknown: Earlier versions (< 8.0)

The SRTP protocol has been stable across firmware versions.

---

## Physical Installation

Visual representation of the rack:

```
┌─────────────┬─────────────┬───────────────────────────┬─────────────┐
│   Slot 0    │   Slot 1    │      Slots 2-3            │   Slot 4    │
│ IC695PSD140 │   (Empty)   │     IC695CPE330           │ IC695ETM001 │
│   Power     │             │     CPU (double-wide)     │  Ethernet   │
│   Supply    │             │                           │             │
└─────────────┴─────────────┴───────────────────────────┴─────────────┘

┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│   Slot 5    │   Slot 6    │   Slot 7    │   Slot 8    │   Slot 9    │
│ IC695ETM001 │ IC694ALG223 │ IC694ALG392 │ IC694MDL240 │ IC694MDL916 │
│  Ethernet   │  Analog In  │ Analog Out  │ Discrete In │Discrete Out │
│             │   (16 Ch)   │   (8 Ch)    │   (16 Ch)   │   (16 Ch)   │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

**Note**: The CPU (IC695CPE330) is a double-wide module spanning slots 2-3. For SRTP addressing, we use the leftmost slot (slot 2) as the identifier.

---

## Module Part Numbers Summary

| Type | Part Number | Description |
|------|-------------|-------------|
| Power Supply | IC695PSD140 | 24 VDC, 40 W |
| CPU | IC695CPE330 | 20MB memory, Ethernet |
| Ethernet | IC695ETM001 | 10/100 Mbps (×2) |
| Analog Input | IC694ALG223 | 16 Ch, 0-20 mA |
| Analog Output | IC694ALG392 | 8 Ch, 4-20 mA |
| Discrete Input | IC694MDL240 | 16 Ch, 120 VAC |
| Discrete Output | IC694MDL916 | 16 Ch, 24 VDC |

**Note**: IC694 series modules (Series 90-30 modules) are compatible with RX3i backplanes.

---

## Power Supply

**Model**: IC695PSD140
- **Input**: 120/240V AC
- **Output**: 24 VDC, 40 W
- **Purpose**: Provides DC power to all modules in the rack
- **Features**: Hot-swappable (on some configurations)
- **Firmware**: 1.10

---

## Documentation References

### GE Documentation
- **CPU Manual**: GFK-2222 (IC695CPE330 User Manual)
- **Hardware Installation**: GFK-2223 (RX3i Installation Manual)
- **Programming**: GFK-2950 (PACSystems Programming Manual)
- **SRTP Protocol**: See reference PDFs in `reference/` directory

### Driver Documentation
- `PROJECT_OVERVIEW.md` - Complete project summary
- `PROTOCOL_DISCOVERIES.md` - 5 major technical discoveries
- `README.md` - User guide
- `TODO.md` - Project status and completion tracking

---

## Summary

**PLC Model**: GE RX3i IC695CPE330
**Location**: 172.16.12.127:18245
**CPU Slot**: 2 (**mandatory parameter**)
**Firmware**: 10.85
**Backplane**: IC695CHS012 (12-slot)
**Driver Status**: ✅ **FULLY COMPATIBLE**

**Installed I/O Modules**:
- ✅ 2 Ethernet modules (IC695ETM001)
- ✅ 16-channel analog input (IC694ALG223)
- ✅ 8-channel analog output (IC694ALG392)
- ✅ 16-channel discrete input (IC694MDL240)
- ✅ 16-channel discrete output (IC694MDL916)

**Driver Features**:
- ✅ All 9 memory types working (%R, %AI, %AQ, %I, %Q, %M, %T, %S, %G)
- ✅ All 15 access modes verified (word, byte, bit)
- ✅ PLC diagnostics functions
- ✅ Multi-packet TCP response handling
- ✅ Slot-specific mailbox addressing
- ✅ RX3i-specific minimum length enforcement

**Test Results**: All memory types tested and verified on this exact hardware configuration.

---

**Last Updated**: 2025-10-16
**Verified By**: Live testing with actual PLC hardware
**Documentation**: See `PROJECT_OVERVIEW.md` for complete details
