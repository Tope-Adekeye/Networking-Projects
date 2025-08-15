# Lab 2: Inter-VLAN Routing Configuration

## 🎯 **Lab Objectives**
- Configure router-on-a-stick for inter-VLAN routing
- Implement VLAN trunking between switch and router
- Configure subinterfaces for multiple VLANs
- Test inter-VLAN communication and troubleshoot connectivity issues

## 🏗️ **Network Topology**

```
VLAN 10 (Sales)      ┌─── PC1 (192.168.10.10/24)
  192.168.10.0/24    │
                     │
VLAN 20 (Engineering)├─── PC2 (192.168.20.10/24)  
  192.168.20.0/24    │     
                     │     Trunk Link
VLAN 30 (Management) ├─── PC3 (192.168.30.10/24) ─── Switch1 ════ Router1
  192.168.30.0/24    │                              (Catalyst 2960)  (ISR 4331)
                     │                                     │
                     └─── PC4 (192.168.10.20/24)         │
                                                           │
                                                    Internet/WAN
                                                   (203.0.113.1/30)
```

## 📋 **Required Equipment**
- 1 x Cisco ISR 4331 Router (or equivalent)
- 1 x Cisco Catalyst 2960 Switch
- 4 x Generic PCs
- 1 x Server (for testing)
- Straight-through and crossover Ethernet cables

## 🔧 **Lab Tasks**

### **Task 1: Switch Configuration**

#### **Step 1: VLAN Creation and Port Assignment**
```cisco
Switch> enable
Switch# configure terminal
Switch(config)# hostname SW1

! Create VLANs
SW1(config)# vlan 10
SW1(config-vlan)# name Sales
SW1(config-vlan)# exit

SW1(config)# vlan 20
SW1(config-vlan)# name Engineering
SW1(config-vlan)# exit

SW1(config)# vlan 30
SW1(config-vlan)# name Management
SW1(config-vlan)# exit

! Configure access ports
SW1(config)# interface fa0/1
SW1(config-if)# switchport mode access
SW1(config-if)# switchport access vlan 10
SW1(config-if)# description "Sales PC1"
SW1(config-if)# exit

SW1(config)# interface fa0/2
SW1(config-if)# switchport mode access
SW1(config-if)# switchport access vlan 20
SW1(config-if)# description "Engineering PC2"
SW1(config-if)# exit

SW1(config)# interface fa0/3
SW1(config-if)# switchport mode access
SW1(config-if)# switchport access vlan 30
SW1(config-if)# description "Management PC3"
SW1(config-if)# exit

SW1(config)# interface fa0/4
SW1(config-if)# switchport mode access
SW1(config-if)# switchport access vlan 10
SW1(config-if)# description "Sales PC4"
SW1(config-if)# exit
```

#### **Step 2: Trunk Configuration**
```cisco
! Configure trunk port to router
SW1(config)# interface fa0/24
SW1(config-if)# switchport mode trunk
SW1(config-if)# switchport trunk native vlan 99
SW1(config-if)# switchport trunk allowed vlan 10,20,30
SW1(config-if)# description "Trunk to Router"
SW1(config-if)# exit

! Create native VLAN (best practice)
SW1(config)# vlan 99
SW1(config-vlan)# name Native
SW1(config-vlan)# exit
```

### **Task 2: Router Configuration**

#### **Step 1: Basic Router Setup**
```cisco
Router> enable
Router# configure terminal
Router(config)# hostname R1

! Configure the physical interface
R1(config)# interface gig0/0
R1(config-if)# no shutdown
R1(config-if)# description "Trunk to Switch"
R1(config-if)# exit
```

#### **Step 2: Subinterface Configuration (Router-on-a-Stick)**
```cisco
! Configure subinterface for VLAN 10 (Sales)
R1(config)# interface gig0/0.10
R1(config-subif)# description "Sales VLAN"
R1(config-subif)# encapsulation dot1Q 10
R1(config-subif)# ip address 192.168.10.1 255.255.255.0
R1(config-subif)# exit

! Configure subinterface for VLAN 20 (Engineering)
R1(config)# interface gig0/0.20
R1(config-subif)# description "Engineering VLAN"
R1(config-subif)# encapsulation dot1Q 20
R1(config-subif)# ip address 192.168.20.1 255.255.255.0
R1(config-subif)# exit

! Configure subinterface for VLAN 30 (Management)
R1(config)# interface gig0/0.30
R1(config-subif)# description "Management VLAN"
R1(config-subif)# encapsulation dot1Q 30
R1(config-subif)# ip address 192.168.30.1 255.255.255.0
R1(config-subif)# exit

! Configure native VLAN subinterface
R1(config)# interface gig0/0.99
R1(config-subif)# description "Native VLAN"
R1(config-subif)# encapsulation dot1Q 99 native
R1(config-subif)# exit
```

#### **Step 3: WAN Interface Configuration**
```cisco
! Configure WAN interface (Internet connectivity)
R1(config)# interface gig0/1
R1(config-if)# description "WAN Connection"
R1(config-if)# ip address 203.0.113.2 255.255.255.252
R1(config-if)# no shutdown
R1(config-if)# exit

! Configure default route
R1(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.1
```

### **Task 3: PC Configuration**

#### **Configure PC IP Addresses**
- **PC1 (Sales VLAN)**: 192.168.10.10/24, Gateway: 192.168.10.1
- **PC2 (Engineering VLAN)**: 192.168.20.10/24, Gateway: 192.168.20.1
- **PC3 (Management VLAN)**: 192.168.30.10/24, Gateway: 192.168.30.1
- **PC4 (Sales VLAN)**: 192.168.10.20/24, Gateway: 192.168.10.1

## 🔍 **Verification and Testing**

### **Switch Verification**
```cisco
! Verify VLAN configuration
SW1# show vlan brief

! Check trunk status
SW1# show interfaces trunk

! Verify MAC address table
SW1# show mac address-table

! Check interface status
SW1# show interfaces status
```

### **Router Verification**
```cisco
! Show IP interface brief
R1# show ip interface brief

! Verify subinterface configuration
R1# show interfaces gig0/0.10
R1# show interfaces gig0/0.20
R1# show interfaces gig0/0.30

! Check routing table
R1# show ip route

! Verify interface status
R1# show interfaces gig0/0
```

### **Connectivity Testing**

#### **Intra-VLAN Communication**
```bash
# From PC1 (VLAN 10)
ping 192.168.10.20  # Should reach PC4 (same VLAN)

# From PC2 (VLAN 20)
ping 192.168.20.1   # Should reach default gateway
```

#### **Inter-VLAN Communication**
```bash
# From PC1 (VLAN 10) to PC2 (VLAN 20)
ping 192.168.20.10  # Should work through router

# From PC3 (VLAN 30) to PC1 (VLAN 10)
ping 192.168.10.10  # Should work through router

# From any PC to WAN
ping 203.0.113.1    # Should reach WAN gateway
```

## 🛠️ **Advanced Configuration**

### **DHCP Configuration on Router**
```cisco
! Configure DHCP pools for each VLAN
R1(config)# ip dhcp excluded-address 192.168.10.1 192.168.10.10
R1(config)# ip dhcp pool SALES
R1(dhcp-config)# network 192.168.10.0 255.255.255.0
R1(dhcp-config)# default-router 192.168.10.1
R1(dhcp-config)# dns-server 8.8.8.8
R1(dhcp-config)# exit

R1(config)# ip dhcp excluded-address 192.168.20.1 192.168.20.10
R1(config)# ip dhcp pool ENGINEERING
R1(dhcp-config)# network 192.168.20.0 255.255.255.0
R1(dhcp-config)# default-router 192.168.20.1
R1(dhcp-config)# dns-server 8.8.8.8
R1(dhcp-config)# exit

R1(config)# ip dhcp excluded-address 192.168.30.1 192.168.30.10
R1(config)# ip dhcp pool MANAGEMENT
R1(dhcp-config)# network 192.168.30.0 255.255.255.0
R1(dhcp-config)# default-router 192.168.30.1
R1(dhcp-config)# dns-server 8.8.8.8
R1(dhcp-config)# exit
```

### **Access Control Lists (ACLs)**
```cisco
! Create ACL to restrict Management VLAN access
R1(config)# access-list 100 permit ip 192.168.30.0 0.0.0.255 any
R1(config)# access-list 100 deny ip 192.168.10.0 0.0.0.255 192.168.30.0 0.0.0.255
R1(config)# access-list 100 deny ip 192.168.20.0 0.0.0.255 192.168.30.0 0.0.0.255
R1(config)# access-list 100 permit ip any any

! Apply ACL to Management VLAN interface
R1(config)# interface gig0/0.30
R1(config-subif)# ip access-group 100 in
R1(config-subif)# exit
```

## 📊 **Performance Monitoring**

### **Traffic Analysis**
```cisco
! Monitor interface statistics
R1# show interfaces gig0/0 | include packets

! Check DHCP bindings
R1# show ip dhcp binding

! Monitor ACL hit counts
R1# show access-lists
```

### **Troubleshooting Commands**
```cisco
! Debug DHCP
R1# debug ip dhcp server packet
R1# debug ip dhcp server events

! Debug routing
R1# debug ip routing

! Show CDP neighbors
R1# show cdp neighbors detail
SW1# show cdp neighbors detail
```

## 🔧 **Troubleshooting Scenarios**

### **Scenario 1: No Inter-VLAN Communication**
**Symptoms**: PCs in different VLANs cannot communicate
**Troubleshooting Steps**:
1. Check trunk configuration on switch
2. Verify subinterface configuration on router
3. Confirm VLAN assignments on switch ports
4. Test gateway connectivity from each VLAN

```cisco
! Verification commands
SW1# show interfaces trunk
R1# show ip interface brief
R1# show ip route
```

### **Scenario 2: Trunk Not Operational**
**Symptoms**: Trunk link showing as down or not passing VLANs
**Troubleshooting Steps**:
1. Check physical connectivity
2. Verify trunk configuration on both ends
3. Confirm VLAN exists on both devices
4. Check for native VLAN mismatch

```cisco
! Debug commands
SW1# show interfaces fa0/24 switchport
SW1# show interfaces fa0/24 trunk
```

### **Scenario 3: DHCP Not Working**
**Symptoms**: PCs not receiving IP addresses automatically
**Troubleshooting Steps**:
1. Verify DHCP pool configuration
2. Check excluded addresses
3. Confirm IP helper-address if needed
4. Monitor DHCP bindings

```cisco
! DHCP troubleshooting
R1# show ip dhcp pool
R1# show ip dhcp binding
R1# show ip dhcp conflict
```

## 📝 **Lab Assessment**

### **Configuration Verification Checklist**
□ All VLANs created and properly named
□ Switch ports assigned to correct VLANs
□ Trunk link configured and operational
□ Router subinterfaces configured with correct VLANs
□ IP addresses assigned to all devices
□ Default gateways configured correctly

### **Functionality Testing Checklist**
□ Intra-VLAN communication working
□ Inter-VLAN communication working
□ Internet connectivity functional (if configured)
□ DHCP working (if configured)
□ ACLs functioning as designed (if configured)

### **Documentation Requirements**
□ Network diagram with IP addressing scheme
□ Complete device configurations
□ Testing results and verification outputs
□ Troubleshooting scenarios and resolutions

## 🎓 **Learning Outcomes**

After completing this lab, you should be able to:

□ **Configure inter-VLAN routing** using router-on-a-stick topology
□ **Implement VLAN trunking** between switches and routers
□ **Create and configure subinterfaces** for multiple VLANs
□ **Troubleshoot inter-VLAN connectivity** issues
□ **Apply security policies** using ACLs between VLANs
□ **Configure DHCP services** for multiple VLANs

---

**Previous Lab**: [Lab 1: Basic Switching Configuration](lab-01-basic-switching.md)  
**Next Lab**: [Lab 3: OSPF Dynamic Routing](lab-03-ospf-routing.md)
