---
name: "arf-topic-t-support-and-maintenance-by-wal-part-2"
description: "Use when defining Wallet Provider support obligations. Covers maintenance requirements, update mechanisms, incident response, and User support channels. Part 2: covers 4 Additions and changes to the ARF, 4 References."
sections:
  - "4 Additions and changes to the ARF"
  - "4.1 High-Level Requirements to be added to Annex 2"
  - "4.2 High-Level Requirements to be changed"
  - "4.3 Descriptions to be added to the ARF main document"
  - "4 References"
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~1416 -->

## 4 Additions and changes to the ARF

### 4.1 High-Level Requirements to be added to Annex 2

A new topic is suggested for discussing the monitoring functions as part of support and maintenance functions of the Wallet Provider. The following HLRs are suggested to be included:

| **Index** | **Requirement specification** | **Proposal** |
|-----------|-------------------------------|--------------|
| WPSM_01   | The Wallet Provider SHALL monitor their installed base of operational Wallet Instances for maintenance purposes, and determine and document in a transparent manner the data it needs and is allowed to monitor in order to deliver the required support. Data or attributes that SHOULD be monitored include: runtime errors for uncaught errors in production code, UX and telemetry information for UX field analysis, OS version and health information for detection of OS level vulnerabilities, Wallet Instance SDK and software library version information for Wallet Instance code vulnerabilities, user locale/localisation data for catching localisation related errors, Wallet Instance version for catching errors or vulnerabilities due to outdated version, supported WSCA/WSDCs and their supported capabilities for detection of cryptography incompatibilities, unique device identifier such as IDFV or persisted UUID (iOS) or AndroidID (Android) for maintaing an up-to-date list of Wallet Instance related device installations and for detecting potential malicious use (unrecognised identifier), device sensor identifiers and patch levels for checking up-to-dateness of sensor hardware on device, hardware-level details on device to identify known hardware-based problems or vulnerabilities, BLE radio and NFC support in device for analysing the security and feasibility of proximity use cases with a given Wallet Instance. | NEW - Add as new 'base' HLR to new Wallet Provider Support and Maintenance topic.|
| WPSM_02   | Wallet Unit developers SHALL for maintenance purposes write custom crash logs for sending them for further analysis. | NEW  |
| WPSM_03   | The Wallet Provider SHALL monitor the security posture of operational Wallet Instances for the purpose of detecting critical security risks in the environment the Wallet Instance is run at, and determine and document in a transparent manner the data it needs and is allowed to monitor. Information that SHOULD be monitored for software and hardware level problems/vulnerabilities on device includes 1) detection of device rooting/jailbreaking, 2) emulator detection, 3) device OS version and health data, 4) Wallet Instance SDK and SW library versions, 5) Wallet Instance version, 6) Supported WSCA/WSCD and 7) Sensor identifiers and patch levels. | NEW  |

### 4.2 High-Level Requirements to be changed

#### 4.2.1 Topic 38

| **Index** | **Requirement specification** | **Proposal** |
|-----------|-------------------------------|--------------|
| WURevocation_09   |  During the lifetime of a Wallet Unit, the Wallet Provider SHALL regularly verify that the security of the Wallet Unit is not breached or compromised. If the Wallet Provider detects a security breach or compromise, the Wallet Provider SHALL analyse its cause(s) and impact(s). If the breach or compromise affects the trustworthiness or reliability of the Wallet Unit, the Wallet Provider SHALL administratively revoke or suspend the Wallet Unit and SHALL immediately revoke the corresponding WUA(s). The Wallet Provider SHALL do so at least in the following circumstances: - If the security of the Wallet Unit, or the security of the mobile device and OS on which the corresponding Wallet Instance is installed, or the security of a WSCA/WSCD it uses for managing cryptographic keys and sensitive data, is breached or compromised in a manner that affects its trustworthiness or reliability. - If the security of the Wallet Solution is breached or compromised in a manner that affects the trustworthiness or reliability of all corresponding Wallet Units. - If the security of the common authentication and data protection mechanisms used by the Wallet Unit is breached or compromised in a manner that affects their trustworthiness or reliability. - If the security of the electronic identification scheme under which the Wallet Unit is provided is breached or compromised in a manner that affects its trustworthiness or reliability. **Note to the first bullet: This corresponds to a Critical or High Risk level security posture risk status according to [refer to table 3 contents in the topic T -updated ARF] as analysed or detected for a Wallet Instance due to monitoring done according to WPSM_03.**   |   MODIFIED (addition of the text in **bold**)    |

#### 4.2.2 Topic 40

| **Index** | **Requirement specification** | **Proposal** |
|-----------|-------------------------------|--------------|
| WIAM_11   | During the lifetime of the Wallet Unit, the Wallet Provider SHALL **guide the user on how to** update the Wallet Unit as necessary to ensure its continued security and functionality. **If the user fails to do so under a given time frame, the Wallet Provider shall disable the Wallet Unit.** | MOVE as MODIFIED - Proposed to be moved as is into a new HLR (WPSM_04) under the wallet support and maintenance topic. |

### 4.3 Descriptions to be added to the ARF main document

A new short paragraph on runtime Wallet Instance -level monitoring as part of maintenance and security posture analysis is suggested for the ARF main text section 6.5.3.2, based on chapters 3.2 and 3.3 of the updated topic T discussion paper.

Details on monitorable Wallet Instance information (table 1 of the topic T discussion paper) is included into ARF section 6.5.3.2.

## 4 References

| Reference | Description |
| --------- | ------------|
| [ARF_DevPlan] | Architecture and Reference Framework Development plan 2025, European Commission, v0.91, final draft |
| [European Digital Identity Regulation] | Regulation (EU) 2024/1183 of the European Parliament and of the Council of 11 April 2024 amending Regulation (EU) No 910/2014 as regards establishing the European Digital Identity Framework |
| [RTS SCA]   |  [Commission Delegated Regulation (EU) 2018/389 of 27 November 2017 supplementing Directive (EU) 2015/2366 of the European Parliament and of the Council with regard to regulatory technical standards for strong customer authentication and common and secure open standards of communication](https://eur-lex.europa.eu/eli/reg_del/2018/389/oj/eng) |
| [Topic AA]  | [AA - Support of Electronic Payments Customer Authentication (SCA) with the Wallet](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/blob/main/docs/discussion-topics/aa-support-of-electronic-payments-SCA-with-wallet.md) |
