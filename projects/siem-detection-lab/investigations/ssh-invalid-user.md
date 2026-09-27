# SSH Invalid User Investigation

## Scenario

A controlled SSH authentication attempt was generated from a Kali Linux workstation against an Ubuntu Server monitored by Wazuh. The login used a nonexistent account named `fakeuser` in order to generate authentication-failure telemetry.

## Environment

| System | Role | IP |
|---|---|---|
| Kali Linux | Activity source | 192.168.200.128 |
| Ubuntu Server | Monitored endpoint | 192.168.200.133 |
| Wazuh | SIEM | 192.168.200.135 |

## Observed Event

Wazuh detected an SSH login attempt originating from `192.168.200.128` against the nonexistent account `fakeuser`.

The original SSH log contained:

`Invalid user fakeuser from 192.168.200.128 port 55436`

Wazuh extracted the source IP, source port, and attempted username from the event.

## Detection

- **Decoder:** `sshd`
- **Rule ID:** `5710`
- **Rule level:** `5`
- **Description:** `sshd: Attempt to login using a non-existent user`
- **Groups:** `syslog`, `sshd`, `authentication_failed`, `invalid_login`

### MITRE ATT&CK Mapping

- `T1110.001` — Password Guessing
- `T1021.004` — SSH
- Credential Access
- Lateral Movement

## Analysis

The alert demonstrates how Wazuh can transform a raw SSH authentication log into structured security telemetry. The original event was decoded to identify information such as the source IP and attempted username before being matched against Wazuh rule 5710.

Although Wazuh maps the event to password guessing, a single failed authentication attempt alone is not sufficient to conclude that a password-guessing attack occurred. Additional events and surrounding context would be required to determine whether the activity represents an attack or an isolated authentication failure.

## Next Steps

Future testing will generate repeated authentication failures to examine how Wazuh correlates multiple related events and whether higher-level detection rules are triggered.