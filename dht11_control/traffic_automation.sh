#!/bin/bash

# Variables
PCAP_FILE="/home/pi/dht11_control/pcap_files/traffic.pcap"  # Path to save captured pcap file
CONN_LOG="/home/pi/dht11_control/live_traffic_conn.log"     # Final conn.log path
ZEEX_BIN="/opt/zeek/bin/zeek"                              # Path to Zeek binary
LOGFILE="/home/pi/dht11_control/traffic_automation.log"     # Script log file

# Start traffic capture
echo "$(date): Starting traffic capture..." >> "$LOGFILE"
sudo timeout 30 tcpdump -i wlan0 -w "$PCAP_FILE"

# Check if the PCAP file was created
if [ -f "$PCAP_FILE" ]; then
    echo "$(date): Traffic capture complete. Converting to Zeek logs..." >> "$LOGFILE"
    
    # Process the PCAP file with Zeek
    $ZEEX_BIN -r "$PCAP_FILE"

    # Check if conn.log was generated
    if [ -f "conn.log" ]; then
        mv conn.log "$CONN_LOG"
        echo "$(date): conn.log saved to $CONN_LOG" >> "$LOGFILE"
    else
        echo "$(date): Error: conn.log was not generated." >> "$LOGFILE"
    fi
else
    echo "$(date): Error: PCAP file was not created." >> "$LOGFILE"
fi
