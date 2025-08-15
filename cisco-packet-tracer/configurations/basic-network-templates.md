# Cisco Packet Tracer Configuration Templates

## 🎯 **Purpose**
This document provides standardized configuration templates for common networking scenarios in Cisco Packet Tracer. These templates ensure consistent configurations and best practices across all lab exercises.

## 🔧 **Basic Device Templates**

### **Switch Configuration Template**
```cisco
! Basic Switch Configuration Template
! Replace <HOSTNAME> with actual switch name
! Replace <MGMT_IP> with management IP address

Switch> enable
Switch# configure terminal
Switch(config)# hostname <HOSTNAME>

! Management interface
Switch(config)# interface vlan1
Switch(config-if)# ip address <MGMT_IP> 255.255.255.0
Switch(config-if)# no shutdown
Switch(config-if)# exit

! Default gateway
Switch(config)# ip default-gateway <GATEWAY_IP>

! Console password
Switch(config)# line console 0
Switch(config-line)# password cisco
Switch(config-line)# login
Switch(config-line)# logging synchronous
Switch(config-line)# exec-timeout 30 0
Switch(config-line)# exit

! VTY lines (Telnet/SSH)
Switch(config)# line vty 0 15
Switch(config-line)# password cisco
Switch(config-line)# login
Switch(config-line)# transport input telnet ssh
Switch(config-line)# exit

! Enable password
Switch(config)# enable secret class

! Banner
Switch(config)# banner motd #
****************************************************
* WARNING: Unauthorized access is prohibited!      *
* This device is monitored for security purposes.  *
****************************************************
#

! Basic security
Switch(config)# service password-encryption
Switch(config)# no ip http-server
Switch(config)# no ip http-secure-server

! Save configuration
Switch(config)# exit
Switch# copy running-config startup-config
```

### **Router Configuration Template**
```cisco
! Basic Router Configuration Template
! Replace <HOSTNAME> with actual router name

Router> enable
Router# configure terminal
Router(config)# hostname <HOSTNAME>

! Console password
Router(config)# line console 0
Router(config-line)# password cisco
Router(config-line)# login
Router(config-line)# logging synchronous
Router(config-line)# exec-timeout 30 0
Router(config-line)# exit

! VTY lines (Telnet/SSH)
Router(config)# line vty 0 4
Router(config-line)# password cisco
Router(config-line)# login
Router(config-line)# transport input telnet ssh
Router(config-line)# exit

! Enable password
Router(config)# enable secret class

! Banner
Router(config)# banner motd #
****************************************************
* WARNING: Unauthorized access is prohibited!      *
* This device is monitored for security purposes.  *
****************************************************
#

! Basic security
Router(config)# service password-encryption
Router(config)# no ip http-server
Router(config)# no ip http-secure-server

! DNS settings
Router(config)# ip domain-name lab.local
Router(config)# ip name-server 8.8.8.8

! Disable unused services
Router(config)# no service tcp-small-servers
Router(config)# no service udp-small-servers
Router(config)# no service finger
Router(config)# no service dhcp
Router(config)# no cdp run

! Save configuration
Router(config)# exit
Router# copy running-config startup-config
```

## 🌐 **Network Topology Templates**

### **Small Office Network Template**
```
Internet
    │
    │ (WAN Link)
    │
┌───▼───┐
│Router │ <- Default Gateway
│  R1   │    192.168.1.1/24
└───┬───┘
    │ (LAN Link)
    │
┌───▼───┐
│Switch │ <- Layer 2 Switch
│  SW1  │    192.168.1.100/24 (Management)
└─┬─┬─┬─┘
  │ │ │
  │ │ └── PC3 (192.168.1.30/24)
  │ └──── PC2 (192.168.1.20/24)
  └────── PC1 (192.168.1.10/24)

IP Addressing Scheme:
- Network: 192.168.1.0/24
- Gateway: 192.168.1.1
- DHCP Pool: 192.168.1.10-100
- Switch Mgmt: 192.168.1.254
```

### **Multi-VLAN Enterprise Template**
```
                    Internet
                        │
                    ┌───▼───┐
                    │Router │
                    │  R1   │
                    └───┬───┘
                        │ (Trunk)
    ┌───────────────────┼───────────────────┐
    │                   │                   │
┌───▼───┐           ┌───▼───┐           ┌───▼───┐
│Switch │           │Switch │           │Switch │
│  SW1  │◄─────────►│  SW2  │◄─────────►│  SW3  │
└─┬─┬─┬─┘           └─┬─┬─┬─┘           └─┬─┬─┬─┘
  │ │ │               │ │ │               │ │ │
VLAN 10             VLAN 20             VLAN 30
Sales Dept          Engineering         Management
192.168.10.0/24     192.168.20.0/24     192.168.30.0/24
```

### **WAN Connectivity Template**
```
Site A                                          Site B
LAN: 192.168.1.0/24                           LAN: 192.168.2.0/24

┌───────┐                                      ┌───────┐
│  R1   │                                      │  R2   │
│Site A │◄────── WAN Link ──────────────────►│Site B │
└───┬───┘        Serial/Frame Relay           └───┬───┘
    │            or VPN Tunnel                    │
┌───▼───┐                                    ┌───▼───┐
│  SW1  │                                    │  SW2  │
└─┬─┬─┬─┘                                    └─┬─┬─┬─┘
  │ │ │                                        │ │ │
Site A Users                                Site B Users
```

## 🔒 **Security Configuration Templates**

### **Basic Port Security Template**
```cisco
! Port Security Configuration
Switch(config)# interface range fa0/1-24
Switch(config-if-range)# switchport mode access
Switch(config-if-range)# switchport port-security
Switch(config-if-range)# switchport port-security maximum 2
Switch(config-if-range)# switchport port-security mac-address sticky
Switch(config-if-range)# switchport port-security violation restrict
Switch(config-if-range)# exit

! Critical ports (servers/infrastructure)
Switch(config)# interface range fa0/22-24
Switch(config-if-range)# switchport port-security maximum 1
Switch(config-if-range)# switchport port-security violation shutdown
Switch(config-if-range)# exit
```

### **Basic ACL Template**
```cisco
! Standard ACL - Block specific network
Router(config)# access-list 10 deny 192.168.100.0 0.0.0.255
Router(config)# access-list 10 permit any

! Extended ACL - Web traffic control
Router(config)# access-list 100 permit tcp 192.168.1.0 0.0.0.255 any eq 80
Router(config)# access-list 100 permit tcp 192.168.1.0 0.0.0.255 any eq 443
Router(config)# access-list 100 permit icmp any any
Router(config)# access-list 100 deny ip any any

! Apply ACL to interface
Router(config)# interface gig0/1
Router(config-if)# ip access-group 100 out
Router(config-if)# exit
```

### **SSH Configuration Template**
```cisco
! SSH Configuration
Router(config)# ip domain-name company.local
Router(config)# crypto key generate rsa general-keys modulus 2048
Router(config)# username admin privilege 15 secret cisco123
Router(config)# username operator privilege 1 secret user123

! VTY configuration for SSH
Router(config)# line vty 0 4
Router(config-line)# transport input ssh
Router(config-line)# login local
Router(config-line)# exec-timeout 10 0
Router(config-line)# exit

! SSH version and settings
Router(config)# ip ssh version 2
Router(config)# ip ssh time-out 60
Router(config)# ip ssh authentication-retries 3
```

## 📶 **VLAN Configuration Templates**

### **Standard VLAN Setup**
```cisco
! Create VLANs
Switch(config)# vlan 10
Switch(config-vlan)# name Sales
Switch(config-vlan)# exit

Switch(config)# vlan 20
Switch(config-vlan)# name Engineering
Switch(config-vlan)# exit

Switch(config)# vlan 30
Switch(config-vlan)# name Management
Switch(config-vlan)# exit

Switch(config)# vlan 99
Switch(config-vlan)# name Native
Switch(config-vlan)# exit

! Access port configuration
Switch(config)# interface range fa0/1-8
Switch(config-if-range)# switchport mode access
Switch(config-if-range)# switchport access vlan 10
Switch(config-if-range)# spanning-tree portfast
Switch(config-if-range)# exit

Switch(config)# interface range fa0/9-16
Switch(config-if-range)# switchport mode access
Switch(config-if-range)# switchport access vlan 20
Switch(config-if-range)# spanning-tree portfast
Switch(config-if-range)# exit

! Trunk configuration
Switch(config)# interface fa0/24
Switch(config-if)# switchport mode trunk
Switch(config-if)# switchport trunk native vlan 99
Switch(config-if)# switchport trunk allowed vlan 10,20,30
Switch(config-if)# exit
```

### **Voice VLAN Template**
```cisco
! Configure voice VLAN
Switch(config)# vlan 100
Switch(config-vlan)# name Voice
Switch(config-vlan)# exit

! Access port with voice VLAN
Switch(config)# interface range fa0/1-12
Switch(config-if-range)# switchport mode access
Switch(config-if-range)# switchport access vlan 10
Switch(config-if-range)# switchport voice vlan 100
Switch(config-if-range)# spanning-tree portfast
Switch(config-if-range)# exit
```

## 🌍 **Routing Protocol Templates**

### **RIP Configuration Template**
```cisco
! RIP Version 2 Configuration
Router(config)# router rip
Router(config-router)# version 2
Router(config-router)# network 192.168.1.0
Router(config-router)# network 192.168.2.0
Router(config-router)# no auto-summary
Router(config-router)# passive-interface default
Router(config-router)# no passive-interface gig0/0
Router(config-router)# no passive-interface serial0/1/0
Router(config-router)# exit
```

### **EIGRP Configuration Template**
```cisco
! EIGRP Configuration
Router(config)# router eigrp 100
Router(config-router)# network 192.168.1.0 0.0.0.255
Router(config-router)# network 192.168.2.0 0.0.0.255
Router(config-router)# network 10.0.0.0 0.0.0.3
Router(config-router)# eigrp router-id 1.1.1.1
Router(config-router)# passive-interface default
Router(config-router)# no passive-interface gig0/0
Router(config-router)# no passive-interface serial0/1/0
Router(config-router)# exit
```

### **OSPF Single Area Template**
```cisco
! OSPF Single Area Configuration
Router(config)# router ospf 1
Router(config-router)# router-id 1.1.1.1
Router(config-router)# network 192.168.1.0 0.0.0.255 area 0
Router(config-router)# network 192.168.2.0 0.0.0.255 area 0
Router(config-router)# network 10.0.0.0 0.0.0.3 area 0
Router(config-router)# passive-interface default
Router(config-router)# no passive-interface gig0/0
Router(config-router)# no passive-interface serial0/1/0
Router(config-router)# exit
```

## 🌐 **DHCP Configuration Templates**

### **Router DHCP Server Template**
```cisco
! DHCP Pool Configuration
Router(config)# ip dhcp excluded-address 192.168.1.1 192.168.1.10
Router(config)# ip dhcp excluded-address 192.168.1.250 192.168.1.254

Router(config)# ip dhcp pool LAN_POOL
Router(dhcp-config)# network 192.168.1.0 255.255.255.0
Router(dhcp-config)# default-router 192.168.1.1
Router(dhcp-config)# dns-server 8.8.8.8 8.8.4.4
Router(dhcp-config)# domain-name company.local
Router(dhcp-config)# lease 0 12 0
Router(dhcp-config)# exit

! DHCP for multiple VLANs
Router(config)# ip dhcp pool VLAN10_POOL
Router(dhcp-config)# network 192.168.10.0 255.255.255.0
Router(dhcp-config)# default-router 192.168.10.1
Router(dhcp-config)# dns-server 8.8.8.8
Router(dhcp-config)# exit

Router(config)# ip dhcp pool VLAN20_POOL
Router(dhcp-config)# network 192.168.20.0 255.255.255.0
Router(dhcp-config)# default-router 192.168.20.1
Router(dhcp-config)# dns-server 8.8.8.8
Router(dhcp-config)# exit
```

## 🔄 **NAT Configuration Templates**

### **PAT (NAT Overload) Template**
```cisco
! PAT Configuration
Router(config)# access-list 1 permit 192.168.1.0 0.0.0.255
Router(config)# access-list 1 permit 192.168.10.0 0.0.0.255
Router(config)# access-list 1 permit 192.168.20.0 0.0.0.255

Router(config)# ip nat inside source list 1 interface gig0/1 overload

! Configure inside interfaces
Router(config)# interface gig0/0
Router(config-if)# ip nat inside
Router(config-if)# exit

Router(config)# interface gig0/0.10
Router(config-subif)# ip nat inside
Router(config-subif)# exit

! Configure outside interface
Router(config)# interface gig0/1
Router(config-if)# ip nat outside
Router(config-if)# exit
```

### **Static NAT Template**
```cisco
! Static NAT for servers
Router(config)# ip nat inside source static 192.168.1.100 203.0.113.10
Router(config)# ip nat inside source static 192.168.1.101 203.0.113.11

! Port forwarding (PAT)
Router(config)# ip nat inside source static tcp 192.168.1.100 80 203.0.113.5 8080
Router(config)# ip nat inside source static tcp 192.168.1.100 443 203.0.113.5 8443
```

## 📊 **Monitoring and Verification Templates**

### **Standard Verification Commands**
```cisco
! Interface verification
show ip interface brief
show interfaces status
show interfaces trunk

! Routing verification
show ip route
show ip protocols
show ip ospf neighbor
show ip eigrp neighbors

! VLAN verification
show vlan brief
show interfaces switchport

! Security verification
show port-security
show access-lists
show ip nat translations

! General troubleshooting
show running-config
show startup-config
show version
show processes cpu
show memory
```

### **Debug Commands (Use Carefully)**
```cisco
! OSPF debugging
debug ip ospf hello
debug ip ospf adj
debug ip ospf packet

! EIGRP debugging
debug eigrp packets
debug ip eigrp

! General debugging
debug ip routing
debug ip packet
debug ip icmp

! Remember to disable debugging
no debug all
undebug all
```

## 🔧 **Best Practices Checklist**

### **Security Best Practices**
□ Enable password encryption (`service password-encryption`)
□ Configure strong enable secret passwords
□ Disable unused services
□ Configure port security on access ports
□ Implement ACLs for traffic filtering
□ Use SSH instead of Telnet
□ Configure banner messages

### **Performance Best Practices**
□ Configure appropriate VLAN design
□ Use passive interfaces in routing protocols
□ Implement route summarization
□ Configure spanning-tree portfast on access ports
□ Set appropriate interface descriptions
□ Configure logging and SNMP for monitoring

### **Documentation Best Practices**
□ Use consistent naming conventions
□ Document all IP addressing schemes
□ Maintain configuration backups
□ Create network diagrams
□ Document change procedures
□ Keep configuration templates updated

---

**Note**: These templates provide a starting point for common configurations. Always adapt them to specific network requirements and security policies.
