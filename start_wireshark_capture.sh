#!/bin/bash
#
# Wireshark Packet Capture Script for GE-SRTP Testing
#
# This script captures all SRTP traffic to/from the PLC
#

# Configuration
PLC_IP="172.16.12.127"
PLC_PORT="18245"
INTERFACE="wlan0"  # WiFi interface on Raspberry Pi
OUTPUT_FILE="plc_srtp_capture.pcap"

echo "============================================================"
echo "GE-SRTP Packet Capture"
echo "============================================================"
echo "PLC IP:       $PLC_IP"
echo "PLC Port:     $PLC_PORT"
echo "Interface:    $INTERFACE"
echo "Output File:  $OUTPUT_FILE"
echo ""
echo "Press Ctrl+C to stop capture"
echo "============================================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "⚠ This script requires sudo/root privileges for packet capture"
    echo ""
    echo "Please run:"
    echo "  sudo bash $0"
    exit 1
fi

# Start capture
tshark -i $INTERFACE \
    -f "host $PLC_IP and port $PLC_PORT" \
    -w $OUTPUT_FILE \
    -P

# When stopped, show summary
echo ""
echo "============================================================"
echo "Capture complete!"
echo "File saved: $OUTPUT_FILE"
echo ""
echo "To analyze:"
echo "  tshark -r $OUTPUT_FILE -V"
echo "  or transfer to PC and open in Wireshark GUI"
echo "============================================================"
