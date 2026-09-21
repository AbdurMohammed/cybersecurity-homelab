# Network Service Discovery

## Objective

Analyze network services exposed by an Ubuntu Server VM
from a separate Kali Linux workstation.

## Environment

- VMware Workstation
- Kali Linux security workstation
- Ubuntu Server target
- VMware virtual network

## Methodology

1. Established baseline network connectivity.
2. Identified listening services locally with `ss`.
3. Performed remote service discovery with Nmap.
4. Used Nmap service detection against discovered ports.
5. Compared remote findings with the Ubuntu host.
6. Examined SSH logs following network and authentication activity.

## Findings

| Observation   | Ubuntu (`ss`)   | Kali (`nmap`)                   |
| ------------- | --------------- | ------------------------------- |
| SSH / TCP 22  | Listening       | Open                            |
| DNS / 53      | Visible locally | Not discovered by standard scan |
| DHCP / UDP 68 | Visible locally | Not discovered by standard scan |


When attempting to identify services remotely with Nmap from Kali to Ubuntu, only the TCP service on port 22 was visible. However, when investigating sockets locally with ss, I saw additional services, including DNS on port 53 and DHCP client activity on port 68. These did not appear in the standard Nmap scan. This demonstrated that a service or socket visible locally is not necessarily reachable or discoverable from another machine. Factors such as the protocol being used, the interface/address a service is bound to, and network filtering can affect what is externally visible.

Next, I compared the interactions between Nmap and port 22 with a normal SSH login event. I first scanned port 22 on Ubuntu and requested service/version information, which provided details including the port status, SSH service information, version, and MAC address. When examining the Ubuntu SSH logs with journalctl, I did not find an authentication event corresponding to the service scan.

I then used SSH to log into Ubuntu from Kali, establishing an authenticated session between the two systems. When I examined the logs afterward, the login had been recorded, including the accepted authentication and the beginning of the SSH session.

From this investigation, I learned that the services and sockets visible locally on a machine do not necessarily represent what another machine can discover remotely. I also observed that service discovery interacts with a system differently from an authenticated connection. This resulted in different logging behavior, which is an important distinction when investigating network activity.


## Observing Attack Surface Changes

### Baseline

First I established a baseline scan of the Ubuntu environment before making any additional changes. The only remotely exposed TCP port was 22, or ssh.

### System Change

I then introduced a new variable into the Ubuntu environment, installing and deploying an Nginx server. I used systemctl to verify its status locally, and then curled it from Kali to observe the webpage externally.

### Rescan/Log Analysis

| Port | Baseline | After Change | Service |
|------|----------|--------------|---------|
| 22/tcp | Open | Open | SSH |
| 80/tcp | Not detected | Open | HTTP |

I then performed another scan from Kali using nmap, and observed a new exposed tcp port on 80 (the nginx server). Going back to Ubuntu, I was able to read the access.log again to see the nmap and curl activity on the new port.

### Conclusions

By establishing a control and then observing the changes after deploying Nginx, I was able to see the change in network exposure. Deploying the web server caused Nginx to listen for incoming connections on TCP port 80, allowing reachable machines to send HTTP requests to the service. This is necessary when hosting a webpage so that other systems can access it. However, this also drastically increased our exposed attack surface, opening up another possible attack vector in our security enclosure in the Ubuntu environment. Using tools is necessary in everyday work, however understanding their impact on the overall security diagram of our network is just as important to make sure we aren't overexposing ourselves or leaving something unsecured.