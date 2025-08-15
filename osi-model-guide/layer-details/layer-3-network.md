# Layer 3: Network Layer

## 🎯 **Purpose**
The Network Layer determines the best physical path for data to reach its destination across multiple networks. It handles routing, logical addressing, and packet forwarding between different network segments.

## 🔧 **Key Functions**
- **Logical Addressing**: IP addressing for unique device identification
- **Routing**: Path determination across multiple networks
- **Packet Forwarding**: Moving packets toward their destination
- **Path Selection**: Choosing optimal routes through network topology
- **Fragmentation**: Breaking large packets into smaller pieces
- **Internetworking**: Connecting different network types

## 📋 **Core Network Protocols**

### **Internet Protocol (IP)**
- **IPv4**: 32-bit addressing (4.3 billion addresses)
- **IPv6**: 128-bit addressing (340 undecillion addresses)
- **IP Header**: Contains routing and control information
- **Fragmentation**: Handles Maximum Transmission Unit (MTU) limits
- **Time to Live (TTL)**: Prevents infinite packet loops

### **Routing Protocols**
- **RIP**: Routing Information Protocol (distance-vector)
- **OSPF**: Open Shortest Path First (link-state)
- **EIGRP**: Enhanced Interior Gateway Routing Protocol
- **BGP**: Border Gateway Protocol (path-vector)
- **IS-IS**: Intermediate System to Intermediate System

### **Internet Control Message Protocol (ICMP)**
- **Ping**: Echo request/reply for connectivity testing
- **Traceroute**: Path discovery to destination
- **Error Reporting**: Network unreachable, host unreachable
- **Path MTU Discovery**: Determining maximum packet size

## 🌐 **IP Addressing and Subnetting**

### **IPv4 Address Classes**
| Class | Range | Default Subnet Mask | Network Bits | Host Bits |
|-------|-------|-------------------|--------------|-----------|
| A | 1.0.0.0 - 126.255.255.255 | 255.0.0.0 (/8) | 8 | 24 |
| B | 128.0.0.0 - 191.255.255.255 | 255.255.0.0 (/16) | 16 | 16 |
| C | 192.0.0.0 - 223.255.255.255 | 255.255.255.0 (/24) | 24 | 8 |
| D | 224.0.0.0 - 239.255.255.255 | Multicast | - | - |
| E | 240.0.0.0 - 255.255.255.255 | Reserved | - | - |

### **Private IP Address Ranges**
- **Class A**: 10.0.0.0/8 (10.0.0.0 - 10.255.255.255)
- **Class B**: 172.16.0.0/12 (172.16.0.0 - 172.31.255.255)
- **Class C**: 192.168.0.0/16 (192.168.0.0 - 192.168.255.255)

### **Special IP Addresses**
- **127.0.0.1**: Loopback (localhost)
- **0.0.0.0**: Default route or unspecified
- **255.255.255.255**: Limited broadcast
- **169.254.x.x**: APIPA (Automatic Private IP Addressing)

### **Subnetting Examples**
```
Network: 192.168.1.0/24
Subnet Mask: 255.255.255.0

Subnetting into 4 subnets (/26):
Subnet 1: 192.168.1.0/26   (192.168.1.1 - 192.168.1.62)
Subnet 2: 192.168.1.64/26  (192.168.1.65 - 192.168.1.126)
Subnet 3: 192.168.1.128/26 (192.168.1.129 - 192.168.1.190)
Subnet 4: 192.168.1.192/26 (192.168.1.193 - 192.168.1.254)
```

## 🗺️ **Routing Fundamentals**

### **Routing Table Components**
- **Destination Network**: Target network address
- **Subnet Mask**: Network/host portion identifier
- **Next Hop**: Router to forward packets to
- **Interface**: Exit interface for packet forwarding
- **Metric**: Cost or preference for route selection

### **Routing Types**
- **Static Routing**: Manually configured routes
- **Dynamic Routing**: Automatically learned routes
- **Default Routing**: Catch-all route (0.0.0.0/0)
- **Host Routing**: Route to specific host (/32)

### **Route Selection Process**
1. **Longest Prefix Match**: Most specific route wins
2. **Administrative Distance**: Route source preference
3. **Metric**: Path cost comparison
4. **Load Balancing**: Multiple equal-cost paths

## 🛡️ **Network Security**

### **Common Network Layer Attacks**
- **IP Spoofing**: Forging source IP addresses
- **Route Hijacking**: Malicious route advertisements
- **DDoS Attacks**: Distributed denial of service
- **Packet Sniffing**: Intercepting network traffic
- **Man-in-the-Middle**: Intercepting communications
- **Smurf Attack**: ICMP amplification attack

### **Security Countermeasures**
- **Access Control Lists (ACLs)**: Traffic filtering rules
- **uRPF**: Unicast Reverse Path Forwarding
- **Rate Limiting**: Prevent flooding attacks
- **IPSec**: IP Security for encryption and authentication
- **Firewalls**: Network traffic filtering and inspection

## 🔍 **Network Address Translation (NAT)**

### **NAT Types**
- **Static NAT**: One-to-one IP mapping
- **Dynamic NAT**: Pool of public IPs
- **PAT (NAT Overload)**: Port-based translation
- **Destination NAT**: Incoming traffic translation

### **NAT Benefits and Limitations**
**Benefits:**
- Conserves public IP addresses
- Provides basic security (hides internal structure)
- Enables multiple devices to share single public IP

**Limitations:**
- Breaks end-to-end connectivity
- Complicates peer-to-peer applications
- Additional processing overhead
- Potential security vulnerabilities

## 💼 **Real-World Examples**

### **Packet Journey Example**
```
Source: 192.168.1.100 → Destination: 8.8.8.8

1. Host routing table lookup
   Default route: 0.0.0.0/0 via 192.168.1.1

2. Layer 2 encapsulation
   Destination MAC: Router's LAN interface

3. Router receives packet
   Route lookup: 8.8.8.8 matches 0.0.0.0/0 via ISP

4. NAT translation
   192.168.1.100:1024 → 203.0.113.5:5678

5. ISP routing
   Multiple router hops based on BGP routes

6. Destination reached
   8.8.8.8 (Google DNS server)
```

### **ICMP Troubleshooting**
```bash
# Test connectivity
ping 8.8.8.8

# Trace packet path
traceroute 8.8.8.8
tracert 8.8.8.8 (Windows)

# Test with specific packet size
ping -s 1472 8.8.8.8

# Continuous ping
ping -t 8.8.8.8 (Windows)
ping 8.8.8.8 (Linux - continuous by default)
```

## 📊 **Performance and Troubleshooting**

### **Network Performance Metrics**
- **Bandwidth**: Maximum data transmission rate
- **Latency**: Round-trip time for packets
- **Jitter**: Variation in packet delay
- **Packet Loss**: Percentage of lost packets
- **Throughput**: Actual data transfer rate

### **Common Network Issues**
- **Routing Loops**: Packets circulating indefinitely
- **Black Holes**: Packets dropped without notification
- **Asymmetric Routing**: Different paths for send/receive
- **MTU Mismatches**: Fragmentation issues
- **Route Flapping**: Unstable route advertisements

## 🧪 **Practical Exercises**

### **Exercise 1: IP Configuration and Testing**
```bash
# Check IP configuration
ip addr show
ifconfig -a (older systems)

# Add static route
ip route add 192.168.2.0/24 via 192.168.1.1
route add -net 192.168.2.0/24 gw 192.168.1.1

# View routing table
ip route show
route -n
netstat -rn
```

### **Exercise 2: Subnetting Practice**
```
Given network: 172.16.0.0/16
Requirements: 8 subnets with ~8000 hosts each

Solution: Use /19 subnetting
Subnet mask: 255.255.224.0 (/19)
Each subnet: 8190 usable hosts

Subnets:
172.16.0.0/19   (172.16.0.1 - 172.16.31.254)
172.16.32.0/19  (172.16.32.1 - 172.16.63.254)
172.16.64.0/19  (172.16.64.1 - 172.16.95.254)
...and so on
```

### **Exercise 3: Network Troubleshooting**
```bash
# Test connectivity
ping -c 4 destination_ip

# Trace route to destination
traceroute destination_ip
mtr destination_ip (real-time traceroute)

# Check ARP table
arp -a
ip neigh show

# Monitor network traffic
tcpdump -i eth0 icmp
wireshark (GUI)
```

## 🧰 **Tools for Network Layer Analysis**

### **Command-Line Tools**
- **ping**: Basic connectivity testing
- **traceroute/tracert**: Path discovery
- **netstat**: Network statistics and connections
- **ip**: Modern Linux networking tool
- **route**: Routing table management

### **Network Analyzers**
- **Wireshark**: Comprehensive packet analysis
- **tcpdump**: Command-line packet capture
- **tshark**: Terminal-based Wireshark
- **Nmap**: Network discovery and port scanning

### **Routing Tools**
- **Quagga/FRR**: Open-source routing software
- **BIRD**: Internet routing daemon
- **GNS3**: Network simulation platform
- **Packet Tracer**: Cisco network simulator

## 🔧 **Router Configuration Examples**

### **Basic Router Configuration (Cisco)**
```
Router(config)# interface gigabitethernet0/0
Router(config-if)# ip address 192.168.1.1 255.255.255.0
Router(config-if)# no shutdown
Router(config-if)# exit

Router(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.1

Router(config)# access-list 100 permit tcp any any eq 80
Router(config)# access-list 100 deny ip any any
```

### **Linux as Router**
```bash
# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Add to /etc/sysctl.conf for persistence
net.ipv4.ip_forward = 1

# Configure NAT with iptables
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
iptables -A FORWARD -i eth0 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

## 🎓 **Learning Resources**

### **RFCs (Request for Comments)**
- [RFC 791 - Internet Protocol (IPv4)](https://tools.ietf.org/html/rfc791)
- [RFC 8200 - Internet Protocol Version 6 (IPv6)](https://tools.ietf.org/html/rfc8200)
- [RFC 792 - Internet Control Message Protocol](https://tools.ietf.org/html/rfc792)
- [RFC 1918 - Private Internet Address Allocation](https://tools.ietf.org/html/rfc1918)

### **Routing Protocol RFCs**
- [RFC 2328 - OSPF Version 2](https://tools.ietf.org/html/rfc2328)
- [RFC 4271 - Border Gateway Protocol 4 (BGP-4)](https://tools.ietf.org/html/rfc4271)
- [RFC 2080 - RIPng for IPv6](https://tools.ietf.org/html/rfc2080)
