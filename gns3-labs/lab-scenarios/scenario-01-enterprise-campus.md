# GNS3 Lab Scenario 1: Enterprise Campus Network

## 🎯 **Lab Objectives**
- Design and implement a realistic enterprise campus network
- Configure hierarchical network architecture (Core, Distribution, Access)
- Implement advanced routing protocols (OSPF, EIGRP, BGP)
- Configure redundancy and high availability features
- Apply comprehensive security policies and monitoring

## 🏗️ **Network Topology Overview**

```
                    Internet/WAN
                         │
                    [ISP Router]
                         │
                    ┌────▼────┐
    ┌──────────────►│   FW1   │◄──────────────┐
    │               │(ASA 5505)│               │
    │               └────┬────┘               │
    │                    │                    │
    │              Core Layer                 │
    │              (Area 0)                   │
    │                    │                    │
    │        ┌───────────┼───────────┐        │
    │        │           │           │        │
    │   ┌────▼───┐  ┌────▼───┐  ┌────▼───┐    │
    │   │  SW1   │◄─┤  SW2   ├─►│  SW3   │    │
    │   │ Core   │  │ Core   │  │ Core   │    │
    │   └────┬───┘  └────┬───┘  └────┬───┘    │
    │        │           │           │        │
    │   Distribution Layer        Distribution │
    │   (Area 1)      (Area 0)     (Area 2)   │
    │        │           │           │        │
    │   ┌────▼───┐  ┌────▼───┐  ┌────▼───┐    │
    │   │  R1    │  │  R2    │  │  R3    │    │
    │   │Distrib │  │Distrib │  │Distrib │    │
    │   └────┬───┘  └────┬───┘  └────┬───┘    │
    │        │           │           │        │
    │   Access Layer  Access Layer  Access    │
    │        │           │           │        │
    │   ┌────▼───┐  ┌────▼───┐  ┌────▼───┐    │
    │   │  SW4   │  │  SW5   │  │  SW6   │    │
    └──►│Access1 │  │Access2 │  │Access3 │◄───┘
        └────┬───┘  └────┬───┘  └────┬───┘
             │           │           │
        Building A   Building B   Building C
         (Sales)      (IT/Eng)    (Finance)
```

## 📋 **Required GNS3 Components**

### **Network Devices**
- **3 x Core Switches**: Cisco Catalyst 3560 or multilayer switch images
- **3 x Distribution Routers**: Cisco ISR 4331 or 2911 series
- **3 x Access Switches**: Cisco Catalyst 2960 series
- **1 x Firewall**: Cisco ASA 5505 or pfSense appliance
- **1 x ISP Router**: Generic router for internet simulation
- **Multiple end devices**: PCs, servers, IP phones

### **Virtual Appliances (Optional)**
- **DHCP Server**: Windows/Linux server appliance
- **DNS Server**: BIND9 or Windows DNS server
- **Web Server**: Apache/nginx for application testing
- **Monitoring Server**: PRTG or LibreNMS appliance

## 🔧 **Implementation Phases**

### **Phase 1: Basic Infrastructure Setup**

#### **Core Layer Configuration (SW1-SW3)**
```cisco
! Core Switch 1 (SW1) Configuration
hostname SW1-Core
!
vlan 10
 name Sales
vlan 20
 name Engineering
vlan 30
 name Finance
vlan 100
 name Management
vlan 200
 name Voice
!
interface vlan 100
 ip address 10.1.100.1 255.255.255.0
 no shutdown
!
! Core-to-Core links (Layer 3)
interface gig0/1
 description "Link to SW2-Core"
 no switchport
 ip address 10.1.1.1 255.255.255.252
 no shutdown
!
interface gig0/2
 description "Link to SW3-Core"
 no switchport
 ip address 10.1.1.5 255.255.255.252
 no shutdown
!
! Distribution links
interface gig0/11
 description "Link to R1-Distribution"
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,100,200
 no shutdown
!
spanning-tree mode rapid-pvst
spanning-tree vlan 1-4094 priority 4096
```

#### **Distribution Layer Configuration (R1-R3)**
```cisco
! Distribution Router 1 (R1) Configuration
hostname R1-Distribution
!
interface gig0/0
 description "Link to SW1-Core"
 no shutdown
!
! Subinterfaces for VLANs
interface gig0/0.10
 description "Sales VLAN"
 encapsulation dot1Q 10
 ip address 10.1.10.1 255.255.255.0
 ip helper-address 10.1.100.10
!
interface gig0/0.20
 description "Engineering VLAN"
 encapsulation dot1Q 20
 ip address 10.1.20.1 255.255.255.0
 ip helper-address 10.1.100.10
!
interface gig0/0.100
 description "Management VLAN"
 encapsulation dot1Q 100
 ip address 10.1.100.254 255.255.255.0
!
interface gig0/1
 description "Link to SW4-Access"
 no shutdown
!
! HSRP Configuration for redundancy
interface gig0/0.10
 standby 10 ip 10.1.10.254
 standby 10 priority 110
 standby 10 preempt
!
interface gig0/0.20
 standby 20 ip 10.1.20.254
 standby 20 priority 110
 standby 20 preempt
```

### **Phase 2: Routing Protocol Implementation**

#### **OSPF Multi-Area Configuration**
```cisco
! R1 OSPF Configuration (Area 1)
router ospf 1
 router-id 1.1.1.1
 network 10.1.10.0 0.0.0.255 area 1
 network 10.1.20.0 0.0.0.255 area 1
 network 10.1.100.0 0.0.0.255 area 1
 network 10.1.1.0 0.0.0.3 area 0
 area 1 range 10.1.0.0 255.255.0.0
 passive-interface default
 no passive-interface gig0/1
!
! R2 OSPF Configuration (Backbone Area 0)
router ospf 1
 router-id 2.2.2.2
 network 10.1.1.0 0.0.0.15 area 0
 network 10.1.100.0 0.0.0.255 area 0
 default-information originate
```

#### **EIGRP Configuration (Alternative)**
```cisco
! Alternative EIGRP implementation
router eigrp CAMPUS
 address-family ipv4 unicast autonomous-system 100
  network 10.1.0.0 0.0.255.255
  topology base
   distribute-list FILTER out gig0/0
  exit-topology
 exit-address-family
!
ip prefix-list FILTER deny 10.1.30.0/24
ip prefix-list FILTER permit 0.0.0.0/0 le 32
```

### **Phase 3: Advanced Security Implementation**

#### **Cisco ASA Firewall Configuration**
```cisco
! Basic ASA Configuration
hostname CAMPUS-FW1
!
interface gigabitethernet0/0
 nameif outside
 security-level 0
 ip address 203.0.113.2 255.255.255.252
 no shutdown
!
interface gigabitethernet0/1
 nameif inside
 security-level 100
 ip address 10.1.254.1 255.255.255.0
 no shutdown
!
! NAT Configuration
object network INSIDE_NET
 subnet 10.1.0.0 255.255.0.0
 nat (inside,outside) dynamic interface
!
! Access Control Lists
access-list OUTSIDE_IN extended permit icmp any any
access-list OUTSIDE_IN extended permit tcp any object INSIDE_NET eq 80
access-list OUTSIDE_IN extended permit tcp any object INSIDE_NET eq 443
access-list OUTSIDE_IN extended deny ip any any
access-group OUTSIDE_IN in interface outside
!
! Default route
route outside 0.0.0.0 0.0.0.0 203.0.113.1
```

#### **Switch Port Security and VLANs**
```cisco
! Access Switch Configuration (SW4)
hostname SW4-Access1
!
! Port security on access ports
interface range fa0/1-20
 switchport mode access
 switchport access vlan 10
 switchport port-security
 switchport port-security maximum 2
 switchport port-security mac-address sticky
 switchport port-security violation restrict
 spanning-tree portfast
 spanning-tree bpduguard enable
!
! Voice VLAN configuration
interface range fa0/21-30
 switchport mode access
 switchport access vlan 10
 switchport voice vlan 200
 switchport port-security
 switchport port-security maximum 3
 mls qos trust device cisco-phone
 auto qos voip cisco-phone
!
! Trunk to distribution
interface gig0/1
 description "Trunk to R1-Distribution"
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,100,200
```

## 🔍 **Advanced Features Implementation**

### **Quality of Service (QoS)**
```cisco
! QoS Policy for Voice Traffic
class-map match-all VOICE
 match dscp ef
!
class-map match-all VIDEO
 match dscp af41
!
policy-map WAN_QOS
 class VOICE
  priority percent 25
 class VIDEO
  bandwidth percent 25
 class class-default
  bandwidth remaining percent 50
  random-detect
!
interface serial0/1/0
 service-policy output WAN_QOS
```

### **Network Monitoring and SNMP**
```cisco
! SNMP Configuration
snmp-server community public RO
snmp-server community private RW
snmp-server host 10.1.100.10 version 2c public
snmp-server enable traps config
snmp-server enable traps interface
snmp-server enable traps hsrp
!
! NetFlow for traffic analysis
interface gig0/0
 ip flow ingress
 ip flow egress
!
ip flow-export destination 10.1.100.11 9996
ip flow-export version 9
```

### **Network Time Protocol (NTP)**
```cisco
! NTP Configuration
ntp server 10.1.100.12
ntp update-calendar
clock timezone EST -5
clock summer-time EDT recurring
!
! Logging configuration
logging buffered 4096 informational
logging host 10.1.100.13
logging facility local0
logging source-interface vlan100
```

## 📊 **Testing and Verification Procedures**

### **Connectivity Testing Matrix**
```bash
# Inter-VLAN connectivity tests
ping 10.1.10.10 source 10.1.20.10   # Sales to Engineering
ping 10.1.30.10 source 10.1.10.10   # Sales to Finance
ping 8.8.8.8 source 10.1.10.10      # Internet connectivity

# Redundancy testing
# Shutdown primary HSRP router
interface gig0/0
 shutdown
# Verify failover to standby router
show standby brief
```

### **Performance Metrics**
```cisco
! Monitor interface utilization
show interfaces gigabitethernet0/0 | include rate
show interfaces gigabitethernet0/0 counters

! Check routing table convergence
show ip route summary
show ip ospf database
show ip eigrp topology

! Verify QoS operation
show policy-map interface gig0/0
show class-map
```

### **Security Verification**
```cisco
! Verify port security
show port-security interface fa0/1
show port-security address

! Check firewall status
show access-list
show nat pool
show connection

! Monitor for security violations
show logging | include VIOLATION
```

## 🛠️ **Troubleshooting Scenarios**

### **Scenario 1: OSPF Adjacency Issues**
**Problem**: R1 and R2 not forming OSPF neighbor relationship
**Diagnosis Steps**:
```cisco
show ip ospf neighbor
show ip ospf interface
debug ip ospf hello
debug ip ospf adj
```
**Common Causes**:
- Area ID mismatch
- Authentication mismatch
- Hello/Dead timer mismatch
- Network type mismatch

### **Scenario 2: Inter-VLAN Routing Failure**
**Problem**: PCs in different VLANs cannot communicate
**Diagnosis Steps**:
```cisco
show vlan brief
show interfaces trunk
show ip route
ping from different VLANs
```
**Common Causes**:
- Trunk configuration errors
- Missing VLAN on trunk
- Routing table issues
- ACL blocking traffic

### **Scenario 3: HSRP Failover Issues**
**Problem**: Gateway redundancy not working properly
**Diagnosis Steps**:
```cisco
show standby brief
show standby
debug standby events
```
**Common Causes**:
- Priority misconfiguration
- Preempt not enabled
- Interface issues
- Authentication problems

## 🎓 **Learning Outcomes and Extensions**

### **Skills Developed**
□ **Enterprise Network Design**: Hierarchical network architecture implementation
□ **Advanced Routing**: Multi-area OSPF and EIGRP configuration
□ **High Availability**: HSRP and redundancy implementation
□ **Security Integration**: Firewall and access control configuration
□ **Quality of Service**: Voice and video traffic prioritization
□ **Network Monitoring**: SNMP, NetFlow, and logging implementation

### **Possible Extensions**
1. **IPv6 Implementation**: Dual-stack configuration throughout campus
2. **MPLS Integration**: Connect multiple campus sites via MPLS VPN
3. **Wireless Integration**: Add wireless LAN controllers and access points
4. **Data Center**: Add server farm with load balancing
5. **WAN Optimization**: Implement WAN acceleration appliances
6. **Network Automation**: Add Python scripts for configuration management

## 📋 **Lab Completion Checklist**

### **Phase 1 Completion**
□ All devices configured with basic settings
□ VLANs created and assigned properly
□ Trunk links operational
□ Management connectivity established

### **Phase 2 Completion**
□ OSPF adjacencies established
□ Routing tables populated correctly
□ Inter-VLAN routing functional
□ Internet connectivity working

### **Phase 3 Completion**
□ Firewall policies applied and tested
□ Port security configured and functional
□ HSRP redundancy tested
□ QoS policies applied and verified

### **Final Verification**
□ End-to-end connectivity tested
□ Failover scenarios validated
□ Security policies enforced
□ Performance metrics collected
□ Documentation completed

---

**Next Scenario**: [Scenario 2: Multi-Site WAN Connectivity](scenario-02-multi-site-wan.md)
