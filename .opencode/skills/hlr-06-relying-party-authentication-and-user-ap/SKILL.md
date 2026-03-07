---
name: "hlr-06-relying-party-authentication-and-user-ap"
description: "Use when working with EUDI high-level requirements for 'Relying Party authentication and User approval'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.4 Topic 6 - Relying Party authentication and User approval"
  - "A. Relying Party authentication <!-- omit from toc -->"
  - "B. User approval <!-- omit from toc -->"
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~1532 -->

#### A.2.3.4 Topic 6 - Relying Party authentication and User approval

##### A. Relying Party authentication <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| RPA_01 | The Wallet Unit used by a User, as well as the Relying Party Instance used by the Relying Party, SHALL implement a mechanism for Relying Party authentication in PID or attestation presentation transactions. This mechanism SHALL: - enable the Wallet Unit to identify and authenticate the Relying Party, - enable the Wallet Unit to verify that the request from the Relying Party was not copied and replayed, - use an access certificate issued in accordance with [[Topic 27](./annex-2.02-high-level-requirements-by-topic.md#a2316-topic-27---registration-of-pid-providers-providers-of-qeaas-pub-eaas-and-non-qualified-eaas-and-relying-parties)]. |
| RPA_01a | If a Wallet Unit supports the [W3C Digital Credentials API] for remote presentation flows, it SHALL retain full authority over the process meant in RPA_01. In particular, this process SHALL NOT be handled by a third party, including the browser and the operating system. |
| RPA_02 | For performing Relying Party authentication, Wallet Units and Relying Party Instances SHALL support access certificates as specified in ETSI TS 119 475 and ETSI TS 119 411-8. *Note: In [ISO/IEC 18013-5], the Relying Party authentication mechanism is called mdoc reader authentication and uses an X.509 certificate. For [OpenID4VP], [HAIP] specifies that Client Identifier Prefix ``x509_hash`` must be used to authenticate the Relying Party; this also uses an X.509 certificate.* |
| RPA_02a | Empty |
| RPA_03 | A Wallet Unit and a Relying Party Instance SHALL perform Relying Party authentication in all PID or attestation presentation transactions to Relying Parties, whether proximity or remote, using an access certificate. *Note: The actions both entities perform differ. For example, while the Relying Party creates a signature over some data in the request, the Wallet Unit validates that signature.* |
| RPA_04 | For the verification of access certificates, a Wallet Unit SHALL accept the trust anchors in the LoTE(s) of all Access Certificate Authorities notified by Member States. *Note: For more information about Access Certificate Authorities, please see [[Topic 31](./annex-2.02-high-level-requirements-by-topic.md#a2320-topic-31---notification-and-publication-of-pid-provider-wallet-provider-attestation-provider-access-certificate-authority-and-provider-of-registration-certificates)].* |
| RPA_05 | If Relying Party authentication fails for any reason, the Wallet Instance SHALL inform the User that the identity of the Relying Party could not be verified and that therefore the request is not trustworthy. |
| RPA_06 | If Relying Party authentication succeeds, the Wallet Instance SHALL display to the User the name of the Relying Party as included in the access certificate received from the Relying Party Instance, together with the attributes requested by the Relying Party. The Wallet Instance SHALL do so when asking the User for approval according to RPA_07. *Note: If the Relying Party is an intermediary acting on behalf of an intermediated Relying Party, the Wallet Instance displays the names of both the intermediary and the intermediated Relying Party to the User, see RPI_07.* |
| RPA_06a | If Relying Party authentication fails for any reason, the Wallet Unit SHALL notify the User. In addition, the Wallet Unit SHALL either not present the requested attributes to the Relying Party, or give the User the choice to present the requested attributes or not. *Note: It is up to the Wallet Provider to make a choice for one of these two options.* |

##### B. User approval <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| RPA_07 | A Wallet Unit SHALL ensure the User approved the presentation of any attribute(s) in the Wallet Unit to a Relying Party or Verifier Wallet Unit, prior to presenting these attributes. A Wallet Unit SHALL always allow the User to refuse presenting an attribute requested by the Relying Party or Verifier Wallet Unit. |
| RPA_07a | If a Wallet Unit supports the [W3C Digital Credentials API] for remote presentation flows, it SHALL retain full authority over the process meant in RPA_07. In particular, this process SHALL NOT be handled by a third party, including the browser and the operating system. |
| RPA_08 | A Wallet Unit SHALL authenticate the User before allowing the User to give or refuse approval for releasing any attributes, in accordance with WIAM_14 or WIAM_15, as applicable. |
| RPA_09 | Empty |
| RPA_10 | When asking for User approval, the Wallet Unit SHALL show to the User the User-friendly description of the Relying Party's intended use and, if available, the link to the applicable privacy policy. *Note: The User-friendly description of the Relying Party's intended use is included in the presentation request and also in the registration certificate, if available. The link to the privacy policy is included in the registration certificate, or in the absence of a registration certificate, the Wallet Unit obtained the link from the Registrar's online service, if the User requested this. See RPRC_19a and other requirements in [Topic 44](./annex-2.02-high-level-requirements-by-topic.md#a2326-topic-44---registration-certificates-for-pid-providers-providers-of-qeaas-pub-eaas-and-non-qualified-eaas-and-relying-parties) for details.* |
| RPA_10a | The Wallet Unit SHOULD ensure that the User gives approval either to present all attributes requested in a presentation request, or none of them. *Note: This means that a User should be asked either to approve the presentation of all requested attributes or to deny all of them. The Wallet Unit should not allow partial approval, since this would mean that the Relying Party cannot deliver the service, but nevertheless receives some User attributes. This would be a violation of the User's privacy. Note that a Relying Party is not allowed to request more data than is justified for the intended use. So if the User feels that the Relying Party is actually requesting more data than needed, that implies that the Relying Party is not trustworthy and should not receive any data.* |
| RPA_11 | When the presentation of an attestation is denied by the User, the Wallet Unit SHALL behave towards the Relying Party as if the attestation did not exist. |
| RPA_12 | When asking for User approval, the Wallet Unit MAY indicate to the User whether the attestation requested by a Relying Party is device-bound or not. *Note: The intent of this indication is to warn the User than a non-device-bound attestation may be copied by the Relying Party and presented to a third party.* |
