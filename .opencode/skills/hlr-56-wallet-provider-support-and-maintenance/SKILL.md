---
name: "hlr-56-wallet-provider-support-and-maintenance"
description: "Use when working with EUDI high-level requirements for 'Wallet Provider Support and Maintenance'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.34 Topic 56 - Wallet Provider Support and Maintenance"
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~524 -->

#### A.2.3.34 Topic 56 - Wallet Provider Support and Maintenance

| **Index** | **Requirement specification** |
| -- | -- |
| WPSM_01 | A Wallet Provider SHALL monitor their installed base of operational Wallet Instances for maintenance purposes, and determine and document in a transparent manner the data it needs and is allowed to monitor in order to deliver the required support. Data or attributes that SHOULD be monitored include: 1) Runtime errors, for uncaught errors in production code, 2) UX and telemetry information, for UX field analysis, 3) OS version and health information, for detection of OS level vulnerabilities, 4) Wallet Instance SDK and software library version information, for Wallet Instance code vulnerabilities, 5) User locale/localisation data, for catching localisation related errors, 6) Wallet Instance version, for catching errors or vulnerabilities due to outdated versions, 7) Supported WSCA/WSCDs and their supported capabilities, for detection of cryptography incompatibilities, 8) Unique device identifier such as IDFV or persisted UUID (iOS) or AndroidID (Android), for maintaining an up-to-date list of Wallet Instance-related device installations and for detecting potential malicious use (unrecognised identifier), 9) Device sensor identifiers and patch levels, for checking if sensor hardware in the device is up-to-date. 10) hardware-level details about the device, to identify known hardware-based problems or vulnerabilities, 11) BLE and NFC support by device, for analysing the security and feasibility of proximity use cases with a given Wallet Instance. |
| WPSM_02 | Wallet Providers SHALL, for maintenance purposes, write custom crash logs for sending them for further analysis. |
| WPSM_03 | A Wallet Provider SHALL monitor the security posture of its operational Wallet Instances for the purpose of detecting critical security risks in the environment the Wallet Instance is run at, and determine and document in a transparent manner the data it needs and is allowed to monitor. Information that SHOULD be monitored for software and hardware level problems/vulnerabilities on device includes 1) detection of device rooting/jailbreaking, 2) emulator detection, 3) device OS version and health data, 4) Wallet Instance SDK and SW library versions, 5) Wallet Instance version, 6) Supported WSCA/WSCD and 7) Sensor identifiers and patch levels. |
| WPSM_04 | During the lifetime of the Wallet Unit, the Wallet Provider SHALL update the Wallet Unit as necessary to ensure its continued security and functionality. |
