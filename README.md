# cybersecurity-homelab
Documentation, projects, and investigations from my personal cybersecurity home lab.


## Latest Status Update

Ubuntu Server: Operational
Kali Linux: Operational
VM-to-VM networking: Verified



## Lab Equipment

- Main desktop — primary virtualization workstation
- Spare desktop — dedicated lab system
- Raspberry Pi 400 — Linux and networking experimentation
- Laptop — portable workstation and administration

## Linux Administration

Practiced basic Linux administration through SSH.

### Topics

- Linux filesystem navigation
- Users and identity
- File creation and modification
- File permissions
- Processes
- systemd services
- SSH
- Linux logs

### Commands

`pwd`, `ls`, `cd`, `whoami`, `id`, `hostname`, `uname`,
`mkdir`, `touch`, `cat`, `chmod`, `ps`, `systemctl`,
`journalctl`, `last`

## Networking Fundamentals

- Ubuntu uses ens33 as its virtual network interface
- VMware assigned the VM a private IPv4 address using DHCP
- VM uses a /24 subnet
- Identified the VM's default gateway
- Tested gateway, Internet, and DNS connectivity separately
- Inspected listening TCP/UDP sockets
- Observed an active SSH TCP connection
- Examined VMware networking from the Windows host

