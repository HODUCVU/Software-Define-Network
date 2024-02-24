# Exercise 1
## Group members:
* Ho Duc Vu - 106200284 
* Nguyen Minh Phuong - 106200241
* Huynh Vu Dinh Phuong - 106200240

# Topic
* Start a topology with 1 switch and 4 hosts
* Manage the flow entries in the created network manually using 'ovs-ofctl' command
	* Check current status of the switch
	* Check flow entries in the switch and modify them (add/remove)
	* Implementing some basic forwarding entries with 'ovs-ofctl' command: Host 1 can send packet to any host, host 2 can sen packets to host 4, drop all packets from host 3
		* Use port number information
		* Use MAC address information
		* Use IP address information
# Solution

## Start a topology with 1 switch and 4 hosts
### Code

```
sudo mn --topo single,4 --controller=none --mac
```
> --topo single,4: Use to create a switch and 4 host.\
> --controller=none: No controller.\
> --mac: Assign MAC address from 00:00:00:00:00:01 to 00:00:00:00:00:04 for host 1 to host 4.
### Result
![](Result1.png)

## Manage the flow entries in the created network mmmanually using 'ovs-ofctl'

### Check curren status of the switch
#### Code
Show status current of switch 1
```
sh ovs-ofctl show s1
```
#### Result
![](CurrentStatusOfSwitch.png)

### Check flow entries in the switch and modify them (add/remove)
#### Show table flows of switch 1
```
sh ovs-ofctl dump-flows s1
```
=> Result: Table is empty
#### Modify table flows
##### Code
```
sh ovs-ofctl add-flow s1 priority=1000,in_port=1,actions=output:2,3,4
sh ovs-ofctl add-flow s1 priority=1000,in_port=2,actions=output:1,3,4
sh ovs-ofctl add-flow s1 priority=1000,in_port=3,actions=output:1,2,4
sh ovs-ofctl add-flow s1 priority=1000,in_port=4,actions=output:1,2,3
// Show table flows and ping to check connect between hosts
sh ovs-ofctl dump-flows s1
pingall
```
##### Result
![](AddTableFlows.png)

### Implementing some basic forwarding entries
* Host 1 can send packet to any host.
* Host 2 can send packets to host 4.
* Drop all packets from host 3.
* **=> To host 1 can send packets to host 3 but host 3 cannot send packets to host 1, we only block requests from host 3, but do not block replies from host 3 to other hosts.**

#### Use port number information
Drop request from host 3
```
sh ovs-ofctl add-flow s1 priority=1001,in_port=s1-eth3,dl_type=0x800,nw_proto=1,icmp_type=8,actions=drop
```
Drop request from host 2 to host 1
```
sh ovs-ofctl add-flow s1 priority=1001,in_port=s1-eth2,dl_dst=00:00:00:00:00:01,dl_type=0x800,nw_proto=1,icmp_type=8,actions=drop
```
Drop request from host 2 to host 3
```
sh ovs-ofctl add-flow s1 priority=1001,in_port=s1-eth2,dl_dst=00:00:00:00:00:03,dl_type=0x800,nw_proto=1,icmp_type=8,actions=drop
```
> dl_dst: destination MAC address
> nw_proto=1: Specifies that the packet's protocol is ICMP.\
> dl_type=0x800: IPv4.\
> icmp_type=8: specifies that packets have ICMP request.
#### Use MAC address information
Delete drop with port number
```
sh ovs-ofctl del-flows s1 in_port=s1-eth3,dl_type=0x800,nw_proto=1,icmp_type=8
sh ovs-ofctl del-flows s1 in_port=s1-eth2,dl_dst=00:00:00:00:00:01
sh ovs-ofctl del-flows s1 in_port=s1-eth2,dl_dst=00:00:00:00:00:03
sh ovs-ofctl dump-flows s1
```

Drop request from host 3
```
sh ovs-ofctl add-flow s1 priority=1001,dl_src=00:00:00:00:00:03,dl_type=0x800,nw_proto=1,icmp_type=8,actions=drop
```
Drop request from host 2 to host 1
```
sh ovs-ofctl add-flow s1 priority=1001,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:01,dl_type=0x800,nw_proto=1,icmp_type=8,actions=drop
```
Drop request from host 2 to host 3
```
sh ovs-ofctl add-flow s1 priority=1001,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:03,dl_type=0x800,nw_proto=1,icmp_type=8,actions=drop
```

#### Use IP address information
Delete drop with MAC adress 
```
sh ovs-ofctl del-flows s1 dl_src=00:00:00:00:00:03,dl_type=0x800,nw_proto=1,icmp_type=8
sh ovs-ofctl del-flows s1 dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:01
sh ovs-ofctl del-flows s1 dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:03
sh ovs-ofctl dump-flows s1
```
Get IP address information
```
h1 ifconfig
h2 ifconfig
h3 ifconfig
h3 ifconfig
```
h1's IPv4 Address is 10.0.0.1 
![](iph1.png) \
Drop request from host 3
```
sh ovs-ofctl add-flow s1 priority=1001,nw_src=10.0.0.3,dl_type=0x800,nw_proto=1,icmp_type=8,actions=drop
```
Drop request from host 2 to host 1
```
sh ovs-ofctl add-flow s1 priority=1001,nw_src=10.0.0.2,nw_dst=10.0.0.1,dl_type=0x800,nw_proto=1,icmp_type=8,actions=drop
```
Drop request from host 2 to host 3
```
sh ovs-ofctl add-flow s1 priority=1001,nw_src=10.0.0.2,nw_dst=10.0.0.3,dl_type=0x800,nw_proto=1,icmp_type=8,actions=drop
```

#### Result
![](UsePortNumberToConfig.png)

