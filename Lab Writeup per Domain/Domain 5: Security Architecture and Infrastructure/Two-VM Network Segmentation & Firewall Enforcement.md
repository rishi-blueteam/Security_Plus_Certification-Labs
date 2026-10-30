# Network Segmentation, & Firewall Enforcement with Packet Capture

## Objective


Simulate:

- Attacker VM
- Target VM
- Controlled communication
- Network segmentation
- Traffic Monitoring, logging blocking & allowing
- Real validation using Nmap & ping

The objective is to simulate two systems communicating over a shared NAT network and implement firewall rules to:

- Allow & Deny communication
- Ensure that the firewall is enabled and capturing its logs 
- Verifying that it does not allow us to formally for a secure connection with the target machine

This validates understanding of:
- Security Architecture (OBJ 3.1)
- Firewalls (OBJ 3.2)
- Configuring Firewalls (OBJ 4.5) 
- Hardening (OBJ 2.5)

## Lab Tools Used

|   |   **Component**   |         **Configuration**        |   |   |
|---|:-------------:|:----------------------------:|---|---|
|   | Hypervisor    | VirtualBox                   |   |   |
|   | Network Type  | NAT Network                  |   |   |
|   | Subnet        | 10.0.2.0/24                  |   |   |
|   | VM 1          | Parrot OS (Target)           |   |   |
|   | VM 2          | Kali Linux (Attacker)        |   |   |
|   | Firewall Tool | UFW (Uncomplicated Firewall) |   |   |
|   | Testing Tools | Networking Tools, nmap       |   |   |
|   | Network Monitoring Tool | TCP-Dump           |   |   |


## Security Architecture Theory

### What is Network Segmentation?

It is dividing of network into smaller segments. This is quite usefull as :

- Reduce Attack Surface
- Prevent Lateral Movement
- Helps to seprate Resources cloud level
- Enforce Zero Trust Principle

**Without segmentation:** Attacker VM can not just communicate but access an internal network and gain full access

**With Segmentation:** Attacker VM cannot easily communicate to the internal network and could be blocked by the firewall

------------------------------------------------------- 

## Firewalls in generall 

A firewall in generall is a middle man that exist between the internet and the user, and when I say user...it simply means between the gateway that passess traffic from the user to router to the network. 

**Definition:** A firewall is a network security device designed to monitor, filter, and control incoming and outgoing network traffic based on predetermined security rules. The primary purpose of a firewall is to establish a barrier between a trusted internal network and untrusted external networks. It appears in form of both hardware and software

They regulate both inbound and outbound network protecting the network from:

-  External Threats
-  Insider threaths

We have varities of Firewall Generation that serves different purposes:

- First Gen Firewall
- Second Gen Firewall
- Third Gen Firewall
- Next Gen Firewall

### Types of Firewall

**Stateless Firewall**

- They are firewall that protect the network by inspecting the packet details usually port, source, destination and act according to the rules they are given. They act on the transport level layer of the protocol.

- It is more of a packet filtering at header level and does not store but just reacts as they inspect packet to packet.

- Inexpensive and yet not so good interms of security at a higher level. 

**Statefull Firewall**

- This is an advance version of firewall, this definetly helps for better packet analysis to inspect the details of the packets incoming and outgoing of the network.
- Expensive and takes a greater toll on the network


**Next Gen Firewall**
- One of the most reliable friendly firewall of all time as they not only just use legacy firewall tactics but even new freindly analysis for ensuring network security. It means it can not only just do port blocking or allowing, but source, destination, ip, packet inspection in detail also to compare it with latest network security threats with AI to train itself to act better with different scenarious.  
- They can be deployed as software or hardware, by scaling to any location to any kind of size required from remote, office, campus, or even outdoor.

Different possible security at different level includes: 
- IOT security
- Zero Trust Network
- Operational Technology Security
- DNS Security
- Application Security

### Linux UFW Firewall

> Linux UFW Firewall known as the UnComplicated Firewall can be used in any linux or ubuntu hypervisor which acts as stateless firewall to the endpoint, for managing various network management traffic rules from ip and ports of source and destination. For this lab we used UFW to understand the working principles of it, and how we can prevent any attacker or ourself to communicate with any attacker.

## Lab Procedure

- Before we set up the firewall it is important to ensure that our vm are able to communicate to each other using the NAT default network. We set up the NAT using the VM GUI.

- We navigate to File > Tools > Network, and select a section known as NAT network

- We ensure the DHCP is enabled


**Why is "NAT Network" important to use?**
>> NAT network means Network Address Translation, and is needed so that hosts can easily communicate to any VM, basically inter VM connection, but NAT itself is hiding behind the host and only allows for Internet Access and no Inter VM connection?


**Questions:** Why do we ensure DHCP is enabled?

>>"We ensure the DHCP is enabled because this takes away the hastle to assign IP address to every single device using a network IP. If we assign a range of subnets of an IP and ensure the DHCP is enabled, then every VM that is using the NAT Network will be having a particular subnet of the same ip assigned automatically."

![NAT Setup](../../Screenshots/Domain%205/Setting%20Nat%20Network%20Up.png)

- After setting the NAT for the VM then we ensure that each VM uses the "NAT Network" in their Network settings for this process to work. 

- We will verifiy this as follows that how the VM is just using same IP of different subnet as follows.

**Target IP:**

![Target IP SET](../../Screenshots/Domain%205/Target%20IP%20Set.png)

**Attacker:**

![Attacker IP set](../../Screenshots/Domain%205/Attacker%20IP%20Set.png)

### Setting up Firewall, Verifying Status and Checking

- First we will ensure that we have UFW enabled or no

> sudo ufw status

- It can either be enabled or not present for the system so, we first install it and then we enable it using the following command

> apt-get install ufw -y

> sudo ufw enable

![UFW Firewall Download and enabled](../../Screenshots/Domain%205/UFW%20Enable%20%26%20Download.png)

> We will now set **deny** incoming, and set **allow** outgoing for the attacker machine. 

![Verify Incoming and Outgoing Firewall Setting](../../Screenshots/Domain%205/VErify%20Incoming%20and%20Outgoing%20Status.png)


**Note:** Pinging the attacker from the Target Machine will allow us to ping, but why is that? UFW is a stateless firwall, it acts on packets, it acts on  Attacker machine has just denied the incoming connections from outside. It is because ping is a ICMP echo request that the stateless firewall does not prevent as we did not edit that rule as such seprately. 

![Pinging Attacking Machine for which UFW was enabled](../../Screenshots/Domain%205/Pinging%20Attacker.png)


- Let's disbale the ufw for attacker machine

- Let's test to see the UFW does any good to protect the target machine.

- we enabled the UFW on the target machine with the same command we did for the attacker machine.

- With the attacker machine we used **nmap** to do check for any open ports or for any open connections but, we will see that all the ports are filtered, and are in ignored state.

![Target Machine blocked TCP connections](../../Screenshots/Domain%205/Target%20Machine%20blocked%20TCP%20connections.png)

>> Now we will enable the logging to be high so that we can capture the log packets of the firewall of the Target machine blocking the incoming connections.

### Capturing UFW logs, Monitoring Connection

- We set the logging to high as it was showing low before hence we use the command:

> sudo ufw set logging high

![Logging High](../../Screenshots/Domain%205/UFW%20logging%20set%20High.png)

- After we set logging high, now lets attack the target machine and let's get to business.

- We use Nmap to talk with our intented target machine again. The target machine is at IP 10.0.2.4 a

- The logs at the target machine (Parrot OS) are supposed to be stored at /var/log/syslog. It appears not to be there.

- After researching, it was found to be noticed that the logs are stored at journalctl not just ufw but generally every log of the system itself.  

![UFW logs on target machine noticed](../../Screenshots/Domain%205/UFW%20logs%20on%20target%20machine%20noticed.png)

- NOw we will use TCPdump in the same machine but another terminal to see if our attacker is able to detect and see if any successfull tcp connections took place or no. This will be live and running until we mannualy end the connection.

> sudo tcpdump -i enp0s3 host 10.0.2.15

![tcpdump working](../../Screenshots/Domain%205/TCPDump%20Live%20and%20running%20with%20logs%20detected..png)

- Now, I have collected the recent logs of the UFW using the command and move them to a text file by saving it as a txt file. These will be recorded as live and hence directly when we print it we will get an output. Untill the can is over, and we do not **cat** the file we won't get the results. 

> journalctl tail -K -f | grep UFW  > ufw_log_recent.txt 

- I have verified it by running the txt file

> cat UFW_final_output.txt

> *The -f keeps the scan live and running*

![output file of logs recent saved](../../Screenshots/Domain%205/output%20file%20of%20logs%20recent%20saved.png)

- We keep the UFW logging on and live waiting for the attacker to actually send an nmap noisy scan.

![UFW Log Scanning Stored to File](../../Screenshots/Domain%205/UFW%20Log%20Scanning%20Stored%20to%20File.png)

- The cursor is blinking means the firewall is activing and ready to log. 

-TCPDump on other hand will just give us a confirmation that attacker doesn't have any hold of infomration to any ports of the attacker. 

![tcpdump scn storing in a file](../../Screenshots/Domain%205/tcpdump%20scn%20storing%20in%20a%20file.png)

- From the attacker machine we will send a nmap scan again to the target machine. 

> nmap 10.0.2.4

### Observations

- We will be able to notice that the firewall is blocking in continous flow of the atttackers attempt to learn about the system, these are all stored on the file.


![output for ufw logs](../../Screenshots/Domain%205/UFW%20Log%20Output%20extracted..png)


- The TCP dump output of the file can also be seen 

![tcpdump logs output of a file](../../Screenshots/Domain%205/tcpdump%20logs%20output%20of%20a%20file.png)


## Conclusion

With this I have not only learnt about just firewalls, but learnt about the types of firewall, its implementation, on linux system too, network segmentation, logs monitoring and capturing, and tcpdump for packet capture and analysis.















