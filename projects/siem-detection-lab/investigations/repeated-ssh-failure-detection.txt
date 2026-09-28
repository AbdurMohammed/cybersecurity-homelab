# Repeated SSH Failure Detection

## Objective

The goal of this exercise was to move beyond detecting individual authentication failures and create a custom Wazuh rule capable of identifying repeated suspicious SSH activity. I wanted the rule to detect multiple login attempts against nonexistent users originating from the same source IP within a short period of time.

## Initial Investigation

I first generated several SSH login attempts from my Kali Linux system against the monitored Ubuntu server using a nonexistent account named `fakeuser`.

Individual attempts were detected by Wazuh rule `5710`, which identifies SSH attempts against nonexistent users. These events were assigned a rule level of 5 and contained information such as the source IP, source port, attempted username, and original SSH log.

After generating multiple failures, Wazuh also triggered rule `2502` at level 10 with the description:

`syslog: User missed the password more than one time`

Initially, this appeared to be a correlation rule for the individual authentication failures. However, inspecting the Wazuh ruleset showed that rule `2502` instead matches log messages containing phrases such as `more authentication failures` or `REPEATED login failures`. It was therefore detecting a separate log message describing repeated failures rather than directly counting the individual rule `5710` events.

To better understand how Wazuh performs event correlation, I searched the installed ruleset for rules using `frequency` and `timeframe`. Rule `11451`, which detects repeated FTP login failures, provided an example of correlation using:

- `frequency` to define the number of repeated events
- `timeframe` to define the period in which they must occur
- `if_matched_sid` to identify the base rule being monitored
- `same_source_ip` to require the events to originate from the same source

I used this structure as the basis for my own SSH detection.

## Detection Logic

The custom detection was designed with the following initial parameters:

| Parameter | Value |
|---|---|
| Base rule | `5710` |
| Threshold | 6 events |
| Timeframe | 30 seconds |
| Correlation | Same source IP |
| Severity | Level 8 |

Six attempts within 30 seconds was selected as an initial lab threshold to distinguish repeated behavior from an isolated authentication mistake. Level 8 was selected because the repeated activity was considered more suspicious than the individual level 5 events, while still leaving room for higher-severity detections.

These values are initial testing parameters rather than production-ready thresholds and could be adjusted based on observed behavior and false positives.

## Implementation

The following custom rule was added to Wazuh's `local_rules.xml`:

```xml
<rule id="100002" level="8" frequency="6" timeframe="30">
    <if_matched_sid>5710</if_matched_sid>
    <same_source_ip />
    <description>Repeated SSH login attempts against nonexistent users</description>
    <group>authentication_failed,sshd,</group>
</rule>
```

Rule `100002` monitors events that previously matched rule `5710`. When the required number of events occur within the configured timeframe and originate from the same source IP, Wazuh generates the custom level 8 alert.

Before loading the rule, the Wazuh configuration was tested with:

```bash
sudo /var/ossec/bin/wazuh-analysisd -t
```

The command returned exit code `0`, confirming that the configuration passed validation.

The Wazuh manager was then restarted to load the new rule.

## Validation

To test the detection, I generated repeated SSH authentication attempts from the Kali Linux system against a nonexistent user on the Ubuntu server.

The activity produced the expected individual rule `5710` events. After the configured threshold was reached within the 30-second window, Wazuh successfully generated an alert for custom rule `100002` at level 8.

This confirmed that the custom rule was successfully correlating multiple authentication events based on both their timing and source IP.

## Analysis

This exercise demonstrated the difference between detecting an individual security event and detecting a pattern of behavior across multiple events.

Rule `5710` identifies each individual attempt against a nonexistent SSH user. The custom rule builds on those events and looks for repeated occurrences from the same source:

`SSH event → Rule 5710 → repeated matches → Rule 100002`

This also demonstrated that SIEM alerts should not be interpreted solely from their descriptions. Inspecting Wazuh's existing rules showed that rule `2502`, despite appearing to represent correlation, was matching a separate log message describing repeated authentication failures. Examining the underlying rule logic was necessary to understand what the detection was actually doing.

The threshold used in this lab is not intended to represent a universal production configuration. In a real environment, the frequency, timeframe, and severity would need to be tuned using normal authentication patterns and false-positive rates.