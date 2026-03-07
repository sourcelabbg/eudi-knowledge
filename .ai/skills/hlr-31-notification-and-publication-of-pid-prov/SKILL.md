---
name: "hlr-31-notification-and-publication-of-pid-prov"
description: "Use when working with EUDI high-level requirements for 'Notification and publication of PID Provider, Wallet Provider, Attestation Provider, Access Certificate Authority, and Provider of registration certificates'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.20 Topic 31 - Notification and publication of PID Provider, Wallet Provider, Attestation Provider, Access Certificate Authority, and Provider of registration certificates"
  - "A. Generic requirements for notification <!-- omit from toc -->"
  - "B. Requirements for the notification of PID Providers <!-- omit from toc -->"
  - "C. Requirements for the notification of Wallet Providers <!-- omit from toc -->"
  - "D. Requirements for the notification of PuB-EAA Providers <!-- omit from toc -->"
  - "E. Requirements for the notification of Access Certificate Authorities and Providers of registration certificates <!-- omit from toc -->"
  - "F. Requirements for the publication of Trusted Lists and LoTES compiled by the Commission <!-- omit from toc -->"
  - "F. Requirements for the publication of Trusted Lists compiled by the Commission <!-- omit from toc -->"
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~3328 -->

#### A.2.3.20 Topic 31 - Notification and publication of PID Provider, Wallet Provider, Attestation Provider, Access Certificate Authority, and Provider of registration certificates

##### A. Generic requirements for notification <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| GenNot_01 | Member States SHALL notify all PID Providers, PuB-EAA Providers, Wallet Providers, Access Certificate Authorities, and Providers of registration certificates to the European Commission, according all relevant requirements in [Technical Specification 2](../../technical-specifications/ts2-notification-publication-provider-information.md). |
| GenNot_02 | As part of [Technical Specification 2] referred to in GenNot_01, the European Commission SHALL establish standard operating procedures for the notification of a PID Provider, PuB-EAA Provider, Wallet Provider, Access Certificate Authority, or Provider of registration certificates to the Commission. *Note: The outcome of the notification procedure is the publication of the information notified by the Member State according to [Article 5a](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e1347-1-1) (18) in a machine and human readable manner using the common system mentioned in Section H, TLPub_01.* |
| GenNot_03 | The common system mentioned in GenNot_01 SHALL enable: - A secure notification channel between Member States and the Commission for all notifications. - A notification, verification, and publication process and associated validation steps (with follow-up and monitoring) at the Commission side. - Collected data to be processed, consolidated, signed or sealed, and published in both a machine-processable Trusted List or LoTE and in a human-readable format, manually and/or automatically using e.g. a web service and/or API. |
| GenNot_04 | As regard to GenNot_03, second bullet, the Commission SHALL verify whether the notified data is complete and meets the technical specifications, while the Member States SHALL be responsible for the correctness of the notified information. |
| GenNot_05 | As part of the specifications referred to in GenNot_01, the European Commission SHALL establish standard operating procedures for the suspension or cancellation of a PID Provider, PuB-EAA Provider, Wallet Provider, Access Certificate Authority, or Provider of registration certificates. These operating procedures SHALL include unambiguous conditions for suspension or cancellation. As an outcome of the suspension or cancellation procedure, the status of the suspended or cancelled PID Provider, PuB-EAA Provider, Wallet Provider, Access Certificate Authority or Provider of registration certificates in the respective LoTE or Trusted List SHALL be changed to Invalid. |

##### B. Requirements for the notification of PID Providers <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| PPNot_01 | The European Commission SHALL establish technical specifications for the common set of information to be notified about PID Providers. |
| PPNot_02 | The common set of information to be notified about a PID Provider SHALL include at least: 1. Identification data: i. MS/Country of establishment, ii. Name as registered in an official record, iii. Where applicable: a. A business registration number from an official record, b. Identification data from that official record. 2. PID Provider trust anchors, i.e., public keys and name as per point 1) ii) above, supporting the authentication of PIDs issued by the PID Provider, 3. Trust anchors of Access Certificate Authorities for PID Providers, i.e., public keys and CA name, supporting the authentication of the PID Provider by Wallet Units at the service supply point(s) listed per point 4. below. 4. Service supply point(s), i.e., the URL(s) at which a Wallet Unit can start the process of requesting and obtaining a PID. *Note: a) Relating to point 3. above: PID Provider Access Certificate Authority trust anchors are notified separately from the Access Certificate Authority for Relying Parties (see Section G below), since PID Providers are -legally speaking- not Relying Parties. b) For the concept of an Access Certificate Authority, see also [[Topic 27](./annex-2.02-high-level-requirements-by-topic.md#a2316-topic-27---registration-of-pid-providers-providers-of-qeaas-pub-eaas-and-non-qualified-eaas-and-relying-parties)] and [Section 6.3.2 of the ARF main document](../../architecture-and-reference-framework-main.md#632-pid-provider-or-attestation-provider-registration-and-notification).* |
| PPNot_03 | PID Providers SHALL ensure that all PIDs they issue can be authenticated using the PID Provider trust anchors notified to the Commission. |
| PPNot_04 | PID Providers SHALL ensure that their access certificates can be authenticated using the applicable Access Certificate Authority trust anchors notified to the Commission. *Note: [[Topic 6](./annex-2.02-high-level-requirements-by-topic.md#a234-topic-6---relying-party-authentication-and-user-approval)] describes how access certificates will be used.* |
| PPNot_05 | PID Provider trust anchors SHALL be accepted because of their secure notification by the Member States to the Commission and by their publication in the corresponding Commission-compiled PID Provider LoTE, which is sealed by the Commission. |
| PPNot_06 | Access Certificate Authority trust anchors SHALL be accepted because of their secure notification by the Member States to the Commission and by their publication in the corresponding Commission-compiled LoTE, which is signed or sealed by the Commission. |
| PPNot_07 | The format of a PID Provider LoTE SHALL comply with ETSI TS 119 602 v1.1.1, including Annex D. |

##### C. Requirements for the notification of Wallet Providers <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| WPNot_01 | The European Commission SHALL establish technical specifications for the common set of information to be notified about Wallet Providers. |
| WPNot_02 | The common set of information to be notified about a Wallet Provider SHALL include: 1. Identification data: i. MS/Country of establishment, ii. Name as registered in an official record, iii. Where applicable: a. Business registration number from an official record, and b. Identification data from the official record. 2. Wallet Provider trust anchors, i.e., public keys and name as per point 1. b. above, supporting the authentication of Wallet Unit Attestations and Wallet Instance Attestations issued by the Wallet Provider. 3. Name and reference number of the certified Wallet Solution(s) provided by the Wallet Provider. *Note: a) See [[Topic 9](./annex-2.02-high-level-requirements-by-topic.md#a236-topic-9---wallet-unit-attestation-and-wallet-instance-attestation)] and [[Topic 38](./annex-2.02-high-level-requirements-by-topic.md#a2322-topic-38---wallet-unit-revocation)] for the definition of the WUA and WIA. b) A Wallet Provider does not need an access certificate to interact with Wallet Units.* |
| WPNot_03 | Wallet Providers SHALL ensure that all WUAs and WIAs they issue can be authenticated using the trust anchors notified to the Commission. |
| WPNot_04 | Wallet Provider trust anchors SHALL be accepted because of their secure notification by the Member States to the Commission and by their publication in the corresponding Commission-compiled Wallet Provider LoTE, which is sealed by the Commission. |
| WPNot_05 | The format of a Wallet Provider LoTE SHALL comply with ETSI TS 119 602 v1.1.1, including Annex E. |
| WPNot_06 | If a Wallet Provider is cancelled (see requirement GenNot_05 above), that Wallet Provider SHALL immediately revoke all of its valid WUAs, in accordance with the requirements in [Topic 38](./annex-2.02-high-level-requirements-by-topic.md#a2322-topic-38---wallet-unit-revocation). If a Wallet Provider is suspended, that Wallet Provider and the Member State SHALL agree on the necessary precautionary measures that need to be taken, which MAY include the immediate revocation of all or some of its valid WUAs. *Note: WIAs do not have to be revoked, since they are short-lived.* |

##### D. Requirements for the notification of PuB-EAA Providers <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| PuBPNot_01 | The European Commission SHALL establish technical specifications for the common set of information to be notified about PuB-EAA Providers. |
| PuBPNot_02 | The common set of information to be notified by Member States about PuB-EAA Providers SHALL include at least: 1. Identification data: i. MS/Country of establishment, ii. Name as registered in an official record, iii. Where applicable: a. Registration number as in official record, and b. Official record identification data. iv. Identification data of the Union or national law under which a. Either the PuB-EAA Provider is established as the responsible body for the Authentic Source based on which the electronic attestation of attributes is issued, or b. The PuB-EAA Provider is the body designated to act on behalf of the responsible body referred to in point 1. iv. a. v.The conformity assessment report issued by a conformity assessment body, confirming that the requirements set out in paragraphs 1, 2 and 6 of [Article 45f](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e3902-1-1) are met. 2. Service supply point(s), i.e., the URL(s) at which a Wallet Unit can start the process of requesting and obtaining a PuB-EAA from the PuB-EAA Provider. |
| PuBPNot_03 | The format of the PuB-EAA Provider Trusted List SHALL comply with ETSI TS 119 612 v2.1.1. |

##### E. Requirements for the notification of Access Certificate Authorities and Providers of registration certificates <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| RPACANot_01 | The European Commission SHALL establish technical specifications for the common set of information to be notified about Access Certificate Authorities and Providers of registration certificates. |
| RPACANot_02 | The common set of information to be notified about an Access Certificate Authority or a Provider of registration certificates SHALL include: 1. Identification data: i) Member State or country of establishment, ii) Name as registered in an official record, iii) Where applicable: - A business registration number from an official record, - Identification data from that official record. 2. Trust anchors of the Access Certificate Authority or Provider of registration certificates, i.e., public keys and name as per point 1) ii), supporting the authentication of access certificates and registration certificates by Wallet Units. |
| RPACANot_03 | Relying Parties, PID Providers, QEAA Providers, PuB-EAA Providers, and non-qualified EAA Providers SHALL ensure that their access certificates can be authenticated using the trust anchors of an Access Certificate Authority notified to the Commission. |
| RPACANot_03a | Relying Parties, PID Providers, QEAA Providers, PuB-EAA Providers, and non-qualified EAA Providers SHALL ensure that their registration certificates, if issued to them, can be authenticated using the trust anchors of a Provider of registration certificates notified to the Commission. |
| RPACANot_04 | The trust anchors of Access Certificate Authorities and Providers of registration certificates SHALL be accepted because of their secure notification by the Member States to the Commission and by their publication in the corresponding Commission-compiled LoTEs, which are signed or sealed by the Commission. |
| RPACANot_05 | The format of a LoTE for Access Certificate Authorities SHALL comply with ETSI TS 119 602 v1.1.1, including Annex F. |
| RPACANot_05a | The format of a LoTE for Providers of registration certificates SHALL comply with ETSI TS 119 602 v1.1.1, including Annex G. |
| RPACANot_06 | If an Access Certificate Authority is suspended or cancelled (see requirement GenNot_05 above), that Access Certificate Authority SHALL immediately revoke all of its temporally valid access certificates. *Note: This implies that if an intermediary obtained its access certificates from an Access Certificate Authority that is suspended or cancelled, any intermediated Relying Party depending on that intermediary will not be able to request attributes from Wallet Units, even though its registration is still valid. Such an intermediated Relying Party will either have to transit to another intermediary (which has access certificates issued by an active Access Certification Authority) or wait until the original intermediary obtains new access certificates either from another Access CA or from the original one, once that CA can continue its operations.* |
| RPACANot_07 | If a Provider of registration certificates is suspended or cancelled (see requirement GenNot_05 above), that Provider SHALL immediately revoke all of its valid registration certificates (if any). Moreover, the corresponding Registrar SHALL prohibit all access to the registry entries published online per Reg_03 and Reg_04. |

##### F. Requirements for the publication of Trusted Lists and LoTES compiled by the Commission <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| TLPub_01 | The European Commission SHALL establish technical specifications for the system enabling the publication by the Commission of the information notified by the Member States regarding PID Providers, Wallet Providers, PuB-EAA Providers, Access Certificate Authorities, and Providers of registration certificates. |
| TLPub_02 | The European Commission SHALL establish technical specifications for the set of information to be published about PID Providers, Wallet Providers, PuB-EAA Providers, Access Certificate Authorities and Providers of registration certificates, based on the information notified by the Member States. *Note: The information to be published MAY be different from the information to be notified per requirements PPNot_01, WPNot_01, PuBPNot_01, and RPACANot_01 above, respectively.* |
| TLPub_03 | The publication of the information referred to in TLPub_01 SHALL take place over a secure channel protecting the authenticity and integrity of the published information. |
| TLPub_04 | The technical system mentioned in TLPub_01 SHALL NOT require authentication or prior registration and authorisation of any entity wishing to retrieve the published information. |
| TLPub_05 | The information referred to in TLPub_01 SHALL be published in an electronically signed or sealed form that is suitable for automated processing, and in a human-readable format, e.g., through introspection and display facilities, over an authenticated channel. |
| TLPub_06 | The Commission SHALL publish in the OJEU the locations of the LoTEs for PID Providers, Wallet Providers, Access Certificate Authorities, and Providers of registration certificates, as well as the location of the Trusted List(s) of PuB-EAA Providers. |
| TLPub_07 | The Commission SHALL publish in the OJEU the trust anchors to be used for verifying the signature or seal mentioned in TLPub_05. |

##### F. Requirements for the publication of Trusted Lists compiled by the Commission <!-- omit from toc -->

| **Index** | **Requirement specification** |
| -- | -- |
| TLPub_08 | As part of the specifications referred to in TLPub_01, the European Commission SHALL establish technical specifications for ensuring the availability and authenticity of the full history regarding the information notified about PID Providers, Wallet Providers, PuB-EAA Providers, Access Certificate Authorities, and Providers of registration certificates. |
