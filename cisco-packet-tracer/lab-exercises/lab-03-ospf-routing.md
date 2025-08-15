# Lab 3: OSPF Dynamic Routing Configuration

## 🎯 **Lab Objectives**
- Configure OSPF (Open Shortest Path First) routing protocol
- Implement multi-area OSPF topology
- Configure OSPF authentication and route summarization
- Analyze OSPF neighbor relationships and LSA propagation
- Troubleshoot OSPF routing issues

## 🏗️ **Network Topology**

```
                    Area 0 (Backbone)
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
 Area 1               Area 0               Area 2
172.16.1.0/24      192.168.0.0/30      172.16.2.0/24
    │               192.168.0.4/30          │
    │               192.168.0.8/30          │
    │                    │                  │
   R1 ──────────────── R2 ──────────────── R3
   │                    │                  │
   │                    │                  │
PC1-A             Internet/WAN           PC3-A
PC1-B              Gateway              PC3-B
172.16.1.10/24    203.0.113.1/30       172.16.2.10/24
172.16.1.20/24                         172.16.2.20/24
```

## 📋 **Required Equipment**
- 3 x Cisco ISR 4331 Routers (R1, R2, R3)
- 4 x Generic PCs
- 1 x Server (Internet simulation)
- Serial and Ethernet cables

## 🔧 **Lab Tasks**

### **Task 1: Basic Router Configuration**

#### **Router R1 (Area 1) Configuration**
```cisco
Router> enable
Router# configure terminal
Router(config)# hostname R1

! Configure LAN interface
R1(config)# interface gig0/0
R1(config-if)# description "LAN Area 1"
R1(config-if)# ip address 172.16.1.1 255.255.255.0
R1(config-if)# no shutdown
R1(config-if)# exit

! Configure WAN interface to R2
R1(config)# interface serial0/1/0
R1(config-if)# description "Link to R2"
R1(config-if)# ip address 192.168.0.1 255.255.255.252
R1(config-if)# clock rate 128000
R1(config-if)# no shutdown
R1(config-if)# exit

! Configure loopback for Router ID
R1(config)# interface loopback0
R1(config-if)# description "Router ID"
R1(config-if)# ip address 1.1.1.1 255.255.255.255
R1(config-if)# exit
```

#### **Router R2 (Area 0 - Backbone) Configuration**
```cisco
Router> enable
Router# configure terminal
Router(config)# hostname R2

! Configure interface to R1
R2(config)# interface serial0/1/0
R2(config-if)# description "Link to R1"
R2(config-if)# ip address 192.168.0.2 255.255.255.252
R2(config-if)# no shutdown
R2(config-if)# exit

! Configure interface to R3
R2(config)# interface serial0/1/1
R2(config-if)# description "Link to R3"
R2(config-if)# ip address 192.168.0.5 255.255.255.252
R2(config-if)# clock rate 128000
R2(config-if)# no shutdown
R2(config-if)# exit

! Configure WAN interface
R2(config)# interface gig0/1
R2(config-if)# description "WAN Connection"
R2(config-if)# ip address 203.0.113.2 255.255.255.252
R2(config-if)# no shutdown
R2(config-if)# exit

! Configure loopback for Router ID
R2(config)# interface loopback0
R2(config-if)# description "Router ID"
R2(config-if)# ip address 2.2.2.2 255.255.255.255
R2(config-if)# exit

! Default route to Internet
R2(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.1
```

#### **Router R3 (Area 2) Configuration**
```cisco
Router> enable
Router# configure terminal
Router(config)# hostname R3

! Configure LAN interface
R3(config)# interface gig0/0
R3(config-if)# description "LAN Area 2"
R3(config-if)# ip address 172.16.2.1 255.255.255.0
R3(config-if)# no shutdown
R3(config-if)# exit

! Configure WAN interface to R2
R3(config)# interface serial0/1/1
R3(config-if)# description "Link to R2"
R3(config-if)# ip address 192.168.0.6 255.255.255.252
R3(config-if)# no shutdown
R3(config-if)# exit

! Configure loopback for Router ID
R3(config)# interface loopback0
R3(config-if)# description "Router ID"
R3(config-if)# ip address 3.3.3.3 255.255.255.255
R3(config-if)# exit
```

### **Task 2: OSPF Configuration**

#### **Router R1 OSPF Setup**
```cisco
! Enable OSPF process
R1(config)# router ospf 1
R1(config-router)# router-id 1.1.1.1
R1(config-router)# log-adjacency-changes

! Configure Area 1 networks
R1(config-router)# network 172.16.1.0 0.0.0.255 area 1
R1(config-router)# network 192.168.0.0 0.0.0.3 area 0
R1(config-router)# network 1.1.1.1 0.0.0.0 area 1
R1(config-router)# exit

! Configure interface OSPF settings
R1(config)# interface gig0/0
R1(config-if)# ip ospf priority 255
R1(config-if)# ip ospf hello-interval 10
R1(config-if)# ip ospf dead-interval 40
R1(config-if)# exit
```

#### **Router R2 OSPF Setup**
```cisco
! Enable OSPF process
R2(config)# router ospf 1
R2(config-router)# router-id 2.2.2.2
R2(config-router)# log-adjacency-changes

! Configure Area 0 networks (Backbone)
R2(config-router)# network 192.168.0.0 0.0.0.3 area 0
R2(config-router)# network 192.168.0.4 0.0.0.3 area 0
R2(config-router)# network 2.2.2.2 0.0.0.0 area 0

! Redistribute default route
R2(config-router)# default-information originate
R2(config-router)# exit
```

#### **Router R3 OSPF Setup**
```cisco
! Enable OSPF process
R3(config)# router ospf 1
R3(config-router)# router-id 3.3.3.3
R3(config-router)# log-adjacency-changes

! Configure Area 2 networks
R3(config-router)# network 172.16.2.0 0.0.0.255 area 2
R3(config-router)# network 192.168.0.4 0.0.0.3 area 0
R3(config-router)# network 3.3.3.3 0.0.0.0 area 2
R3(config-router)# exit

! Configure interface OSPF settings
R3(config)# interface gig0/0
R3(config-if)# ip ospf priority 255
R3(config-if)# ip ospf hello-interval 10
R3(config-if)# ip ospf dead-interval 40
R3(config-if)# exit
```

### **Task 3: OSPF Authentication**

#### **Configure MD5 Authentication**
```cisco
! R1 Configuration
R1(config)# interface serial0/1/0
R1(config-if)# ip ospf message-digest-key 1 md5 cisco123
R1(config-if)# exit
R1(config)# router ospf 1
R1(config-router)# area 0 authentication message-digest
R1(config-router)# exit

! R2 Configuration
R2(config)# interface serial0/1/0
R2(config-if)# ip ospf message-digest-key 1 md5 cisco123
R2(config-if)# exit
R2(config)# interface serial0/1/1
R2(config-if)# ip ospf message-digest-key 1 md5 cisco123
R2(config-if)# exit
R2(config)# router ospf 1
R2(config-router)# area 0 authentication message-digest
R2(config-router)# exit

! R3 Configuration
R3(config)# interface serial0/1/1
R3(config-if)# ip ospf message-digest-key 1 md5 cisco123
R3(config-if)# exit
R3(config)# router ospf 1
R3(config-router)# area 0 authentication message-digest
R3(config-router)# exit
```

### **Task 4: Route Summarization**

#### **Configure Area Border Router (ABR) Summarization**
```cisco
! R1 - Summarize Area 1 routes
R1(config)# router ospf 1
R1(config-router)# area 1 range 172.16.1.0 255.255.255.0
R1(config-router)# exit

! R3 - Summarize Area 2 routes
R3(config)# router ospf 1
R3(config-router)# area 2 range 172.16.2.0 255.255.255.0
R3(config-router)# exit
```

## 🔍 **Verification and Monitoring**

### **OSPF Neighbor Verification**
```cisco
! Check OSPF neighbors
R1# show ip ospf neighbor
R2# show ip ospf neighbor
R3# show ip ospf neighbor

! Detailed neighbor information
R1# show ip ospf neighbor detail
```

### **OSPF Database Analysis**
```cisco
! View OSPF database
R1# show ip ospf database
R2# show ip ospf database
R3# show ip ospf database

! Specific LSA types
R2# show ip ospf database router
R2# show ip ospf database network
R2# show ip ospf database summary
```

### **OSPF Interface Information**
```cisco
! Show OSPF interfaces
R1# show ip ospf interface
R1# show ip ospf interface brief

! Specific interface details
R1# show ip ospf interface gig0/0
```

### **Routing Table Verification**
```cisco
! Check routing table
R1# show ip route
R1# show ip route ospf

! Specific route information
R1# show ip route 172.16.2.0
```

## 📊 **Performance Analysis**

### **OSPF Metrics and Costs**
```cisco
! View interface costs
R1# show ip ospf interface | include Cost

! Modify interface cost
R1(config)# interface gig0/0
R1(config-if)# ip ospf cost 10
R1(config-if)# exit

! Auto-cost reference bandwidth
R1(config)# router ospf 1
R1(config-router)# auto-cost reference-bandwidth 10000
R1(config-router)# exit
```

### **OSPF Timers Optimization**
```cisco
! Configure hello and dead intervals
R1(config)# interface gig0/0
R1(config-if)# ip ospf hello-interval 5
R1(config-if)# ip ospf dead-interval 20
R1(config-if)# exit

! SPF throttling
R1(config)# router ospf 1
R1(config-router)# timers throttle spf 1000 5000 30000
R1(config-router)# exit
```

## 🛠️ **Advanced OSPF Features**

### **Virtual Links (if needed)**
```cisco
! If Area 0 connectivity is broken
R1(config)# router ospf 1
R1(config-router)# area 1 virtual-link 2.2.2.2
R1(config-router)# exit

R2(config)# router ospf 1
R2(config-router)# area 1 virtual-link 1.1.1.1
R2(config-router)# exit
```

### **Stub Area Configuration**
```cisco
! Configure Area 1 as stub
R1(config)# router ospf 1
R1(config-router)# area 1 stub
R1(config-router)# exit

! Any other routers in Area 1 must also be configured as stub
```

### **OSPF LSA Filtering**
```cisco
! Filter LSA Type 3 into Area 1
R1(config)# router ospf 1
R1(config-router)# area 1 filter-list prefix FILTER-IN in
R1(config-router)# exit

R1(config)# ip prefix-list FILTER-IN deny 172.16.2.0/24
R1(config)# ip prefix-list FILTER-IN permit 0.0.0.0/0 le 32
```

## 🔧 **Troubleshooting OSPF**

### **Common OSPF Issues**

#### **Neighbor Adjacency Problems**
```cisco
! Debug OSPF adjacency
R1# debug ip ospf adj

! Check for common issues:
! 1. Mismatched area IDs
! 2. Mismatched authentication
! 3. Mismatched hello/dead timers
! 4. Mismatched network types

! Verify configuration
R1# show running-config | section router ospf
```

#### **Authentication Failures**
```cisco
! Debug OSPF authentication
R1# debug ip ospf packet

! Common authentication issues:
! 1. Mismatched key IDs
! 2. Mismatched passwords
! 3. Authentication not enabled on all interfaces
```

#### **Routing Issues**
```cisco
! Check SPF calculation
R1# show ip ospf statistics

! Debug OSPF route calculation
R1# debug ip ospf spf

! Check LSA propagation
R1# debug ip ospf lsa-generation
R1# debug ip ospf flood
```

### **OSPF Monitoring Commands**
```cisco
! Monitor OSPF events
R1# show ip ospf events
R1# show ip ospf flood-list
R1# show ip ospf request-list
R1# show ip ospf retransmission-list

! Check OSPF timers
R1# show ip ospf interface | include Timer
```

## 📝 **Lab Verification Checklist**

### **Configuration Verification**
□ All routers have correct OSPF process ID and router ID
□ Network statements match interface addressing
□ Area assignments are correct
□ Authentication is configured and working
□ Route summarization is implemented

### **Functionality Testing**
□ OSPF neighbor adjacencies are established
□ All networks appear in routing tables
□ End-to-end connectivity works
□ Default route propagation functions
□ Failover and reconvergence work properly

### **Performance Optimization**
□ OSPF costs are optimized for desired paths
□ Hello/Dead timers are appropriate
□ SPF throttling is configured
□ Route summarization reduces database size

## 🎓 **Learning Outcomes**

After completing this lab, you should be able to:

□ **Configure multi-area OSPF** topology
□ **Implement OSPF authentication** for security
□ **Configure route summarization** to optimize routing tables
□ **Analyze OSPF neighbor relationships** and LSA propagation
□ **Troubleshoot OSPF routing issues** systematically
□ **Optimize OSPF performance** using timers and costs

## 📈 **Performance Metrics**

### **Convergence Time Analysis**
- **Initial convergence**: Time from network startup to full adjacency
- **Failure detection**: Hello/Dead timer effectiveness
- **Reconvergence**: Time to find alternate paths after link failure
- **SPF calculation**: Database size impact on calculation time

### **Scalability Considerations**
- **Database size**: Number of LSAs in each area
- **Memory usage**: Router resource utilization
- **CPU utilization**: SPF calculation frequency
- **Bandwidth usage**: Hello packets and LSA updates

---

**Previous Lab**: [Lab 2: Inter-VLAN Routing Configuration](lab-02-inter-vlan-routing.md)  
**Next Lab**: [Lab 4: Network Address Translation (NAT)](lab-04-nat-configuration.md)
