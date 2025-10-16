# Wireshark Packet Capture Guide for GE-SRTP Debugging

## Objective
Capture and analyze GE-SRTP packets to understand discrete I/O behavior on the RX3i PLC.

---

## Prerequisites

1. **Wireshark/tcpdump installed** on Raspberry Pi
2. **Network interface** connected to PLC (172.16.12.127)
3. **PAC Machine Edition v10.6** access from separate PC
4. **Root/sudo access** for packet capture

---

## Method 1: Using tcpdump (Command Line)

### Step 1: Find Network Interface

```bash
ip addr show
# or
ifconfig
```

Look for the interface connected to the PLC network (probably `eth0` or similar).

### Step 2: Start Packet Capture

```bash
# Capture SRTP traffic to/from PLC and save to file
sudo tcpdump -i eth0 -w /home/jobeastwood/Desktop/plc_project/plc_capture.pcap \
  host 172.16.12.127 and port 18245
```

Leave this running, then proceed to Step 3.

### Step 3: Run Test Script

In another terminal:
```bash
cd /home/jobeastwood/Desktop/plc_project
python3 test_discrete_wireshark.py
```

### Step 4: Stop Capture

Return to tcpdump terminal and press `Ctrl+C`.

### Step 5: Analyze Capture

Transfer `plc_capture.pcap` to a PC with Wireshark GUI, or use:
```bash
tcpdump -r plc_capture.pcap -X
```

---

## Method 2: Using Wireshark GUI (If Installed)

### Step 1: Install Wireshark (requires sudo)

```bash
sudo apt-get update
sudo apt-get install wireshark
sudo usermod -a -G wireshark $USER
# Log out and back in for group change to take effect
```

### Step 2: Start Wireshark

```bash
wireshark &
```

### Step 3: Configure Capture

1. Select network interface (eth0 or similar)
2. Set filter: `ip.addr == 172.16.12.127 && tcp.port == 18245`
3. Click "Start Capturing"

### Step 4: Run Tests

```bash
python3 test_discrete_wireshark.py
```

### Step 5: Stop and Save

1. Stop capture in Wireshark
2. Save as: `plc_discrete_capture.pcapng`

---

## What to Look For in Captures

### Request Packet Structure

**Expected 56-byte request**:
```
Byte 0:     0x02 (Request packet type)
Byte 2/30:  Sequence number
Byte 4:     0x00 (no payload in request)
Byte 31:    0xC0 (Message type: SERVICE_REQUEST)
Bytes 36-39: 0x20 0x0E 0x00 0x00 (Mailbox dest - slot 2)
Byte 42:    0x04 (Service code: READ_SYSTEM_MEMORY)
Byte 43:    Segment selector (THIS IS KEY!)
Bytes 44-45: Data offset (little-endian)
Bytes 46-47: Data length (little-endian)
```

### Response Packet Structure

**For successful read**:
```
Byte 0:     0x03 (Response packet type)
Byte 2/30:  Sequence number (matches request)
Byte 4:     Payload length (0 = empty, >0 = has data)
Byte 31:    0x94 (ACK_WITH_DATA) or 0xD4 (ACK_NO_DATA)
```

### Segment Selectors to Verify

| Memory | Mode | Selector (Hex) | Expected |
|--------|------|----------------|----------|
| %I (Discrete Input) | bit | 0x46 | Discrete input bits |
| %I (Discrete Input) | byte | 0x10 | Discrete input bytes |
| %Q (Discrete Output) | bit | 0x48 | Discrete output bits |
| %Q (Discrete Output) | byte | 0x12 | Discrete output bytes |
| %M (Internal) | byte | 0x16 | Internal memory bytes |
| %T (Temp) | byte | 0x18 | Temporary memory bytes |

### Critical Questions to Answer

1. **Does byte 4 in response = 0?** → PLC has no data to send
2. **Is byte 31 = 0xD4 (ACK) or 0xD1 (ERROR)?** → Request acknowledged or rejected?
3. **Do segment selectors match protocol spec?** → Are we using correct selectors?
4. **Is mailbox destination = 0x20 0x0E 0x00 0x00?** → Slot 2 addressing correct?

---

## Test Scenarios

### Scenario 1: Register Read (Known Working)

**Purpose**: Verify baseline - we know this works

**Test**:
```python
plc.read_register(0)  # %R1
```

**Expected Response**:
- Byte 4 = 0x08 (8-byte payload)
- Byte 31 = 0x94 (ACK_WITH_DATA)
- Payload = 2 words (4 bytes) of data

### Scenario 2: Discrete Input - Byte Mode

**Test**:
```python
plc.read_discrete_input(0, count=4, mode='byte')
```

**Request Should Have**:
- Byte 42 = 0x04 (READ_SYSTEM_MEMORY)
- Byte 43 = 0x10 (DISCRETE_INPUTS_BYTE selector)
- Bytes 46-47 = 0x04 0x00 (4 bytes requested)

**Check Response**:
- Byte 4 = ? (payload length)
- Byte 31 = 0xD4 or 0x94 or 0xD1?

### Scenario 3: Discrete Input - Bit Mode

**Test**:
```python
plc.read_discrete_input(0, count=32, mode='bit')
```

**Request Should Have**:
- Byte 43 = 0x46 (DISCRETE_INPUTS_BIT selector)
- Bytes 46-47 = 0x20 0x00 (32 bits requested)

### Scenario 4: Try Alternative Selectors

Some RX3i models might use different selectors. Test variations:

**Alternative byte selectors**:
- 0x70 (some models use this for %I byte)
- 0x72 (alternative %Q byte)

---

## Preparing the PLC (PAC Machine Edition)

### Option 1: Configure Simulated Discrete I/O

If your RX3i supports internal simulation:

1. **Open PAC Machine Edition v10.6**
2. **Connect to PLC** (172.16.12.127)
3. **Hardware Configuration**:
   - Check if discrete I/O modules are configured
   - Note which slots have I/O modules
   - Note I/O address ranges

4. **Program Simple Ladder Logic**:
```
|----[%I0001]----( %Q0001 )
|
|----[%M0001]----( %M0002 )
```

5. **Force Some Values**:
   - Force %I0001 = 1
   - Force %M0001 = 1
   - This creates known data to read

6. **Download and Run**

### Option 2: Check What's Actually Configured

1. **Open Hardware Configuration** in PAC Machine Edition
2. **View Rack Configuration**:
   - Slot 0: Power Supply
   - Slot 2: CPU
   - Slot 3+: What modules are here?

3. **Check I/O Assignment**:
   - Are %I addresses assigned?
   - Are %Q addresses assigned?
   - What ranges are valid?

4. **Export Configuration**:
   - Save configuration to file
   - We can analyze what's actually available

---

## Interpreting Results

### Case 1: Response has data (byte 4 > 0)
**Conclusion**: Discrete I/O IS available, driver works!

### Case 2: Response byte 31 = 0xD1 (ERROR)
**Possible causes**:
- Invalid segment selector
- Invalid address range
- Memory type not supported

### Case 3: Response byte 31 = 0xD4, byte 4 = 0 (ACK, no data)
**Possible causes**:
- Memory exists but is uninitialized
- Address out of range
- No I/O modules configured

### Case 4: No response at all
**Possible causes**:
- Wrong slot number
- Network issue
- PLC not responding

---

## Advanced Analysis

### Compare Register Read vs Discrete Read

Capture both and compare side-by-side:

**Register Read (Working)**:
```
Request:  02 00 XX ... 04 08 00 00 04 00  (service=0x04, selector=0x08, len=4)
Response: 03 00 XX ... 94 ... [8 bytes payload]
```

**Discrete Read (Not Working)**:
```
Request:  02 00 XX ... 04 10 00 00 04 00  (service=0x04, selector=0x10, len=4)
Response: 03 00 XX ... D4 ... [0 bytes payload]
```

**Question**: Why does 0x08 work but 0x10 doesn't?

### Check GE Documentation

If we find the response is an error (0xD1), we need to check:
1. RX3i-specific segment selectors (may differ from Series 90-30)
2. Firmware-specific protocol variations
3. Module-specific addressing requirements

---

## Output Files

After capture, we'll have:
1. **plc_capture.pcap** - Raw packet capture
2. **Analysis report** - What we learned
3. **Updated driver** - If we discover correct selectors

---

## Timeline

1. **5 minutes**: User starts packet capture
2. **2 minutes**: Run test script
3. **5 minutes**: Analyze capture
4. **10 minutes**: Adjust driver if needed
5. **2 minutes**: Re-test with fixes

**Total**: ~25 minutes to full discrete I/O support (if possible)

---

**Ready to proceed?**
1. User: Start Wireshark/tcpdump
2. User: Run `python3 test_discrete_wireshark.py`
3. User: Check PAC Machine Edition for actual I/O config
4. We: Analyze results together

