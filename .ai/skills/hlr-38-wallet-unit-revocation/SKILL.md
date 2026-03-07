---
name: "hlr-38-wallet-unit-revocation"
description: "Use when working with EUDI high-level requirements for 'Wallet Unit revocation'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.22 Topic 38 - Wallet Unit revocation"
  - "A. Issuing a Wallet Unit Attestation <!-- omit from toc -->"
  - "B. Revoking a Wallet Unit <!-- omit from toc -->"
  - "C. Informing the User <!-- omit from toc -->"
  - "D. Verifying the revocation status of a Wallet Unit <!-- omit from toc -->"
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~2234 -->

#### A.2.3.22 Topic 38 - Wallet Unit revocation

##### A. Issuing a Wallet Unit Attestation <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| WURevocation_01 | To enable a PID Provider or an Attestation Provider to verify the authenticity and the revocation status of a Wallet Unit it is interacting with, a Wallet Provider SHALL issue one or more Wallet Unit Attestations to the Wallet Unit, as specified in [Topic 9](./annex-2.02-high-level-requirements-by-topic.md#a236-topic-9---wallet-unit-attestation-and-wallet-instance-attestation). *Note: The first of these WUAs will be issued during the activation phase of a Wallet Unit. During the lifetime of the Wallet Unit, the Wallet Provider will re-issue WUAs as needed.* |
| WURevocation_02 | Empty |
| WURevocation_03 | A Wallet Provider SHALL have a policy governing all aspects of WUA issuance and management. The policy SHALL distinguish between WUAs for WSCA/WSCDs and WUAs for keystores. For WUAs describing a WSCA/WSCD, the policy SHALL comply with at least the extended normalised certificate policy (‘NCP+’) requirements as specified in ETSI EN 319 411-1, insofar applicable for the issuance of WUAs rather than public key certificates. For WUAs describing a keystore, the policy SHALL comply with at least the normalised certificate policy (‘NCP’) requirements as specified in ETSI EN 319 411-1, insofar applicable for the issuance of WUAs rather than public key certificates *Note: A common dedicated policy for issuing WUAs may be developed in the future. If so, this requirement will be changed to refer to it.* |
| WURevocation_04 | Empty |
| WURevocation_05 | Empty |

##### B. Revoking a Wallet Unit <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| WURevocation_06 | Empty |
| WURevocation_07 | A Wallet Provider SHALL be able to revoke a Wallet Unit by revoking its WUA(s), as specified in [[Topic 7](./annex-2.02-high-level-requirements-by-topic.md#a235-topic-7---attestation-revocation-and-revocation-checking)]. |
| WURevocation_08 | Empty |
| WURevocation_09 | During the lifetime of a Wallet Unit, the Wallet Provider SHALL regularly verify that the security of the Wallet Unit is not breached or compromised. If the Wallet Provider detects a security breach or compromise, the Wallet Provider SHALL analyse its cause(s) and impact(s). If the breach or compromise affects the trustworthiness or reliability of the Wallet Unit, the Wallet Provider SHALL revoke the Wallet Unit and SHALL immediately revoke the corresponding WUA(s). The Wallet Provider SHALL do so at least in the following circumstances: - If the security of the Wallet Unit, or the security of the mobile device and OS on which the corresponding Wallet Instance is installed, or the security of the WSCA/WSCD it uses for managing critical cryptographic assets, is breached or compromised in a manner that affects its trustworthiness or reliability. - If the security of the Wallet Solution is breached or compromised in a manner that affects the trustworthiness or reliability of all corresponding Wallet Units. - If the security of the common authentication and data protection mechanisms used by the Wallet Unit is breached or compromised in a manner that affects their trustworthiness or reliability. - If the security of the electronic identification scheme under which the Wallet Unit is provided is breached or compromised in a manner that affects its trustworthiness or reliability. *Note: Note to the first bullet: This corresponds to a Critical or High Risk level security posture risk status according to the table in [Section 6.5.4.2 of the ARF main document](../../architecture-and-reference-framework-main.md#6542-wallet-unit-revocation), as analysed or detected for a Wallet Instance due to monitoring done according to WPSM_03.* |
| WURevocation_09a | If the Wallet Provider must revoke the entire Wallet Unit (e.g., for one of the reasons stated in WURevocation_09), then the Wallet Provider SHALL revoke all WUAs related to the WSCA/WSCD and to all keystores. |
| WURevocation_09b | If there is a security breach of the WSCA/WSCD, then the Wallet Provider SHALL revoke the entire Wallet Unit by revoking all WUAs related to the WSCA/WSCD and to all keystores. |
| WURevocation_09c | If there is a security breach of a keystore, then the Wallet Provider SHALL at least revoke all WUAs related to that keystore. The Wallet Provider SHOULD also revoke the WUAs related to the WSCA/WSCD and to the other keystores (if any). If the Wallet Provider decides to only revoke the relevant keystore, the Wallet Provider SHALL create a risk analysis showing that this does not lead to unacceptable risks to the User, PID Providers and Attestation Providers, Relying Parties, or the Wallet Provider itself. *Note: If the Wallet Provider does not revoke the other WUAs, only the attestations bound to the revoked keystore will be impacted. Other functionalities of the Wallet Unit, including the presentation of a PID, will remain available to the User.* |
| WURevocation_10 | A Wallet Provider SHALL revoke a Wallet Unit upon the explicit request of the User registered during the Wallet Unit activation process, see [Topic 40](./annex-2.02-high-level-requirements-by-topic.md#a2323-topic-40---wallet-instance-installation-and-wallet-unit-activation-and-management). To do so, the Wallet Provider SHALL revoke all valid WUA(s) for that Wallet Unit. The Wallet Provider SHALL authenticate the User before accepting a request to revoke the Wallet Unit. |
| WURevocation_11 | A Wallet Provider SHALL revoke a Wallet Unit upon the explicit request of a PID Provider, in case the natural person using the Wallet Unit has died. To do so, the Wallet Provider SHALL revoke all valid WUA(s) for that Wallet Unit. To identify the Wallet Unit that is to be revoked, the PID Provider SHALL use a Wallet Unit identifier provided by the Wallet Provider in the WUA during PID issuance. *Note: See the notes to WUA_08.* |
| WURevocation_12 | Before revoking a Wallet Unit per WURevocation_11, the Wallet Provider SHALL verify that the party requesting revocation is indeed a valid PID Provider listed in the LoTE of PID Providers. |
| WURevocation_13 | Before requesting a Wallet Provider to revoke a Wallet Unit per WURevocation_11, the PID Provider SHALL ensure that the revocation does not harm the interests of any of the stakeholders. The PID Provider SHALL include a documented policy ensuring that this is the case in the policy meant in WURevocation_03. |

##### C. Informing the User <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| WURevocation_14 | A Wallet Provider SHALL inform a User without delay, and within 24 hours at most, in case the Wallet Provider decided to revoke the User's Wallet Unit. The Wallet Provider SHALL also inform the User about the reason(s) for the revocation. This information SHALL be understandable for the general public. It SHALL include (a reference to) technical details about any security breach if applicable. The Wallet Provider SHALL inform the User about the function(s) of the Wallet Unit that remain available to the User, if any, and functions that will not work any more. The Wallet Provider SHALL also inform the User about measures they can take to ensure they have a fully working Wallet Unit again as soon as possible, such as migrating to a different Wallet Solution. *Note: Functions that remain available to the User may include viewing their own attributes in their Wallet Unit and accessing their account at the Wallet Provider.* |
| WURevocation_15 | Empty |
| WURevocation_16 | To inform a User about the revocation of their Wallet Unit, the Wallet Provider SHALL use a communication channel that is independent of the Wallet Unit. In addition, the Wallet Provider MAY use the Wallet Unit itself to inform the User. |

##### D. Verifying the revocation status of a Wallet Unit <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| WURevocation_17 | Empty |
| WURevocation_18 | A PID Provider issuing revocable PIDs SHALL, for each of its valid PIDs, regularly verify whether the Wallet Provider revoked the Wallet Unit on which that PID is residing, using the revocation information in the WUA it received during issuance of that PID. If it turns out that the Wallet Unit is revoked, the PID Provider SHALL immediately revoke the respective PID in accordance with all requirements in [[Topic 7](./annex-2.02-high-level-requirements-by-topic.md#a235-topic-7---attestation-revocation-and-revocation-checking)]. *Note: a) This is a consequence of the legal requirement in [CIR 2024/2977], Article 5, 4.(b). b) See [Technical Specification 3](../../technical-specifications/ts3-wallet-unit-attestation.md) for how the PID Provider can do this verification. c) The reverse is not true: When a PID is revoked, this does not imply that the Wallet Unit on which it is residing should also be revoked. Instead, the Wallet Unit moves to the Operational state. See [ARF main document Section 4.6.3](../../architecture-and-reference-framework-main.md#463-wallet-unit).* |
| WURevocation_19 | An Attestation Provider issuing revocable attestations MAY decide to revoke an attestation if the Wallet Provider revoked the Wallet Unit on which that attestation is residing, in the same manner as described in WURevocation_18. An Attestation Provider SHALL publish its policy in this regard. *Note: Publishing its policy regarding revocation allows a Relying Party to decide if it can put sufficient trust in the attestations issued by that Attestation Provider.* |
| WURevocation_19a | Empty |
| WURevocation_19b | Empty |
| WURevocation_20 | Empty |
| WURevocation_21 | Empty |
