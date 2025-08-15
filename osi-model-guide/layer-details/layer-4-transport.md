# Layer 4: Transport Layer

## 🎯 **Purpose**
The Transport Layer provides reliable data transfer services to the upper layers. It manages end-to-end communication, error recovery, flow control, and ensures complete data transfer between host applications.

## 🔧 **Key Functions**
- **Segmentation**: Breaking data into manageable segments
- **Reassembly**: Reconstructing original data from segments
- **Error Detection**: Identifying corrupted or lost data
- **Error Recovery**: Retransmitting lost or corrupted segments
- **Flow Control**: Managing data transmission rate
- **Port Addressing**: Identifying specific applications/services

## 📋 **Primary Transport Protocols**

### **TCP (Transmission Control Protocol)**
- **Connection-Oriented**: Establishes reliable connections
- **Guaranteed Delivery**: Ensures all data arrives
- **Ordered Delivery**: Data arrives in correct sequence
- **Error Checking**: Detects and corrects transmission errors
- **Flow Control**: Prevents overwhelming the receiver
- **Congestion Control**: Manages network traffic

### **UDP (User Datagram Protocol)**
- **Connectionless**: No connection establishment required
- **Best-Effort Delivery**: No guarantee of delivery
- **Faster Transmission**: Lower overhead than TCP
- **No Error Recovery**: Applications handle errors
- **No Flow Control**: No transmission rate management
- **Broadcast Support**: Can send to multiple recipients

## 🔌 **Port Numbers and Services**

### **Well-Known Ports (0-1023)**
| Port | Protocol | Service | Description |
|------|----------|---------|-------------|
| 20/21 | TCP | FTP | File Transfer Protocol |
| 22 | TCP | SSH | Secure Shell |
| 23 | TCP | Telnet | Remote Terminal |
| 25 | TCP | SMTP | Email Sending |
| 53 | TCP/UDP | DNS | Domain Name Resolution |
| 67/68 | UDP | DHCP | Dynamic IP Assignment |
| 80 | TCP | HTTP | Web Traffic |
| 110 | TCP | POP3 | Email Retrieval |
| 143 | TCP | IMAP | Email Management |
| 443 | TCP | HTTPS | Secure Web Traffic |
| 993 | TCP | IMAPS | Secure IMAP |
| 995 | TCP | POP3S | Secure POP3 |

### **Registered Ports (1024-49151)**
| Port | Protocol | Service | Description |
|------|----------|---------|-------------|
| 1433 | TCP | SQL Server | Microsoft SQL Database |
| 1521 | TCP | Oracle | Oracle Database |
| 3306 | TCP | MySQL | MySQL Database |
| 3389 | TCP | RDP | Remote Desktop Protocol |
| 5432 | TCP | PostgreSQL | PostgreSQL Database |
| 5900 | TCP | VNC | Virtual Network Computing |
| 8080 | TCP | HTTP Alt | Alternative HTTP Port |
| 8443 | TCP | HTTPS Alt | Alternative HTTPS Port |

### **Dynamic/Private Ports (49152-65535)**
- **Client Ports**: Temporarily assigned for outbound connections
- **Ephemeral Ports**: Short-lived port assignments
- **Application-Specific**: Custom application ports

## 🔄 **TCP Connection Management**

### **Three-Way Handshake (Connection Establishment)**
```
Client                    Server
  |                         |
  |    SYN (seq=100)        |
  |------------------------>|
  |                         |
  |  SYN-ACK (seq=200,      |
  |   ack=101)              |
  |<------------------------|
  |                         |
  |    ACK (ack=201)        |
  |------------------------>|
  |                         |
  |   Connection Established |
```

### **Four-Way Handshake (Connection Termination)**
```
Client                    Server
  |                         |
  |    FIN (seq=300)        |
  |------------------------>|
  |                         |
  |    ACK (ack=301)        |
  |<------------------------|
  |                         |
  |    FIN (seq=400)        |
  |<------------------------|
  |                         |
  |    ACK (ack=401)        |
  |------------------------>|
  |                         |
  |   Connection Closed     |
```

## 🛡️ **Security Considerations**

### **Common Transport Layer Attacks**
- **TCP SYN Flood**: Overwhelming server with SYN requests
- **TCP Reset Attack**: Forceful connection termination
- **TCP Sequence Prediction**: Guessing sequence numbers
- **UDP Flood**: Overwhelming server with UDP packets
- **Port Scanning**: Discovering open services
- **Man-in-the-Middle**: Intercepting communications

### **Security Countermeasures**
- **SYN Cookies**: Protect against SYN flood attacks
- **Rate Limiting**: Limit connection attempts
- **Firewalls**: Filter unwanted traffic
- **Intrusion Detection**: Monitor for suspicious activity
- **Encryption**: Secure data transmission (TLS/SSL)

## 💼 **Real-World Examples**

### **Web Browser Connection (TCP)**
```
1. DNS Resolution: www.example.com → 93.184.216.34
2. TCP Handshake: Client:49152 ↔ Server:443
3. TLS Negotiation: Secure channel establishment
4. HTTP Request: GET /index.html
5. HTTP Response: 200 OK + HTML content
6. Connection Close: FIN/ACK sequence
```

### **Video Streaming (UDP)**
```
Media Server:5004 → Client:Random_Port
UDP Packet 1: [Video Frame 1][Timestamp][Sequence 001]
UDP Packet 2: [Video Frame 2][Timestamp][Sequence 002]
UDP Packet 3: [Video Frame 3][Timestamp][Sequence 003]
...
Note: No acknowledgments, fast delivery prioritized
```

### **Email Transmission (TCP)**
```
Client:49153 → SMTP Server:25
MAIL FROM: sender@example.com
RCPT TO: recipient@domain.com
DATA
Subject: Test Message
Hello World!
.
QUIT
```

## 🔍 **Flow Control and Congestion Control**

### **TCP Flow Control (Sliding Window)**
- **Window Size**: Amount of data sender can transmit
- **Window Scaling**: Adjust window size based on capacity
- **Zero Window**: Receiver temporarily stops sender
- **Window Update**: Receiver announces available space

### **TCP Congestion Control Algorithms**
- **Slow Start**: Gradually increase transmission rate
- **Congestion Avoidance**: Maintain optimal rate
- **Fast Retransmit**: Quick recovery from packet loss
- **Fast Recovery**: Avoid slow start after packet loss

## 📊 **Performance Monitoring**

### **TCP Performance Metrics**
- **Throughput**: Data transferred per unit time
- **Latency**: Round-trip time for packets
- **Packet Loss**: Percentage of lost packets
- **Retransmissions**: Number of packet retransmissions
- **Connection Time**: Time to establish connection

### **UDP Performance Metrics**
- **Packet Rate**: Packets transmitted per second
- **Jitter**: Variation in packet delay
- **Out-of-Order Delivery**: Packets arriving out of sequence
- **Duplicate Packets**: Redundant packet delivery

## 🧪 **Practical Exercises**

### **Exercise 1: TCP Connection Analysis**
```bash
# Monitor TCP connections
netstat -ant | grep ESTABLISHED
ss -t -a

# Capture TCP handshake
tcpdump -i eth0 -n "tcp[tcpflags] & tcp-syn != 0"

# Analyze TCP with Wireshark
# Filter: tcp.flags.syn==1 or tcp.flags.fin==1
```

### **Exercise 2: Port Scanning**
```bash
# Basic port scan with nmap
nmap -sT target_ip

# TCP SYN scan (stealth scan)
nmap -sS target_ip

# UDP port scan
nmap -sU target_ip

# Service version detection
nmap -sV target_ip
```

### **Exercise 3: Traffic Analysis**
```bash
# Monitor network traffic by protocol
netstat -s

# Check listening ports
netstat -tuln
ss -tuln

# Real-time traffic monitoring
iftop -i eth0
nethogs
```

## 🧰 **Tools for Transport Layer Analysis**

### **Network Analysis Tools**
- **Wireshark**: Comprehensive protocol analyzer
- **tcpdump**: Command-line packet capture
- **netstat**: Network statistics and connections
- **ss**: Socket statistics (modern netstat)
- **iftop**: Network bandwidth monitoring

### **Performance Testing Tools**
- **iperf3**: Network bandwidth testing
- **netperf**: Network performance measurement
- **ttcp**: TCP performance testing
- **hping3**: Custom packet generation

### **Security Testing Tools**
- **nmap**: Network discovery and port scanning
- **masscan**: High-speed port scanner
- **zmap**: Internet-wide network scanner
- **nc (netcat)**: Network connection utility

## 🔧 **Transport Layer Configuration**

### **TCP Tuning Parameters (Linux)**
```bash
# TCP window scaling
echo 1 > /proc/sys/net/ipv4/tcp_window_scaling

# TCP congestion control algorithm
echo "cubic" > /proc/sys/net/ipv4/tcp_congestion_control

# TCP keepalive settings
echo 7200 > /proc/sys/net/ipv4/tcp_keepalive_time
echo 9 > /proc/sys/net/ipv4/tcp_keepalive_probes
echo 75 > /proc/sys/net/ipv4/tcp_keepalive_intvl

# TCP buffer sizes
echo "4096 65536 16777216" > /proc/sys/net/ipv4/tcp_rmem
echo "4096 65536 16777216" > /proc/sys/net/ipv4/tcp_wmem
```

### **Firewall Configuration**
```bash
# iptables examples
# Allow TCP traffic on port 80
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Block UDP traffic from specific IP
iptables -A INPUT -p udp -s 192.168.1.100 -j DROP

# Limit TCP connection rate
iptables -A INPUT -p tcp --dport 22 -m limit --limit 5/min -j ACCEPT
```

## 🎓 **Learning Resources**

### **RFCs (Request for Comments)**
- [RFC 793 - TCP Specification](https://tools.ietf.org/html/rfc793)
- [RFC 768 - UDP Specification](https://tools.ietf.org/html/rfc768)
- [RFC 6298 - TCP Retransmission Timeout](https://tools.ietf.org/html/rfc6298)
- [RFC 5681 - TCP Congestion Control](https://tools.ietf.org/html/rfc5681)

### **Performance Optimization Guides**
- **TCP/IP Illustrated Series** by W. Richard Stevens
- **High Performance Browser Networking** by Ilya Grigorik
- **Linux Network Performance Tuning** guides
