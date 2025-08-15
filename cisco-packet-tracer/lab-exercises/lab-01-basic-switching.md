# Lab 1: Basic Switching Configuration

## 🎯 **Lab Objectives**
- Configure basic switch settings and management interface
- Implement port security and VLAN configurations
- Practice switch administration and monitoring commands
- Understand Layer 2 switching fundamentals

## 🏗️ **Network Topology**

```
PC1 (192.168.1.10/24) ──┐
                         │
PC2 (192.168.1.20/24) ──┼── Switch1 (Catalyst 2960) ── Management PC
                         │    (192.168.1.100/24)       (192.168.1.5/24)
PC3 (192.168.1.30/24) ──┘
```

## 📋 **Required Equipment**
- 1 x Cisco Catalyst 2960 Switch
- 4 x Generic PCs
- 4 x Straight-through Ethernet cables

## 🔧 **Lab Tasks**

### **Task 1: Basic Switch Configuration**

#### **Step 1: Initial Setup**
```cisco
Switch> enable
Switch# configure terminal

! Set hostname
Switch(config)# hostname SW1

! Configure management VLAN interface
SW1(config)# interface vlan1
SW1(config-if)# ip address 192.168.1.100 255.255.255.0
SW1(config-if)# no shutdown
SW1(config-if)# exit

! Set default gateway
SW1(config)# ip default-gateway 192.168.1.1

! Configure console password
SW1(config)# line console 0
SW1(config-line)# password cisco
SW1(config-line)# login
SW1(config-line)# exit

! Configure enable password
SW1(config)# enable secret class
```

#### **Step 2: Interface Configuration**
```cisco
! Configure access ports
SW1(config)# interface range fa0/1-3
SW1(config-if-range)# switchport mode access
SW1(config-if-range)# switchport access vlan 1
SW1(config-if-range)# no shutdown
SW1(config-if-range)# exit

! Configure port descriptions
SW1(config)# interface fa0/1
SW1(config-if)# description "PC1 Connection"
SW1(config-if)# exit

SW1(config)# interface fa0/2
SW1(config-if)# description "PC2 Connection"
SW1(config-if)# exit

SW1(config)# interface fa0/3
SW1(config-if)# description "PC3 Connection"
SW1(config-if)# exit
```

### **Task 2: Port Security Configuration**

```cisco
! Configure port security on Fa0/1
SW1(config)# interface fa0/1
SW1(config-if)# switchport port-security
SW1(config-if)# switchport port-security maximum 1
SW1(config-if)# switchport port-security mac-address sticky
SW1(config-if)# switchport port-security violation restrict
SW1(config-if)# exit

! Apply port security to other ports
SW1(config)# interface range fa0/2-3
SW1(config-if-range)# switchport port-security
SW1(config-if-range)# switchport port-security maximum 1
SW1(config-if-range)# switchport port-security mac-address sticky
SW1(config-if-range)# switchport port-security violation shutdown
SW1(config-if-range)# exit
```

### **Task 3: VLAN Configuration**

```cisco
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

! Assign ports to VLANs
SW1(config)# interface fa0/1
SW1(config-if)# switchport access vlan 10
SW1(config-if)# exit

SW1(config)# interface fa0/2
SW1(config-if)# switchport access vlan 20
SW1(config-if)# exit

SW1(config)# interface fa0/3
SW1(config-if)# switchport access vlan 30
SW1(config-if)# exit
```

## 🔍 **Verification Commands**

### **Basic Switch Information**
```cisco
! Show running configuration
SW1# show running-config

! Show interface status
SW1# show interfaces status

! Show VLAN information
SW1# show vlan brief

! Show MAC address table
SW1# show mac address-table

! Show port security information
SW1# show port-security
SW1# show port-security interface fa0/1
```

### **Interface Statistics**
```cisco
! Show interface details
SW1# show interfaces fa0/1

! Show interface counters
SW1# show interfaces fa0/1 counters

! Show CDP neighbors (if enabled)
SW1# show cdp neighbors
```

## 📊 **Testing and Troubleshooting**

### **Connectivity Testing**
1. **PC to PC Communication**:
   - Test ping between PCs in same VLAN
   - Verify PCs in different VLANs cannot communicate

2. **Management Access**:
   - Telnet to switch management IP
   - SSH access (if configured)

### **Port Security Testing**
```cisco
! Test port security violation
! 1. Connect second device to secured port
! 2. Observe violation counter increase
! 3. Check security status

SW1# show port-security interface fa0/1
SW1# show port-security address
```

### **Common Troubleshooting Commands**
```cisco
! Check for errors
SW1# show interfaces | include error

! Monitor real-time interface status
SW1# show interfaces fa0/1 | include line protocol

! Clear MAC address table
SW1# clear mac address-table dynamic

! Reset port security
SW1(config)# interface fa0/2
SW1(config-if)# shutdown
SW1(config-if)# no shutdown
```

## 📝 **Lab Questions**

### **Configuration Questions**
1. What is the difference between `switchport mode access` and `switchport mode trunk`?
2. How does port security protect against MAC address flooding attacks?
3. What happens when a port security violation occurs with different violation modes?

### **Verification Questions**
1. How can you verify that VLANs are properly configured?
2. What command shows the MAC addresses learned on each port?
3. How do you check if an interface is up/up?

### **Troubleshooting Scenarios**
1. **Scenario 1**: PC1 cannot communicate with PC2
   - Check VLAN assignments
   - Verify interface status
   - Confirm IP configurations

2. **Scenario 2**: Port security violation occurred
   - Identify violation type
   - Check learned MAC addresses
   - Reset interface if needed

3. **Scenario 3**: Switch management interface unreachable
   - Verify VLAN 1 configuration
   - Check default gateway setting
   - Confirm physical connectivity

## 🎓 **Learning Outcomes**

After completing this lab, you should be able to:

□ **Configure basic switch settings** including hostname, passwords, and management interface
□ **Implement port security** to prevent unauthorized access
□ **Create and assign VLANs** for network segmentation
□ **Use verification commands** to confirm configuration
□ **Troubleshoot common switching issues** systematically

## 🔄 **Advanced Exercises**

### **Extension Activities**
1. **Implement SSH access** instead of Telnet for secure management
2. **Configure port channels** for link aggregation
3. **Set up DHCP snooping** for additional security
4. **Implement 802.1X** for port-based authentication

### **Configuration Templates**
```cisco
! SSH Configuration Template
SW1(config)# ip domain-name lab.local
SW1(config)# crypto key generate rsa
SW1(config)# username admin privilege 15 secret cisco123
SW1(config)# line vty 0 15
SW1(config-line)# transport input ssh
SW1(config-line)# login local
SW1(config-line)# exit
```

## 💾 **Save Configuration**
```cisco
! Save running configuration to startup
SW1# copy running-config startup-config

! Backup configuration to TFTP (optional)
SW1# copy running-config tftp://192.168.1.254/SW1-backup.cfg
```

## 📋 **Lab Completion Checklist**

□ Basic switch configuration completed
□ Management interface configured and accessible
□ Port security implemented on all access ports
□ VLANs created and assigned to appropriate ports
□ All verification commands executed successfully
□ Connectivity testing between PCs completed
□ Configuration saved to startup-config
□ Lab questions answered
□ Troubleshooting scenarios practiced

---

**Next Lab**: [Lab 2: Inter-VLAN Routing Configuration](lab-02-inter-vlan-routing.md)
