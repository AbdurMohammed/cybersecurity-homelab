# Kali Linux Workstation

## Purpose

Kali Linux will serve as the security testing workstation
in my cybersecurity home lab.

## Virtual Machine

- Hypervisor: VMware Workstation
- Guest OS: Kali Linux
- CPU: 2 cores
- RAM: 4 GB
- Virtual disk: 40 GB
- Network: VMware NAT

## Network Testing

Verified:

- Default gateway connectivity
- Internet connectivity
- DNS resolution
- Kali-to-Ubuntu connectivity
- Ubuntu-to-Kali connectivity

## Commands Used

- whoami
- hostname
- uname
- ip addr
- ip route
- ping
- ip neigh

## Lab Architecture

Windows Host
    |
VMware Workstation
    |
VMware NAT Network
    |
    +-- Ubuntu Server
    |
    +-- Kali Linux