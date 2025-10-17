# Wireshark Packet Capture Guide for GE-SRTP Research

## Objective
Capture and analyze GE-SRTP packets to understand:
1. **Symbolic tag addressing** - How KEPServerEX implements tag-based reads
2. **Additional data types** - INT, DINT, UINT, BYTE, WORD, DWORD, REAL, LREAL, STRING, ENUM
3. **Write operations** - Protocol for writing data to PLC
4. **Protocol variations** - Firmware-specific or model-specific differences

---

## Current Environment

### Hardware Setup
- **Development PC**: Windows 10/11
- **Current Test PLC**: Emerson PACSystems EPXCPE210 (Firmware 10.30) at 172.16.12.124:18245 (slot 0)
- **Previous PLC**: Emerson RX3i IC695CPE330 (Firmware 10.85) at 172.16.12.127:18245 (slot 2)
- **Network**: Isolated industrial network

### Software
- **Wireshark** for Windows
- **KEPServerEX** with GE Ethernet driver
- **Python 3.x** with gesrtp-py driver
- **PAC Machine Edition** (optional, for PLC programming)

---

## Prerequisites

1. **Wireshark installed** on Windows PC
   - Download from: https://www.wireshark.org/download.html
   - Install with administrator privileges
   - Include WinPcap/Npcap during installation

2. **KEPServerEX installed** with GE Ethernet driver
   - Configure connection to PLC
   - Set up some test tags (symbolic names)

3. **Network interface** connected to PLC network
   - Ethernet adapter on same subnet as PLC
   - IP address: 172.16.12.x (not .124 or .127)

4. **Administrator access** for packet capture

---

## Method 1: Wireshark GUI (Recommended for Windows)

### Step 1: Identify Network Interface

1. Open **Command Prompt**
2. Run: `ipconfig /all`
3. Find the adapter connected to PLC network (e.g., "Ethernet", "Local Area Connection")
4. Note the interface name

### Step 2: Start Wireshark

1. **Run Wireshark as Administrator**
   - Right-click Wireshark icon
   - Select "Run as administrator"

2. **Select Network Interface**
   - Choose the interface connected to PLC network
   - Double-click to start capture

3. **Set Display Filter** (optional, for cleaner view)
   ```
   ip.addr == 172.16.12.124 && tcp.port == 18245
   ```
   - Enter in filter bar at top
   - Click Apply

### Step 3: Capture KEPServerEX Traffic

**Objective**: Understand symbolic tag addressing

1. **Configure KEPServerEX**:
   - Create channel: "GE_PLC"
   - Device: "EPXCPE210" at 172.16.12.124
   - Add tags:
     - `Tag1` → %R1 (INT)
     - `Tag2` → %R2 (DINT)
     - `TempSensor` → %AI1 (REAL)
     - `OutputStatus` → %Q1 (BOOL)

2. **Start OPC Quick Client**:
   - Browse to created tags
   - Right-click → Read (refresh every 1-2 seconds)

3. **Watch Wireshark**:
   - Observe packet flow
   - Look for patterns in requests

4. **Stop Capture**:
   - Wireshark → Capture → Stop
   - Save as: `kepserver_symbolic_tags.pcapng`

### Step 4: Capture Python Driver Traffic

**Objective**: Compare direct addressing vs symbolic

1. **Keep Wireshark running**

2. **Run Python test**:
   ```bash
   cd C:\Users\jeastwood\Documents\git\personal\gesrtp-py
   python tests\01_connection_basic.py
   ```

3. **Stop and save**:
   - Save as: `python_direct_addressing.pcapng`

### Step 5: Analyze Captures

1. **Compare packets side-by-side**:
   - KEPServerEX request structure
   - Python driver request structure
   - Identify differences

2. **Look for symbolic tag protocol**:
   - Service codes different from 0x04?
   - Additional payload data?
   - Different packet structure?

---

## Method 2: Command Line Capture (dumpcap)

For automated/scripted captures:

### Using dumpcap (included with Wireshark)

```batch
@echo off
REM Capture SRTP traffic to PLC
set PLC_IP=172.16.12.124
set PLC_PORT=18245
set OUTPUT_FILE=plc_capture.pcapng

echo Starting packet capture for %PLC_IP%:%PLC_PORT%
echo Press Ctrl+C to stop
echo.

"C:\Program Files\Wireshark\dumpcap.exe" ^
  -i "Ethernet" ^
  -f "host %PLC_IP% and port %PLC_PORT%" ^
  -w %OUTPUT_FILE%

echo.
echo Capture saved to %OUTPUT_FILE%
pause
```

Save as: `capture_srtp.bat`

Run as Administrator

---

## Research Focus Areas

### 1. Symbolic Tag Addressing Investigation

**Questions to Answer**:
1. How does KEPServerEX request tags by name?
2. Is there a tag name → address resolution packet?
3. Does PLC store tag-to-address mappings?
4. Can we replicate symbolic addressing in Python?

**Packet Analysis**:
- Compare service codes (byte 42)
- Check for string payloads (tag names)
- Look for tag metadata requests
- Identify address translation mechanism

**See `docs/symbolic_addressing.md` for detailed investigation plan**

### 2. Data Type Support Research

**Current Support**: 16-bit words only
**Goal**: Support multiple data types

| Data Type | Size | Expected Encoding | Status |
|-----------|------|-------------------|--------|
| BOOL/BIT | 1 bit | Single bit | ✅ Working |
| BYTE | 8 bits | Unsigned byte | ✅ Working |
| WORD | 16 bits | Unsigned word | ⚠️ As register |
| INT | 16 bits | Signed integer | 🔬 Research |
| UINT | 16 bits | Unsigned integer | 🔬 Research |
| DWORD | 32 bits | Unsigned double word | 🔬 Research |
| DINT | 32 bits | Signed double integer | 🔬 Research |
| UDINT | 32 bits | Unsigned double integer | 🔬 Research |
| REAL | 32 bits | IEEE 754 float | 🔬 Research |
| LREAL | 64 bits | IEEE 754 double | 🔬 Research |
| STRING | Variable | ASCII/UTF-8 | 🔬 Research |
| ENUM | Variable | Enumerated values | 🔬 Research |

**Investigation Steps**:
1. Create PLC program with different data types
2. Use KEPServerEX to read each type
3. Capture packets for each data type
4. Identify:
   - Service codes used
   - Segment selectors
   - Payload encoding
   - Byte order (little-endian confirmed for words)

### 3. Write Operations Research

**Current Status**: Read-only driver
**Goal**: Safe write operation support

⚠️ **CRITICAL**: Write operations are DANGEROUS
- Can damage equipment
- Can cause physical harm
- Can disrupt processes
- Must implement extensive safety checks

**Investigation Approach**:
1. **Capture KEPServerEX writes**:
   - Use OPC Quick Client to write values
   - Capture packets
   - Analyze write packet structure

2. **Identify write service codes**:
   - 0x07 - Write System Memory?
   - 0x08 - Write Task Memory?
   - Other codes?

3. **Understand payload structure**:
   - Address encoding
   - Value encoding
   - Verification/checksum

4. **Safety implementation plan**:
   - Dry-run mode (validate but don't send)
   - Explicit confirmation for every write
   - Logging (who, what, when)
   - Rollback capability (if possible)
   - Rate limiting
   - Emergency stop/disconnect

**DO NOT IMPLEMENT writes until fully understood and safety measures in place!**

---

## What to Look For in Captures

### Standard Read Request (Known Working)

**56-byte header**:
```
Byte 0:     0x02 (Request packet type)
Byte 2/30:  Sequence number
Byte 4:     0x00 (no payload in request)
Byte 31:    0xC0 (Message type: SERVICE_REQUEST)
Bytes 36-39: Mailbox destination (slot-specific)
            - Slot 0: 0x00 0x0E 0x00 0x00 (EPXCPE210)
            - Slot 2: 0x20 0x0E 0x00 0x00 (IC695CPE330)
Byte 42:    0x04 (Service code: READ_SYSTEM_MEMORY)
Byte 43:    Segment selector:
            - 0x08: Registers (%R)
            - 0x0A: Analog Inputs (%AI)
            - 0x10: Discrete Inputs byte (%I)
            - 0x46: Discrete Inputs bit (%I)
Bytes 44-45: Data offset (little-endian)
Bytes 46-47: Data length (little-endian)
```

### Standard Read Response

**56-byte header + payload**:
```
Byte 0:     0x03 (Response packet type)
Byte 2/30:  Sequence number (matches request)
Byte 4:     Payload length (0 = empty, >0 = has data)
Byte 31:    Response type:
            - 0x94: ACK_WITH_DATA (success, has payload)
            - 0xD4: ACK_NO_DATA (acknowledged, no data)
            - 0xD1: ERROR (request failed)
```

### Unknown Patterns to Identify

**KEPServerEX may use**:
- Different service codes for symbolic tags
- Tag name resolution requests
- Metadata queries
- Different segment selectors
- Extended payload formats

**Questions**:
1. Are there packets before tag reads?
2. Do symbolic tags use different service codes?
3. Is there a "lookup tag address" operation?
4. How are strings/arrays handled?

---

## Packet Capture Best Practices

### 1. Capture Sequentially

Don't mix different operations in one capture:

```
Capture 1: KEPServerEX symbolic tag reads
Capture 2: Python direct address reads
Capture 3: KEPServerEX writes
Capture 4: Python reads of different data types
Capture 5: KEPServerEX reads of different data types
```

### 2. Label Everything

File naming convention:
```
YYYYMMDD_HHMMSS_description.pcapng

Examples:
20251017_143052_kepserver_symbolic_read_tags.pcapng
20251017_144211_python_direct_read_registers.pcapng
20251017_150334_kepserver_write_int_value.pcapng
```

### 3. Document Test Conditions

Create a log file for each capture:
```
Capture: kepserver_symbolic_read_tags.pcapng
Date: 2025-10-17 14:30
PLC: EPXCPE210 at 172.16.12.124 (slot 0)
Software: KEPServerEX 6.x with GE Ethernet driver

Operations performed:
1. Read tag "Tag1" (%R1) - INT type
2. Read tag "TempSensor" (%AI1) - REAL type
3. Read tag "OutputStatus" (%Q1) - BOOL type

Total packets: 47
Duration: 2 minutes

Observations:
- KEPServerEX polls every 1000ms
- Each tag read generates 2 packets (request + response)
- Noticed service code 0x04 used for all tags
- No obvious symbolic addressing mechanism visible
```

### 4. Use Wireshark Filters

**During capture (Capture Filter)**:
```
host 172.16.12.124 and port 18245
```

**During analysis (Display Filter)**:
```
# Show only SRTP traffic
tcp.port == 18245

# Show only requests
tcp.port == 18245 and frame[56] == 0x02

# Show only responses
tcp.port == 18245 and frame[56] == 0x03

# Show requests with specific service code
tcp.port == 18245 and frame[56] == 0x02 and frame[98] == 0x04

# Show responses with data
tcp.port == 18245 and frame[56] == 0x03 and frame[60] > 0
```

---

## Analysis Workflow

### Step 1: Identify Packet Pairs

Each operation = Request + Response

1. **Find request**:
   - Byte 0 = 0x02
   - Byte 31 = 0xC0
   - Note sequence number (bytes 2 and 30)

2. **Find matching response**:
   - Byte 0 = 0x03
   - Same sequence number

### Step 2: Decode Request

Extract key fields:
- Service code (byte 42)
- Segment selector (byte 43)
- Address (bytes 44-45, little-endian)
- Length (bytes 46-47, little-endian)

### Step 3: Decode Response

Check:
- Payload length (byte 4)
- Response type (byte 31)
- If data present, decode payload

### Step 4: Compare Patterns

**KEPServerEX vs Python**:
- Same service codes?
- Same segment selectors?
- Different packet structure?
- Additional fields?

### Step 5: Document Findings

Update `docs/protocol.md` with discoveries

---

## Windows Batch Script

Save as `start_wireshark_capture.bat`:

```batch
@echo off
REM ============================================================
REM Wireshark Packet Capture for GE-SRTP Research
REM ============================================================

set PLC_IP=172.16.12.124
set PLC_PORT=18245
set INTERFACE=Ethernet
set OUTPUT_FILE=plc_srtp_capture_%DATE:~-4,4%%DATE:~-10,2%%DATE:~-7,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%.pcapng
set OUTPUT_FILE=%OUTPUT_FILE: =0%

echo ============================================================
echo GE-SRTP Packet Capture
echo ============================================================
echo PLC IP:       %PLC_IP%
echo PLC Port:     %PLC_PORT%
echo Interface:    %INTERFACE%
echo Output File:  %OUTPUT_FILE%
echo.
echo Press Ctrl+C to stop capture
echo ============================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script requires Administrator privileges
    echo.
    echo Please run:
    echo   Right-click this batch file
    echo   Select "Run as administrator"
    pause
    exit /b 1
)

REM Start capture using dumpcap
"C:\Program Files\Wireshark\dumpcap.exe" ^
    -i "%INTERFACE%" ^
    -f "host %PLC_IP% and port %PLC_PORT%" ^
    -w "%OUTPUT_FILE%"

REM When stopped, show summary
echo.
echo ============================================================
echo Capture complete!
echo File saved: %OUTPUT_FILE%
echo.
echo To analyze:
echo   Open %OUTPUT_FILE% in Wireshark
echo ============================================================
pause
```

**Usage**:
1. Right-click → Run as administrator
2. Perform operations (KEPServerEX reads, Python tests, etc.)
3. Press Ctrl+C to stop
4. File saved with timestamp

---

## Next Steps

1. ✅ **Set up Wireshark** on Windows PC
2. ✅ **Configure KEPServerEX** with test tags
3. 🔬 **Capture symbolic tag reads** from KEPServerEX
4. 🔬 **Analyze packet structure** for symbolic addressing
5. 🔬 **Capture different data types** (INT, DINT, REAL, etc.)
6. 🔬 **Document findings** in protocol.md
7. 🔬 **Implement new features** based on discoveries
8. ⚠️ **Research write operations** (with extreme caution)

---

## Research Status

**Phase**: Investigation and Protocol Reverse Engineering

**Current Focus**:
1. Symbolic tag addressing via KEPServerEX packet analysis
2. Additional data type support (INT, DINT, REAL, STRING, etc.)
3. Write operation protocol understanding

**Resources**:
- KEPServerEX with GE Ethernet driver
- Wireshark for Windows
- Real Emerson PACSystems hardware
- Limited GE-SRTP documentation (trial and error approach)

**Safety**:
- READ operations: Safe, non-invasive ✅
- WRITE operations: DANGEROUS, extensive research required ⚠️

See `docs/todo.md` for detailed research roadmap.

---

**Last Updated**: 2025-10-17
**Status**: Research in Progress 🔬
**Environment**: Windows 10/11 with Wireshark and KEPServerEX
