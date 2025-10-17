# Symbolic Addressing Investigation - Research in Progress

**Date**: 2025-10-17 (Updated)
**Status**: 🔬 **ACTIVE RESEARCH - Windows Environment**
**Priority**: Active Investigation
**Environment**: Windows 10/11 with KEPServerEX and Wireshark

---

## Current Research Status (October 2025)

**Development Environment CHANGED**:
- ✅ **Windows PC**: Primary development environment (was Raspberry Pi)
- ✅ **KEPServerEX**: Installed with GE Ethernet driver
- ✅ **Wireshark**: Installed for packet capture
- ✅ **Test PLC**: Emerson PACSystems EPXCPE210 at 172.16.12.124:18245
- 🔬 **Active Investigation**: Using KEPServerEX traffic analysis to understand symbolic addressing

**Research Approach**: Trial and error with limited GE-SRTP documentation

---

## Executive Summary

Modern PACSystems (Emerson RX3i, formerly GE) support **symbolic/tag-based addressing** in addition to traditional memory addressing (%R, %Q, %I). This would allow reading variables by name (e.g., "Tank_Level") instead of by address (e.g., %R100).

**Current Driver Status**: ✅ Supports traditional addressing (%R, %AI, %AQ, %I, %Q, %M, %T, %S)
**Symbolic Support**: ❌ Not implemented - protocol unknown

**Key Resource**: KEPServerEX with GE Ethernet driver successfully reads symbolic tags from PLC. We can reverse-engineer the protocol by capturing KEPServerEX traffic with Wireshark.

---

## The Problem: Two Types of Addressing

### Traditional Addressing (Currently Supported ✅)

```python
# Direct memory addressing - what our driver does now
plc.read_register(100)           # Reads %R100
plc.read_analog_input(5)         # Reads %AI5
plc.read_discrete_output(12)     # Reads %Q12
```

**How it works**:
- Uses `READ_SYSTEM_MEMORY` service code (0x04)
- Specifies segment selector (0x08 for %R, 0x10 for %I, etc.)
- Specifies offset (address number)
- Reads from physical memory locations

### Symbolic Addressing (Not Supported ❌)

```python
# Tag-based addressing - would be much more user-friendly
plc.read_tag("Tank_Level")       # What is this? Where is it?
plc.read_tag("Pump_Running")     # Unknown protocol
plc.read_tag("Emergency_Stop")   # Need to discover how this works
```

**How it MIGHT work** (unknown):
- Could use a different service code (not 0x04)
- Could send tag name as ASCII string in payload
- Could use tag IDs from a symbol table
- Could be a completely different protocol (not GE-SRTP)

---

## Key Distinction: Symbolic Variables May Not Map to %R/%Q/%I

**Critical Understanding**:

Modern PACSystems symbolic variables may **NOT** correspond to traditional memory addresses at all:

- Symbolic variables like `Tank_Level` might be allocated by the compiler in optimized program memory
- They might not be in %R/%Q/%I segments
- They might only be accessible through symbolic lookup
- Traditional `READ_SYSTEM_MEMORY` (service 0x04) might not work for them

**Example**:
```
Traditional Variable:  %R00100 = 12345    ← Our driver can read this ✓
Symbolic Variable:     MyVariable = 67890  ← Our driver CANNOT read this ✗
```

The symbolic variable might exist in compiler-allocated memory that isn't accessible via segment selectors.

---

## Why Symbolic Addressing Would Be Valuable

### Current Approach (Requires Documentation)
```python
# Code is not self-documenting
value1 = plc.read_register(100)      # What is this?
value2 = plc.read_analog_input(5)    # What sensor?
value3 = plc.read_discrete_output(12)  # What equipment?

# Need external documentation to understand:
# %R100 = Tank level
# %AI5 = Temperature sensor
# %Q12 = Cooling pump
```

### With Symbolic Support (Self-Documenting)
```python
# Code is immediately clear
tank_level = plc.read_tag("Tank_Level")
temperature = plc.read_tag("Temperature_Sensor")
pump_status = plc.read_tag("Cooling_Pump")

# No external documentation needed!
```

**Benefits**:
- ✅ Self-documenting code
- ✅ Matches how engineers think about their programs
- ✅ No need to maintain address mapping tables
- ✅ Industry standard approach (all modern SCADA systems)
- ✅ Resilient to program changes (addresses might change, tag names don't)

---

## Investigation Strategy: Reverse Engineer KEPServerEX

**Key Asset**: KEPServerEX with GE Ethernet driver successfully reads symbolic tags from this PLC.

Since KEPServerEX knows how to do it, we can **watch what it does** and replicate it!

### Phase 1: Identify the Protocol

**Goal**: Determine if KEPServerEX uses GE-SRTP or a different protocol.

**Method**: Check KEPServerEX configuration
1. Open KEPServerEX configuration
2. Look at the channel/device driver being used
3. Check what protocol it shows:
   - "GE Ethernet Global Data"?
   - "GE SRTP"?
   - "GE EGD"?
   - "EtherNet/IP"?
   - "PROFINET"?

**Why this matters**:
- If KEPServerEX uses GE-SRTP → We can extend our existing driver
- If KEPServerEX uses EtherNet/IP → We'd need to implement a different protocol
- Different protocols have completely different packet structures

### Phase 2: Capture KEPServerEX Traffic with Wireshark (Windows)

**Setup**: Windows PC with Wireshark and KEPServerEX

**Method 1 - Wireshark GUI** (Recommended):
1. Run Wireshark as Administrator
2. Select network interface connected to PLC
3. Set capture filter: `host 172.16.12.124 and port 18245`
4. Start capture
5. Operate KEPServerEX (read tags)
6. Stop and save as `kepserver_symbolic.pcapng`

**Method 2 - Command Line**:
```batch
REM Run as Administrator
"C:\Program Files\Wireshark\dumpcap.exe" ^
  -i "Ethernet" ^
  -f "host 172.16.12.124 and port 18245" ^
  -w kepserver_symbolic.pcapng
```

Or use the included `start_wireshark_capture.bat` script

**What to capture**:
1. KEPServerEX connecting to PLC (initialization sequence)
2. KEPServerEX reading 2-3 symbolic tags
3. KEPServerEX reading 1-2 traditional tags (%R) for comparison
4. Any periodic traffic (symbol table updates?)

**Duration**: 30-60 seconds should be sufficient

**See `docs/wireshark.md` for detailed Windows capture instructions**

### Phase 3: Analyze the Packets

**Tools** (Windows):
```batch
REM Open in Wireshark GUI
"C:\Program Files\Wireshark\Wireshark.exe" kepserver_symbolic.pcapng

REM Or use tshark command line
"C:\Program Files\Wireshark\tshark.exe" -r kepserver_symbolic.pcapng

REM Filter by port
"C:\Program Files\Wireshark\tshark.exe" -r kepserver_symbolic.pcapng -Y "tcp.port == 18245"
```

**What to look for**:

1. **Destination Port**:
   - Port 18245 → GE-SRTP (same as our driver)
   - Port 44818 → EtherNet/IP (different protocol)
   - Port 502 → Modbus TCP (different protocol)

2. **Packet Structure** (if port 18245):
   - Does it use 56-byte header? (like our driver)
   - Byte 30: Service code - is it 0x04 or something else?
   - Byte 31: Segment selector - what value?
   - Payload: Look for ASCII tag names

3. **Symbol Table Download**:
   - Large data transfer after connection?
   - KEPServerEX might download entire symbol table at startup
   - Would show as many packets with lots of data

4. **Tag Name Encoding**:
   - Search for ASCII text in payloads
   - Tag names might be null-terminated strings
   - Or might be encoded as tag IDs (integers)

5. **Comparison: Symbolic vs Traditional**:
   - Do symbolic reads use different service codes?
   - Do symbolic reads include tag names in payload?
   - Are responses formatted differently?

### Phase 4: Decode the Protocol

**If GE-SRTP (port 18245)**:

Compare KEPServerEX packets to our driver packets:

**Our Current READ_REGISTER Packet** (known working):
```
Bytes 30-31: 0x04 0x08 (service=READ_SYSTEM_MEMORY, selector=REGISTERS)
Bytes 32-35: address offset (little-endian)
Bytes 36-39: 0x20 0x0E 0x00 0x00 (slot 2 mailbox)
Payload: (empty for reads)
```

**KEPServerEX Symbolic Read Packet** (to discover):
```
Bytes 30-31: 0x?? 0x?? (different service code?)
Bytes 32-35: ??? (tag ID? or zero?)
Bytes 36-39: 0x20 0x0E 0x00 0x00 (same mailbox?)
Payload: "Tank_Level\0" (tag name as ASCII?)
```

**Questions to answer**:
- What service code does KEPServerEX use for symbolic reads?
- Is the tag name in the payload?
- How long are tag names? (null-terminated? length-prefixed?)
- Are there tag IDs or is it purely name-based?
- What does the response look like?

**If EtherNet/IP (port 44818)**:
- This is a completely different protocol (CIP)
- Would require implementing EtherNet/IP client
- More complex but well-documented standard
- Many Python libraries exist (pycomm3, cpppo)

---

## Implementation Approaches (After Protocol Discovery)

Once we know how symbolic addressing works, three implementation paths:

### Approach 1: Pure Symbolic Read (If Protocol Supports It)

**If KEPServerEX shows a symbolic read service code**:

```python
# New method in driver.py
def read_symbolic(self, tag_name: str):
    """
    Read a variable by symbolic tag name.
    Uses symbolic read service (to be discovered).
    """
    response = self._send_request_and_receive(
        service_code=0x??,  # Discovered from KEPServerEX
        segment_selector=0x??,
        data_offset=0,
        data_length=0,
        payload=tag_name.encode('ascii') + b'\0'  # Tag name
    )
    return response.extract_word_values(1)[0]
```

**Pros**: Direct, clean, efficient
**Cons**: Requires discovering the protocol

### Approach 2: Symbol Table Download + Local Resolution

**If KEPServerEX downloads a symbol table at connection**:

```python
# New method in driver.py
def download_symbol_table(self):
    """
    Download the complete symbol table from PLC.
    Called once at connection.
    """
    response = self._send_request_and_receive(
        service_code=0x??,  # Symbol table service
        segment_selector=0x??,
        data_offset=0,
        data_length=0
    )
    # Parse response into tag database
    self._symbol_table = self._parse_symbol_table(response)
    # Returns: {"Tank_Level": {"type": "R", "address": 100, ...}, ...}

def read_tag(self, tag_name: str):
    """
    Read using symbolic name by resolving to address.
    """
    if tag_name not in self._symbol_table:
        raise ValueError(f"Tag '{tag_name}' not found")

    tag_info = self._symbol_table[tag_name]

    # Route to traditional read based on memory type
    if tag_info['type'] == 'R':
        return self.read_register(tag_info['address'])
    elif tag_info['type'] == 'AI':
        return self.read_analog_input(tag_info['address'])
    # ... etc
```

**Pros**: Fast reads after initial download, uses existing read methods
**Cons**: Requires parsing symbol table format

### Approach 3: Manual Tag Database (Fallback - No Protocol Discovery Needed)

**If protocol is too complex or proprietary**:

```python
# Simple implementation using external mapping
class GE_SRTP_Driver:
    def __init__(self, host, port=18245, slot=1):
        # ... existing code ...
        self._tag_database = {}

    def load_tags_from_csv(self, csv_file: str):
        """
        Load tag definitions from CSV file.
        Format: TagName,Type,Address,DataType,Description
        """
        import csv
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self._tag_database[row['TagName']] = {
                    'type': row['Type'],
                    'address': int(row['Address']),
                    'data_type': row['DataType']
                }

    def define_tag(self, name: str, memory_type: str, address: int):
        """Manually define a tag."""
        self._tag_database[name] = {
            'type': memory_type,
            'address': address
        }

    def read_tag(self, name: str):
        """Read using tag name from local database."""
        if name not in self._tag_database:
            raise ValueError(f"Tag '{name}' not defined")

        tag = self._tag_database[name]

        # Route to appropriate read method
        if tag['type'] == 'R':
            return self.read_register(tag['address'])
        elif tag['type'] == 'AI':
            return self.read_analog_input(tag['address'])
        elif tag['type'] == 'Q':
            return self.read_discrete_output(tag['address'], mode='bit')
        # ... etc

# Usage:
plc = GE_SRTP_Driver('172.16.12.124', slot=0)
plc.connect()

# Option 1: Load from CSV export
plc.load_tags_from_csv('plc_tags.csv')

# Option 2: Define manually
plc.define_tag("Tank_Level", "R", 100)
plc.define_tag("Pump_Running", "Q", 12)

# Read by name
level = plc.read_tag("Tank_Level")
pump = plc.read_tag("Pump_Running")
```

**Pros**:
- Easy to implement (~50 lines of code)
- No protocol research needed
- Works with existing driver
- User provides the mapping

**Cons**:
- Requires external tag database
- Not automatic
- Must be kept in sync with PLC program

**CSV Format Example**:
```csv
TagName,Type,Address,DataType,Description
Tank_Level,R,100,INT,Main tank level sensor
Pump_Running,Q,12,BOOL,Cooling pump status
Inlet_Valve,Q,13,BOOL,Main inlet valve control
Temperature,AI,5,INT,Temperature sensor reading
```

This could be exported from PAC Machine Edition or KEPServerEX.

---

## Research Questions to Answer

### Protocol Questions
1. ❓ What protocol does KEPServerEX use? (GE-SRTP? EtherNet/IP? Other?)
2. ❓ What port does KEPServerEX connect to? (18245? 44818? Other?)
3. ❓ Does KEPServerEX use the same initialization sequence as our driver?

### Symbolic Read Questions
4. ❓ What service code is used for symbolic reads?
5. ❓ How are tag names encoded in packets? (ASCII? UTF-8? Tag IDs?)
6. ❓ Are tag names sent with each read, or resolved once at connection?
7. ❓ What is the maximum tag name length?

### Symbol Table Questions
8. ❓ Does KEPServerEX download a symbol table at connection?
9. ❓ If yes, what service code retrieves the symbol table?
10. ❓ How is the symbol table formatted in the response?
11. ❓ Does the symbol table include data types, addresses, descriptions?

### Addressing Questions
12. ❓ Do symbolic variables map to traditional %R/%Q/%I addresses?
13. ❓ Or are they in separate compiler-allocated memory?
14. ❓ Can symbolic variables be read using traditional READ_SYSTEM_MEMORY?

---

## Test Plan (When Ready to Implement)

### Test Setup
1. PLC with both traditional and symbolic variables defined
2. KEPServerEX successfully reading both types
3. Packet capture ready on Windows PC

### Test Cases

**Test 1: Identify Protocol**
- Capture KEPServerEX connection initialization
- Verify port number and packet structure
- Compare to our driver's packets

**Test 2: Symbolic Read Packet Analysis**
- Capture KEPServerEX reading symbolic tag "Tank_Level"
- Identify service code, selector, payload format
- Document exact packet structure

**Test 3: Traditional Read Comparison**
- Capture KEPServerEX reading %R100
- Compare to symbolic read packet
- Identify differences

**Test 4: Symbol Table Discovery**
- Capture KEPServerEX connecting to fresh PLC
- Look for large data transfer
- Analyze symbol table format if present

**Test 5: Replication**
- Implement discovered protocol in our driver
- Test reading same symbolic tag
- Verify we get same value as KEPServerEX

---

## Current Status & Next Steps

### ✅ What We Have Now
- Complete GE-SRTP driver for traditional addressing
- All memory types working (%R, %AI, %AQ, %I, %Q, %M, %T, %S)
- Verified on real PACSystems hardware (EPXCPE210)
- Production-ready for direct addressing

### ❌ What We Don't Have
- No symbolic addressing support
- Unknown protocol for symbolic reads
- No documentation on GE symbolic addressing

### 🔬 Investigation Resources
- ✅ KEPServerEX with GE Ethernet driver successfully reading symbolic tags
- ✅ Wireshark installed on Windows PC
- ✅ Network access to capture traffic
- ✅ Real PLC hardware for testing (Emerson PACSystems EPXCPE210 at 172.16.12.124)

### 📋 Recommended Next Steps

**Step 1: Gather Information** (15 minutes)
- [ ] Check KEPServerEX configuration - what driver/protocol is it using?
- [ ] List 2-3 symbolic tag names that exist in the PLC program
- [ ] Check if tags are purely symbolic or also have %R addresses

**Step 2: Capture Traffic** (30 minutes)
- [ ] Start Wireshark capture on Windows PC
- [ ] KEPServerEX: Read 2-3 symbolic tags using OPC Quick Client
- [ ] KEPServerEX: Read 1-2 traditional tags (%R) for comparison
- [ ] Stop capture and save pcapng file

**Step 3: Analyze Packets** (1-2 hours)
- [ ] Identify protocol and port number
- [ ] Find service codes for symbolic operations
- [ ] Document packet structure
- [ ] Determine if symbol table is downloaded

**Step 4: Prototype** (2-4 hours)
- [ ] Implement discovered protocol in test script
- [ ] Verify we can replicate KEPServerEX's reads
- [ ] Integrate into main driver

**Step 5: Document** (1 hour)
- [ ] Update this document with findings
- [ ] Create protocol specification for symbolic reads
- [ ] Add examples to README

---

## Alternative: Manual Tag Database (Quick Win)

**If protocol research is too time-consuming**, we can implement Approach 3 (manual tag database) in ~30 minutes:

```python
# Quick implementation - no protocol discovery needed!
plc.define_tag("Tank_Level", "R", 100)
plc.define_tag("Pump_Running", "Q", 12)

level = plc.read_tag("Tank_Level")  # Works immediately!
```

This provides 80% of the benefits with 20% of the effort, and can be upgraded later once we understand the protocol.

---

## References

### Existing Documentation
- `FINAL_SUCCESS_SUMMARY.md` - Current driver capabilities
- `RX3i_MINIMUM_LENGTH_DISCOVERY.md` - Protocol discoveries
- `MULTI_PACKET_DISCOVERY.md` - TCP response handling
- `SLOT_ADDRESSING_FINDINGS.md` - Mailbox addressing

### External Resources
- KEPServerEX with GE Ethernet driver - Working symbolic read implementation
- PAC Machine Edition (optional) - PLC programming environment
- Wireshark for Windows - Packet capture and analysis tool

### PLC Hardware
- **Current**: Emerson PACSystems EPXCPE210 (Firmware 10.30)
  - IP: 172.16.12.124, Port: 18245
  - CPU Slot: 0
- **Previous**: Emerson RX3i IC695CPE330 (Firmware 10.85)
  - IP: 172.16.12.127, Port: 18245
  - CPU Slot: 2

---

## Notes

- This is **active research**, part of protocol reverse engineering effort
- Current driver is **production-ready** for traditional addressing
- Symbolic support would improve usability significantly
- **Trial and error approach** due to limited GE-SRTP documentation
- Using KEPServerEX as reference implementation

---

**Status**: 🔬 **ACTIVE RESEARCH**
**Priority**: Active Investigation
**Effort**: Medium-High (trial and error with KEPServerEX packet analysis)
**Value**: High (Much better user experience)
**Approach**: Reverse engineering via packet capture

---

**Last Updated**: 2025-10-17
**Environment**: Windows 10/11 with KEPServerEX and Wireshark
**Next Action**: Capture KEPServerEX traffic to identify symbolic read protocol
**See Also**: `docs/wireshark.md` for detailed capture procedures
