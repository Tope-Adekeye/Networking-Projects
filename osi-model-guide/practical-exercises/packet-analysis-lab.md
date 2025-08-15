# OSI Model Packet Analysis Laboratory

## 🎯 **Objective**
This hands-on laboratory demonstrates how network packets traverse the OSI model layers, providing practical experience with protocol analysis and network troubleshooting.

## 🧪 **Lab Setup Requirements**

### **Software Tools**
- **Wireshark**: Network protocol analyzer
- **tcpdump**: Command-line packet capture
- **Nmap**: Network scanning and discovery
- **Netcat**: Network connection utility
- **ping/traceroute**: Network connectivity testing

### **Network Environment**
- **Physical**: Two computers connected via switch/router
- **Virtual**: VM network with bridged/NAT configuration
- **Cloud**: AWS/Azure lab environment with security groups
- **Simulated**: GNS3 or Packet Tracer topology

## 📊 **Exercise 1: Web Traffic Analysis**

### **Scenario**: HTTP Request Analysis
Analyze the complete OSI stack for a simple web request.

### **Setup Commands**
```bash
# Start packet capture
sudo tcpdump -i eth0 -w web_traffic.pcap

# Alternative with Wireshark
wireshark -i eth0 -k &

# Generate HTTP traffic
curl -v http://www.example.com/index.html

# Stop capture after response
```

### **Analysis Tasks**

#### **Layer 1 (Physical)**
```
Observation Points:
□ Network interface status: ip link show eth0
□ Link speed and duplex: ethtool eth0
□ Signal quality (WiFi): iwconfig wlan0
□ Cable connectivity: Physical LED indicators

Documentation:
- Interface: ________________
- Speed/Duplex: _____________
- Physical medium: __________
```

#### **Layer 2 (Data Link)**
```bash
# Wireshark filter for Ethernet frames
eth.dst == your_gateway_mac

Analysis Tasks:
□ Source MAC address identification
□ Destination MAC address (gateway)
□ Frame type field (0x0800 for IPv4)
□ Frame check sequence validation

Frame Structure:
Destination MAC: _______________
Source MAC: ___________________
EtherType: ____________________
Frame Size: ___________________
```

#### **Layer 3 (Network)**
```bash
# Wireshark filter for IP packets
ip.dst == target_ip_address

Analysis Tasks:
□ IP version and header length
□ Source and destination IP addresses
□ Time to Live (TTL) value
□ Protocol field (6 for TCP)
□ IP fragmentation flags

IP Header Analysis:
Version: _______  Header Length: _______
Source IP: ____________________________
Destination IP: _______________________
TTL: __________  Protocol: ____________
```

#### **Layer 4 (Transport)**
```bash
# Wireshark filter for TCP
tcp.port == 80

Analysis Tasks:
□ TCP three-way handshake observation
□ Source and destination port numbers
□ Sequence and acknowledgment numbers
□ TCP flags (SYN, ACK, FIN, RST)
□ Window size and scaling

TCP Analysis:
Source Port: _______ Dest Port: _______
Sequence Number: ____________________
Acknowledgment: _____________________
Flags: _____________________________
Window Size: _______________________
```

#### **Layer 5-7 (Session/Presentation/Application)**
```bash
# Wireshark filter for HTTP
http

Analysis Tasks:
□ HTTP request method and URI
□ HTTP headers and user agent
□ Content encoding and compression
□ Response status code
□ Session cookies (if any)

HTTP Analysis:
Method: ____________________________
Host: ______________________________
User-Agent: _______________________
Accept-Encoding: __________________
Response Code: ____________________
```

## 📊 **Exercise 2: DNS Resolution Deep Dive**

### **Scenario**: DNS Query Analysis
Examine DNS resolution across OSI layers.

### **Setup**
```bash
# Clear DNS cache
sudo systemctl flush-dns  # or equivalent

# Capture DNS traffic
sudo tcpdump -i eth0 port 53 -v

# Perform DNS lookup
nslookup www.github.com
```

### **Analysis Framework**

#### **Layer 3 Analysis**
```
DNS Query Path:
Client IP: _________________________
DNS Server IP: ____________________
TTL values: _______________________
Fragmentation: ____________________
```

#### **Layer 4 Analysis**
```
Transport Protocol: UDP (typically)
Source Port: ______________________
Destination Port: 53 (DNS)
Query ID: _________________________
```

#### **Layer 7 Analysis**
```
DNS Query:
Question Type: ____________________
Query Name: _______________________
Query Class: ______________________

DNS Response:
Answer Records: ___________________
Authority Records: ________________
Additional Records: _______________
Response Code: ____________________
```

## 📊 **Exercise 3: Secure Connection Analysis**

### **Scenario**: HTTPS/TLS Connection
Analyze encrypted web traffic establishment.

### **Setup**
```bash
# Capture HTTPS traffic
sudo tcpdump -i eth0 port 443 -w https_capture.pcap

# Generate HTTPS traffic
curl -v https://www.google.com

# Analyze with tshark
tshark -r https_capture.pcap -V
```

### **TLS Handshake Analysis**

#### **Client Hello**
```
TLS Version: ______________________
Cipher Suites: ____________________
Extensions: _______________________
Server Name Indication: ___________
```

#### **Server Hello**
```
Selected Cipher Suite: ____________
Certificate Chain: ________________
Key Exchange Method: ______________
```

#### **Application Data**
```
Encrypted Content: ________________
Record Layer Protocol: ____________
Content Type: _____________________
```

## 📊 **Exercise 4: Network Troubleshooting Scenario**

### **Problem Statement**
Users report intermittent connectivity issues to internal web server.

### **Systematic OSI Troubleshooting**

#### **Layer 1 Verification**
```bash
# Check physical connectivity
ethtool eth0
ip link show

# Cable testing commands
sudo ethtool -t eth0 online

Checklist:
□ Link status: Up/Down
□ Speed negotiation: _____________
□ Duplex mismatch: ______________
□ Error counters: _______________
```

#### **Layer 2 Verification**
```bash
# Check ARP table
arp -a
ip neigh show

# Monitor for errors
ethtool -S eth0 | grep -i error

Checklist:
□ ARP resolution working: ________
□ MAC address conflicts: ________
□ Switch port errors: ___________
□ VLAN configuration: ___________
```

#### **Layer 3 Verification**
```bash
# Test IP connectivity
ping target_server
traceroute target_server

# Check routing table
ip route show
route -n

Checklist:
□ IP reachability: ______________
□ Routing table correct: ________
□ Default gateway: ______________
□ Subnet configuration: _________
```

#### **Layer 4 Verification**
```bash
# Test port connectivity
telnet target_server 80
nc -zv target_server 80

# Check listening ports
netstat -tuln
ss -tuln

Checklist:
□ Service listening: ____________
□ Port accessibility: __________
□ Firewall rules: ______________
□ NAT configuration: ___________
```

#### **Layer 7 Verification**
```bash
# Test application layer
curl -I http://target_server
wget --spider http://target_server

Checklist:
□ HTTP response codes: __________
□ Service availability: ________
□ Application errors: __________
□ Performance issues: __________
```

## 📈 **Performance Analysis**

### **Latency Analysis by Layer**
```bash
# Layer 1: Physical propagation delay
# Speed of light in medium: ~200,000 km/s in copper

# Layer 2: Frame processing delay
# Switch forwarding delay: ~10-50 microseconds

# Layer 3: Routing delay
# Router processing: ~100 microseconds to several milliseconds

# Layer 4: Protocol overhead
# TCP handshake: 1.5 × RTT

# Application: Processing time
# Server response time varies by application
```

### **Throughput Analysis**
```bash
# Test bandwidth at different layers
iperf3 -c target_server -p 5201

# Layer 2 throughput (theoretical)
# Gigabit Ethernet: 1000 Mbps
# Overhead: ~4% (preamble, IFG, FCS)

# Layer 3 throughput
# IP overhead: 20 bytes per packet
# Efficiency depends on packet size

# Layer 4 throughput
# TCP overhead: 20 bytes per segment
# Window scaling and congestion control impact
```

## 🔍 **Advanced Analysis Techniques**

### **Protocol Dissection**
```bash
# Extract specific protocol information
tshark -r capture.pcap -T fields -e frame.number -e ip.src -e ip.dst -e tcp.port

# Follow TCP streams
tshark -r capture.pcap -z follow,tcp,ascii,0

# Generate protocol statistics
tshark -r capture.pcap -z prot,colinfo
```

### **Traffic Pattern Analysis**
```bash
# Conversation analysis
tshark -r capture.pcap -z conv,ip

# I/O graph generation
tshark -r capture.pcap -z io,phs

# Expert info analysis
tshark -r capture.pcap -z expert
```

## 📝 **Lab Report Template**

### **Executive Summary**
- Objective of analysis
- Key findings
- Recommendations

### **Methodology**
- Tools used
- Capture procedures
- Analysis techniques

### **Layer-by-Layer Analysis**
```
Layer 1 (Physical):
- Medium type: ____________________
- Speed/Duplex: ___________________
- Physical issues: ________________

Layer 2 (Data Link):
- Frame analysis: __________________
- Error detection: _________________
- Switching behavior: ______________

Layer 3 (Network):
- Routing analysis: ________________
- IP configuration: _______________
- Path determination: ______________

Layer 4 (Transport):
- Protocol analysis: ______________
- Connection management: ___________
- Error recovery: __________________

Layers 5-7 (Application):
- Protocol identification: ________
- Data analysis: ___________________
- Performance metrics: _____________
```

### **Troubleshooting Results**
- Problem identification
- Root cause analysis
- Resolution steps
- Verification procedures

### **Performance Metrics**
- Latency measurements
- Throughput analysis
- Error rates
- Utilization statistics

## 🎓 **Learning Outcomes**

Upon completion of this laboratory, you should be able to:

□ **Capture and analyze network traffic** using industry-standard tools
□ **Identify protocols** operating at each OSI layer
□ **Troubleshoot network issues** systematically across all layers
□ **Interpret packet headers** and understand their significance
□ **Measure network performance** and identify bottlenecks
□ **Document findings** in professional technical reports

## 🔄 **Follow-Up Exercises**

### **Advanced Scenarios**
1. **VoIP Call Analysis**: RTP/RTCP stream examination
2. **VPN Traffic**: IPSec/SSL VPN protocol analysis
3. **Wireless Security**: 802.11 frame analysis and security
4. **Network Attack Simulation**: Protocol exploitation techniques
5. **Quality of Service**: Traffic prioritization analysis

### **Automation Opportunities**
```bash
# Automated capture and analysis script
#!/bin/bash
INTERFACE="eth0"
DURATION="300"  # 5 minutes
OUTPUT_DIR="/tmp/network_analysis"

# Start capture
tcpdump -i $INTERFACE -w $OUTPUT_DIR/capture_$(date +%Y%m%d_%H%M%S).pcap &
TCPDUMP_PID=$!

# Wait for specified duration
sleep $DURATION

# Stop capture
kill $TCPDUMP_PID

# Generate analysis report
tshark -r $OUTPUT_DIR/capture_*.pcap -z prot,colinfo > $OUTPUT_DIR/protocol_stats.txt
```
