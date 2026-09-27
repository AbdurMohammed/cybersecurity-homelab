# SIEM Detection Lab

A home security monitoring and detection engineering environment built using Wazuh.

## Architecture

- **Kali Linux** — controlled security activity
- **Ubuntu Server** — monitored Linux endpoint
- **Wazuh** — centralized SIEM and security analysis

The lab is designed to generate controlled security activity, collect endpoint telemetry, investigate alerts, and develop and test detection logic.

## Investigations

- [SSH Invalid User Investigation](investigations/ssh-invalid-user.md)