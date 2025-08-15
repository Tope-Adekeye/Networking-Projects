# Wireshark Network Troubleshooting Laboratory

## 🎯 **Lab Overview**
This comprehensive troubleshooting laboratory demonstrates advanced network analysis techniques using Wireshark for diagnosing common network issues, performance problems, and connectivity failures in enterprise environments.

## 🔍 **Network Troubleshooting Methodology**

### **Systematic Analysis Approach**
```
1. Problem Identification
   ├── Gather symptoms and user reports
   ├── Define scope and impact
   └── Establish baseline behavior

2. Data Collection
   ├── Strategic capture point selection
   ├── Appropriate capture filters
   └── Sufficient capture duration

3. Analysis and Correlation
   ├── Protocol-specific analysis
   ├── Performance metrics evaluation
   └── Root cause identification

4. Solution Implementation
   ├── Configuration changes
   ├── Performance optimization
   └── Verification testing
```

## 📊 **Scenario 1: Slow Application Performance**

### **Problem Statement**
Users report slow response times when accessing internal web applications during peak hours.

### **Capture Strategy**
```bash
# Capture filter for web traffic analysis
host 192.168.1.100 and port 80 or port 443

# Alternative: Focus on specific application server
net 192.168.100.0/24 and (port 80 or port 443 or port 8080)
```

### **Key Analysis Points**

#### **TCP Performance Metrics**
```wireshark
# Display filters for performance analysis
tcp.analysis.flags                    # TCP issues and retransmissions
tcp.analysis.retransmission          # Retransmitted packets
tcp.analysis.duplicate_ack           # Duplicate ACKs
tcp.analysis.window_full             # Window size issues
tcp.time_delta > 1                   # Slow responses (>1 second)
```

#### **HTTP Response Time Analysis**
```wireshark
# HTTP response time tracking
http.time > 2                        # HTTP responses taking >2 seconds
http.response.code != 200            # Non-successful HTTP responses
http.content_length > 1000000        # Large content transfers
```

### **Common Root Causes and Solutions**

#### **1. Network Congestion**
**Symptoms in Wireshark:**
- High packet loss and retransmissions
- TCP window scaling issues
- Increased round-trip times

**Analysis Techniques:**
```wireshark
# Filter for congestion indicators
tcp.analysis.retransmission or tcp.analysis.fast_retransmission
tcp.window_size_scalefactor == -1    # Window scaling problems
tcp.analysis.zero_window             # Zero window conditions
```

**Solution Steps:**
1. Identify bandwidth bottlenecks
2. Implement QoS policies
3. Upgrade network infrastructure
4. Load balance traffic across multiple paths

#### **2. Server Performance Issues**
**Symptoms in Wireshark:**
- Long server response times
- Connection timeouts
- HTTP 50x error codes

**Analysis Techniques:**
```wireshark
# Server performance indicators
http.time > 5                        # Very slow server responses
tcp.flags.reset == 1                 # Connection resets
http.response.code >= 500            # Server errors
```

## 📊 **Scenario 2: Intermittent Connectivity Issues**

### **Problem Statement**
Users experience random disconnections and timeouts when accessing network resources.

### **Capture Strategy**
```bash
# Comprehensive connectivity monitoring
not arp and not stp and not cdp      # Exclude L2 protocols
tcp.flags.reset == 1 or icmp.type == 3  # Focus on connection issues
```

### **Analysis Framework**

#### **Connection Establishment Analysis**
```wireshark
# TCP handshake analysis
tcp.flags.syn == 1 and tcp.flags.ack == 0    # SYN packets
tcp.flags.syn == 1 and tcp.flags.ack == 1    # SYN-ACK packets
tcp.connection.fin                             # Connection terminations
tcp.connection.rst                             # Connection resets
```

#### **DNS Resolution Issues**
```wireshark
# DNS troubleshooting filters
dns.flags.rcode != 0                  # DNS errors
dns.time > 1                          # Slow DNS responses
dns.qry.name contains "example.com"   # Specific domain issues
```

### **Root Cause Analysis Techniques**

#### **1. Duplicate IP Addresses**
**Detection in Wireshark:**
```wireshark
# ARP conflicts and duplicate IPs
arp.duplicate-address-detected
arp.opcode == 2 and arp.src.proto_ipv4 == 192.168.1.100
```

**Investigation Steps:**
1. Monitor ARP traffic for conflicts
2. Check DHCP lease tables
3. Verify static IP assignments
4. Implement IP address management

#### **2. VLAN Configuration Issues**
**Detection in Wireshark:**
```wireshark
# VLAN tagging problems
vlan.id == 100                       # Specific VLAN traffic
not vlan                              # Untagged traffic on trunk
```

## 📊 **Scenario 3: Security Incident Investigation**

### **Problem Statement**
Suspicious network activity detected - possible data exfiltration or malware communication.

### **Capture Strategy**
```bash
# Security-focused capture
not (port 53 or port 123 or port 161)  # Exclude common protocols
tcp.port > 1024 and tcp.port < 5000    # Focus on dynamic ports
```

### **Threat Detection Filters**

#### **Malware Communication Patterns**
```wireshark
# Suspicious traffic indicators
tcp.flags.push == 1 and tcp.len < 10          # Small push packets
tcp.stream eq X and tcp.len == 0              # Empty ACKs (covert channel)
http.user_agent contains "bot" or http.user_agent contains "crawler"
dns.qry.name matches ".*\.tk$|.*\.ml$"        # Suspicious TLDs
```

#### **Data Exfiltration Detection**
```wireshark
# Large data transfers
tcp.len > 1460                        # Full-size TCP segments
ftp.request.command == "STOR"         # FTP uploads
http.request.method == "POST" and http.content_length > 10000
```

### **Security Analysis Workflows**

#### **1. Baseline vs. Anomaly Analysis**
```wireshark
# Establish normal traffic patterns
ip.src == 192.168.1.0/24 and ip.dst != 192.168.1.0/24  # External traffic
tcp.flags.syn == 1                    # Connection attempts
dns.qry.name                          # DNS queries
```

#### **2. Protocol Anomaly Detection**
```wireshark
# Unusual protocol usage
tcp.port == 80 and not http           # Non-HTTP on port 80
udp.port == 53 and not dns           # Non-DNS on port 53
tcp.flags == 0x00                     # Null scan detection
```

## 🔧 **Advanced Analysis Techniques**

### **Network Performance Profiling**

#### **Bandwidth Utilization Analysis**
```wireshark
# I/O Graph calculations for bandwidth
Statistics > I/O Graph
Y Axis: SUM(frame.len)
X Axis: Time intervals (1 second)
Filter: ip.addr == 192.168.1.0/24
```

#### **Application Response Time Analysis**
```wireshark
# Service Response Time analysis
Statistics > Service Response Time
Choose protocol: HTTP, SMB, RPC, etc.
Filter by specific servers or applications
```

### **Expert System Analysis**
```wireshark
# Expert Information analysis
Analyze > Expert Information
- Errors: Critical issues requiring immediate attention
- Warnings: Potential problems worth investigating
- Notes: Informational items for context
- Chats: Normal protocol conversations
```

## 📋 **Troubleshooting Checklists**

### **Performance Issues Checklist**
□ **Capture Location**: Strategic placement near problem area
□ **Capture Duration**: Sufficient time to observe patterns
□ **Baseline Comparison**: Normal vs. problematic periods
□ **Protocol Analysis**: Layer-specific examination
□ **Timing Analysis**: Request/response timing patterns
□ **Error Analysis**: Retransmissions, timeouts, resets
□ **Bandwidth Analysis**: Utilization and saturation points
□ **Application Behavior**: Protocol-specific analysis

### **Connectivity Issues Checklist**
□ **Physical Layer**: Cable, port, and link status
□ **Data Link Layer**: ARP, switching, VLAN configuration
□ **Network Layer**: IP addressing, routing, ICMP
□ **Transport Layer**: TCP/UDP port and connection state
□ **Session/Application**: Protocol-specific troubleshooting
□ **DNS Resolution**: Name resolution functionality
□ **Security Policies**: Firewall and ACL configurations
□ **Time Synchronization**: NTP and clock accuracy

### **Security Investigation Checklist**
□ **Incident Scope**: Affected systems and timeframe
□ **Traffic Baseline**: Normal vs. anomalous patterns
□ **Protocol Analysis**: Unexpected protocol usage
□ **Payload Examination**: Suspicious content or commands
□ **Communication Patterns**: C&C or exfiltration indicators
□ **Geolocation Analysis**: External IP reputation
□ **Timeline Reconstruction**: Event sequence and correlation
□ **Evidence Preservation**: Proper capture file handling

## 🎓 **Best Practices for Network Troubleshooting**

### **Capture Strategy Guidelines**
```bash
# Effective capture practices
1. Use appropriate capture filters to focus on relevant traffic
2. Capture from multiple strategic points for comprehensive view
3. Ensure sufficient buffer space for extended captures
4. Document capture conditions and network state
5. Maintain chain of custody for security investigations
```

### **Analysis Methodology**
```bash
# Systematic analysis approach
1. Start with high-level overview (Protocol Hierarchy)
2. Use Expert Information for automated issue detection
3. Follow TCP streams for connection-level analysis
4. Correlate timestamps across multiple captures
5. Document findings and create actionable recommendations
```

### **Performance Optimization**
```bash
# Wireshark performance tips
1. Use display filters instead of capture filters when possible
2. Close unused protocol decoders to improve performance
3. Limit capture file size for better responsiveness
4. Use command-line tools (tshark) for automated analysis
5. Implement proper file management and organization
```

## 📊 **Reporting and Documentation**

### **Executive Summary Template**
```markdown
## Network Issue Investigation Report

**Issue**: [Brief description]
**Impact**: [Business impact and affected users]
**Root Cause**: [Technical explanation]
**Resolution**: [Implemented solution]
**Prevention**: [Recommendations for future prevention]

### Technical Analysis
- **Problem Symptoms**: [Observable network behavior]
- **Investigation Method**: [Tools and techniques used]
- **Key Findings**: [Critical discovery points]
- **Performance Metrics**: [Before/after comparisons]

### Recommendations
1. [Immediate actions required]
2. [Long-term improvements]
3. [Monitoring enhancements]
```

### **Technical Evidence Documentation**
- **Capture Files**: Organized by timestamp and investigation phase
- **Filter Sets**: Documented for reproducible analysis
- **Screenshots**: Key findings and evidence preservation
- **Timeline**: Chronological event reconstruction
- **Metrics**: Quantitative performance measurements

---

**Related Labs**: [Security Investigation](../security-investigations/malware-analysis.md), [Protocol Analysis](../protocol-labs/), [Performance Optimization](network-performance-analysis.md)
