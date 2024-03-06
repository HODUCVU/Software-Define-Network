# SDN Contoller Lecture
* [Link](https://learning.knetsolutions.in/docs/ryu/)
# Lecture
* Get MAC Address in subnet by ping IP Address:
	* To h1 get MAC Address of h2
	```
	mininet>h1 ping h2
	// see ARP (Address Resolution Protocol) of h1
	mininet>h1 arp -a
	```

	![](images/h1ARP.png)
	* Delete MAC Address of host 2 in ARP entry of host 1
	'''
	h1 arp -d 10.0.0.2
	'''
* Create network with many topos
	* Linear Topology
	```
	sudo mn --topo linear,4 --mac --controller remote,ip=127.0.0.1 -i 10.0.0.0/24 --switch ovsk
	
        ```
	![](images/linear-topo.png)
	* Tree Topology
	```
	sudo mn --topo tree,depth=2,fanout=3 --mac --controller remote,ip=127.0.0.1 -i 10.0.0.0/24 --switch ovsk

        ```
	![](images/tree-topo.png)
	* Single Topology
	```
	sudo mn --topo single,4 --mac --controller remote,ip=127.0.0.1 -i 10.0.0.0/24 --switch ovsk
	```

