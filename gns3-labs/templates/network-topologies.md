# GNS3 Network Topology Templates

## 🎯 **Overview**
This document provides standardized network topology templates for common networking scenarios in GNS3. These templates serve as starting points for building complex network simulations and can be customized for specific requirements.

## 🏗️ **Basic Network Topologies**

### **1. Simple Router-to-Router Connection**
```
[R1] ────────── [R2]
     Serial Link
   192.168.1.0/30
```

**Use Cases:**
- Basic routing protocol testing
- WAN link simulation
- Point-to-point protocol configuration

**Device Requirements:**
- 2 x Cisco routers (any IOS version)
- Serial interfaces or Ethernet with crossover

**Configuration Template:**
```cisco
! R1 Configuration
interface serial0/0
 ip address 192.168.1.1 255.255.255.252
 clock rate 128000
 no shutdown

! R2 Configuration  
interface serial0/0
 ip address 192.168.1.2 255.255.255.252
 no shutdown
```

---

### **2. Hub and Spoke Topology**
```
        [HQ-Router]
           /  |  \
          /   |   \
    [Branch1] | [Branch3]
         [Branch2]
```

**Use Cases:**
- MPLS VPN simulation
- Hub-and-spoke VPN deployment
- Centralized routing architecture

**Device Requirements:**
- 1 x Hub router (ISR 4331 recommended)
- 3+ x Spoke routers
- Frame Relay switch (or point-to-point links)

**IP Addressing Scheme:**
```
Hub: 10.0.0.1/24 (Loopback)
Spoke 1: 10.1.1.0/24
Spoke 2: 10.2.2.0/24
Spoke 3: 10.3.3.0/24
WAN Links: 192.168.x.0/30
```

---

### **3. Three-Tier Hierarchical Design**
```
         Core Layer
      [SW1-Core] ── [SW2-Core]
         /    \    /    \
        /      \  /      \
   [R1-Dist] ── X ── [R2-Dist]
      /  \            /  \
     /    \          /    \
[SW1-Acc][SW2-Acc][SW3-Acc][SW4-Acc]
   |      |      |      |
 Users  Users  Users  Users
```

**Use Cases:**
- Enterprise campus networks
- Scalable network design
- Redundancy and load balancing

**Device Requirements:**
- 2 x Core switches (Layer 3 capable)
- 2 x Distribution routers
- 4 x Access switches
- Multiple end devices

---

### **4. Service Provider Core**
```
[PE1] ── [P1] ── [P2] ── [PE2]
  |      /  \    /  \      |
  |     /    \  /    \     |
[CE1] [P3] ── [P4] ── [P5][CE2]
        \      |      /
         \     |     /
          [PE3]─┴─[PE4]
```

**Use Cases:**
- MPLS service provider networks
- BGP route reflection
- Traffic engineering

**Device Requirements:**
- Multiple high-end routers
- MPLS capability
- BGP and IGP protocols

---

## 🌐 **Advanced Network Scenarios**

### **5. Multi-Site Enterprise Network**
```
    Internet
       |
   [Firewall]
       |
   Headquarters
   [Core-SW] ──┐
       |       |
   [Dist-R1]   |
       |       |
   [Access-SW] |
       |       |
    Users      |
              /
         WAN Links
        /         \
   Branch-A     Branch-B
   [Router]     [Router]
      |            |
   [Switch]     [Switch]
      |            |
    Users        Users
```

**Use Cases:**
- Multi-site corporate networks
- WAN optimization testing
- Site-to-site VPN implementation

**Key Technologies:**
- OSPF or EIGRP for routing
- HSRP/VRRP for redundancy
- VPN tunnels for WAN
- QoS for voice/video

---

### **6. Data Center Fabric**
```
      Spine Layer
   [SP1] ── [SP2] ── [SP3]
    / \     / \     / \
   /   \   /   \   /   \
  /     \ /     \ /     \
[L1] ── [L2] ── [L3] ── [L4]
      Leaf Layer
 |       |       |       |
Servers Servers Servers Servers
```

**Use Cases:**
- Modern data center design
- East-west traffic optimization
- Container networking

**Technologies:**
- BGP EVPN
- VXLAN overlays
- Anycast gateways

---

### **7. Internet Service Provider (ISP)**
```
    Peering
      |
   [Border Router]
      |
   [Core Router] ──── [Route Reflector]
      |                     |
   [Aggregation] ────── [Aggregation]
      |                     |
   [PE Router] ───────── [PE Router]
      |                     |
   Customer A           Customer B
```

**Use Cases:**
- ISP network simulation
- BGP routing policies
- MPLS VPN services

**Protocols:**
- iBGP and eBGP
- OSPF or IS-IS for IGP
- MPLS LDP/RSVP-TE

---

## 🔧 **Specialized Topologies**

### **8. Wireless LAN Controller Setup**
```
[WLC] ──── [Core Switch]
  |             |
  |         [Access SW]
  |             |
  |          [AP1][AP2]
  |             |
  └─── Management Network
```

**Use Cases:**
- Enterprise wireless deployment
- Centralized wireless management
- Guest network implementation

---

### **9. Network Security Lab**
```
Internet ── [Perimeter FW] ── [Core] ── [Internal FW] ── [Servers]
                |                           |
            [DMZ Servers]              [User Network]
                |                           |
           [Web/Mail/DNS]               [Workstations]
```

**Use Cases:**
- Security policy testing
- Intrusion detection/prevention
- Network segmentation

---

### **10. Voice over IP (VoIP) Network**
```
[Call Manager] ── [Voice Gateway] ── PSTN
       |               |
   [Core SW] ──────────┘
       |
   [Access SW]
       |
   [IP Phones] ── [PCs]
```

**Use Cases:**
- VoIP implementation
- Quality of Service (QoS)
- Voice VLAN configuration

---

## 📋 **Template Selection Guide**

### **By Experience Level**
| **Level** | **Recommended Templates** | **Focus Areas** |
|-----------|-------------------------|-----------------|
| **Beginner** | Router-to-Router, Simple Hub-Spoke | Basic routing, IP addressing |
| **Intermediate** | Three-Tier, Multi-Site | VLANs, routing protocols, redundancy |
| **Advanced** | Data Center, ISP Core | BGP, MPLS, advanced protocols |

### **By Use Case**
| **Scenario** | **Template** | **Key Technologies** |
|--------------|-------------|---------------------|
| **Enterprise Campus** | Three-Tier Hierarchical | OSPF, VLANs, HSRP |
| **Service Provider** | ISP Core Network | BGP, MPLS, Route Reflection |
| **Branch Connectivity** | Hub and Spoke | VPN, QoS, WAN protocols |
| **Security Testing** | Security Lab | Firewalls, ACLs, IPS |
| **Cloud Integration** | Hybrid Cloud | SD-WAN, Cloud connectivity |

### **By Device Count**
| **Size** | **Devices** | **Recommended Templates** |
|----------|-------------|-------------------------|
| **Small (2-5)** | Router-to-Router, Basic Hub-Spoke | Learning fundamentals |
| **Medium (6-15)** | Three-Tier, Multi-Site | Enterprise scenarios |
| **Large (16+)** | Data Center, ISP Core | Complex simulations |

## 🛠️ **Template Customization Guidelines**

### **IP Addressing Standards**
```bash
# Private IP Address Allocation
10.0.0.0/8     - Large enterprise networks
172.16.0.0/12  - Medium enterprise networks  
192.168.0.0/16 - Small networks and labs

# Subnet Organization
x.x.0.0/24    - Core infrastructure
x.x.1.0/24    - Distribution layer
x.x.10.0/24   - Access layer (VLAN 10)
x.x.20.0/24   - Access layer (VLAN 20)
x.x.100.0/24  - Management network
x.x.200.0/24  - Voice network
```

### **VLAN Standards**
```bash
VLAN 1    - Native/Default (unused)
VLAN 10   - Sales/Users
VLAN 20   - Engineering/IT
VLAN 30   - Finance/Management
VLAN 100  - Management/Infrastructure
VLAN 200  - Voice/IP Phones
VLAN 300  - Guest Network
VLAN 999  - Quarantine/Security
```

### **Device Naming Conventions**
```bash
# Router naming: <Site>-<Function>-<Number>
HQ-CORE-01, HQ-DIST-01, BR1-EDGE-01

# Switch naming: <Site>-<Layer>-<Number>
HQ-CORE-SW01, HQ-ACC-SW01, BR1-ACC-SW01

# Server naming: <Function>-<Environment>-<Number>
WEB-PROD-01, DB-DEV-01, DNS-SHARED-01
```

## 📊 **Performance Considerations**

### **Resource Requirements by Topology**
| **Template** | **RAM (GB)** | **CPU Cores** | **Devices** |
|-------------|-------------|--------------|-------------|
| **Basic Router-to-Router** | 2-4 | 2 | 2-3 |
| **Hub and Spoke** | 4-8 | 4 | 4-6 |
| **Three-Tier** | 8-16 | 4-8 | 8-12 |
| **Data Center** | 16+ | 8+ | 12+ |

### **Optimization Tips**
```bash
# Reduce CPU usage:
- Use idle-pc optimization
- Minimize routing table sizes
- Adjust hello timers appropriately
- Use static routes where possible

# Memory optimization:
- Allocate minimum required RAM
- Use sparse memory features
- Close unused console sessions
- Monitor memory usage regularly
```

## 🔄 **Template Deployment Process**

### **Step 1: Template Selection**
1. Identify network requirements
2. Choose appropriate template
3. Verify resource availability
4. Download required IOS images

### **Step 2: Basic Setup**
1. Create new GNS3 project
2. Add devices from template
3. Configure basic connectivity
4. Verify physical topology

### **Step 3: Configuration**
1. Apply IP addressing scheme
2. Configure routing protocols
3. Implement security policies
4. Add redundancy features

### **Step 4: Testing**
1. Verify connectivity
2. Test failover scenarios
3. Monitor performance
4. Document configuration

### **Step 5: Documentation**
1. Create network diagram
2. Document IP addressing
3. Save device configurations
4. Create troubleshooting guide

---

**Related Documents**: [GNS3 Setup Guide](../documentation/gns3-setup-guide.md), [Lab Scenarios](../lab-scenarios/), [Configuration Examples](../configurations/)
