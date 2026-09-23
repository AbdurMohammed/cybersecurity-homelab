# Network Service Discovery -------------------------------------------------------------------------------------------------------

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


## Observing Attack Surface Changes -----------------------------------------------------------------------------------------------

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


## Building an XML Parser

After obtaining multiple scans of different environments in different states, it was time to make use of the data. To do this, I built a Python script that would help me make sense of the information present in these Nmap scans without having to trawl through them by hand. The scope of this script is narrow and straightforward: its goal is to parse XML scans, perform some simple error handling, and extract these important pieces of data: protocol, port ID, state, service, product, and version.

### Parsing the XML

First, I needed to import ElementTree in order to use its XML parsing functionality. I imported the module using the shorthand `ET`. I then used the `parse()` function to parse the file provided by the user and stored the resulting XML tree in a variable called `tree`.

Next, I used `.getroot()` to retrieve the root element of the XML tree and stored it in a variable called `root`. After establishing the root, the next steps were much simpler. I used `findall()` to locate all of the port elements within the XML file and stored them in a Python list named `ports`.

### Making Sense of the List

With a list of ports in hand, I needed to extract useful and relevant information from each one. I looped through the `ports` list and obtained the `protocol` and `portid` attributes from each port element.

Some of the information I wanted was stored deeper in the XML structure. The `state` and `service` elements are child elements of each port rather than attributes of the port itself. From the `state` element, I extracted whether the port was open. From the `service` element, I focused on three pieces of information: the service name, product name, and product version.

Before attempting to extract the service information, I checked whether the service element actually existed. I also included a fallback value of `"Unknown"` in case attributes such as the product or version were missing.

### Reusability

At first, I had hardcoded the exact scan I wanted to parse into the script. While this worked for testing, it wasn't very useful in the long term. I changed the script to accept a command-line argument specifying the XML scan that should be parsed.

This allowed me to use the same script on different Nmap scans without modifying the Python code each time. For example, I could analyze both the baseline scan and the scan taken after installing Nginx simply by providing a different file when running the script.

### Error Handling

Allowing the user to provide a file also introduced several possible edge cases that needed to be handled.

First, I made sure that a scan argument was actually provided. If no argument is given, the script prints a usage message and exits rather than attempting to access a nonexistent argument.

Next, I added handling for a file that does not exist. This could occur because of a mistyped filename or because the expected scan had not been generated yet. Instead of allowing Python to produce a traceback, the script displays a simple error message and exits.

Finally, I added handling for files that exist but are not valid XML documents. Since the script is specifically designed to parse XML data, ElementTree's `ParseError` is caught and a useful error message is displayed instead.

I also included fallback values for missing service information so that unavailable attributes can be displayed as `"Unknown"` rather than causing problems with the output.

### Example

Here is the output when parsing an Nmap XML scan conducted after I installed Nginx on the Ubuntu Server:

```text
python scripts/scan_parser.py scans/after-nginx.xml

tcp/22 - open - ssh - OpenSSH - 10.2p1 Ubuntu 2ubuntu3.6
tcp/80 - open - http - nginx - 1.28.3
```

Compared with the baseline scan, which only exposed SSH on TCP port 22, the parser makes the newly exposed HTTP service on TCP port 80 immediately visible. This provides a much more concise view of the important service information contained within the original Nmap XML output.