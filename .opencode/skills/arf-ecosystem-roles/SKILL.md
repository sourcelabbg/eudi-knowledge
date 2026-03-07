---
name: "arf-ecosystem-roles"
description: "Use when discussing who does what in the EUDI ecosystem: Wallet Provider, PID Provider, QEAA Provider, PuB-EAA Provider, EAA Provider, Relying Party, CAB, Trust List Provider, Access Certificate Authority."
sections:
  - "3. Roles within the EUDI Wallet ecosystem"
  - "3.1 Introduction"
  - "3.2 Users of Wallet Units"
  - "3.3 Wallet Providers"
  - "3.4 Person Identification Data (PID) Providers"
  - "3.5 Trusted List or LoTE Provider"
  - "3.6 Qualified Electronic Attestation of Attributes (QEAA) Providers"
  - "3.7 EAA issued by or on behalf of a public sector body responsible for an authentic source (PuB-EAA) Providers"
  - "3.8 Non-Qualified Electronic Attestation of Attributes (EAA) Providers"
  - "3.9 Qualified Electronic Signature Remote Creation (QESRC) Providers"
  - "3.10 Authentic Sources"
  - "3.11 Relying Parties, Relying Party Instances, and intermediaries"
  - "3.12 Conformity Assessment Bodies (CAB)"
  - "3.13 Supervisory Bodies"
  - "3.14 Device Manufacturers and Related Subsystems Providers"
  - "3.15 Attestation Scheme Providers for QEAAs, PuB-EAAs and EAAs"
  - "3.16 National Accreditation Bodies"
  - "3.17 Registrars"
  - "3.18 Access Certificate Authorities"
  - "3.19 Providers of registration certificates"
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~7207 -->

## 3. Roles within the EUDI Wallet ecosystem

### 3.1 Introduction

This chapter describes the EUDI Wallet ecosystem as it is foreseen in the [European
Digital Identity Regulation]. The different roles in the EUDI Wallet ecosystem
are depicted in Figure 1 and described in the following sections.

Note that a single entity may combine multiple of the roles depicted in
the figure, as long as that entity complies with all requirements, both legal
and technical, for each of the roles. In addition, potential conflicts of
interest are to be avoided, but this issue is outside the scope of this ARF.

![Figure 1: Overview of the EUDI Wallet ecosystem roles](media/Figure_1_Overview_of_EUDI_Wallet_roles.png)
*Figure 1: Overview of the EUDI Wallet ecosystem roles*

The table below summarizes the key roles in the EUDI Wallet ecosystem, as shown in Figure 1. Each role
is detailed in the corresponding referenced section.

| Role | Primary Responsibility | Section |
| ------------------------------ | ------------------------------------ | --------------------- |
| **User of Wallet Unit** | Manage, store, and present PIDs/attestations. | [Section 3.2](#32-users-of-wallet-units) |
| **Wallet Provider** | Make the certified Wallet Solution available to Users. | [Section 3.3](#33-wallet-providers) |
| **PID Provider** | Issue Person Identification Data (PID) to Users. | [Section 3.4](#34-person-identification-data-pid-providers) |
| **Trusted List or LoTE Provider** | Maintain, manage, and publish Trusted Lists and/or Lists of Trusted Entities. | [Section 3.5](#35-trusted-list-or-lote-provider) |
| **QEAA Provider** | Issue Qualified Electronic Attestations of Attributes (QEAAs). | [Section 3.6](#36-qualified-electronic-attestation-of-attributes-qeaa-providers) |
| **PuB-EAA Provider** | Issue EAAs on behalf of a public sector body. | [Section 3.7](#37-eaa-issued-by-or-on-behalf-of-a-public-sector-body-responsible-for-an-authentic-source-pub-eaa-providers) |
| **EAA Provider** | Issue Non-Qualified Electronic Attestations of Attributes (EAAs). | [Section 3.8](#38-non-qualified-electronic-attestation-of-attributes-eaa-providers) |
| **Qualified Electronic Signature Remote Creation (QESRC) Provider** | Provide Qualified Electronic Signature Remote Creation services. | [Section 3.9](#39-qualified-electronic-signature-remote-creation-qesrc-providers) |
| **Authentic Source** | Act as the definitive repository for specific attributes. | [Section 3.10](#310-authentic-sources) |
| **Relying Party (RP) / Intermediary** | Request and receive attributes from a Wallet Unit. | [Section 3.11](#311-relying-parties-relying-party-instances-and-intermediaries) |
| **Conformity Assessment Body (CAB)** | Certify Wallet Solutions and audit Trust Service Providers. | [Section 3.12](#312-conformity-assessment-bodies-cab) |
| **Supervisory Body** | Review the proper functioning of ecosystem actors. | [Section 3.13](#313-supervisory-bodies) |
| **Device Manufacturers / Subsystems** | Provide the underlying platform (hardware, OS, secure elements). | [Section 3.14](#314-device-manufacturers-and-related-subsystems-providers) |
| **Attestation Scheme Provider** | Define and publish the Attestation Rulebooks and schemes. | [Section 3.15](#315-attestation-scheme-providers-for-qeaas-pub-eaas-and-eaas) |
| **National Accreditation Body (NAB)** | Accredit CABs according to EU regulations. | [Section 3.16](#316-national-accreditation-bodies) |
| **Registrar** | Manages the registration of Providers and Relying Parties. | [Section 3.17](#317-registrars) |
| **Access Certificate Authority (Access CA)** | Issue access certificates for authentication. | [Section 3.18](#318-access-certificate-authorities) |
| **Provider of Registration Certificates** | Issue certificates detailing registration status and scope. | [Section 3.19](#319-providers-of-registration-certificates) |

### 3.2 Users of Wallet Units

Users of Wallet Units use the Wallet Unit to receive, store, and present PIDs,
QEAAs, PuB-EAAs, or non-qualified EAAs to Relying Parties. Users can also create
qualified electronic signatures and seals (QES) and create and present
pseudonyms.

[CIR 2024/2982](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202402982)
(among others) defines 'wallet user' as 'a user who is in control of the wallet
unit'. Being in control of the Wallet Unit implies being able to present a PID
or attestation to a Relying Party. Within the use cases described in the current
version of the ARF, the User is the subject of the PID(s) in the Wallet Unit.
The User is also the subject of most of the attestations in the Wallet Unit, but
there could be attestations related to objects owned or used by the User, such as a vehicle registration card. Additionally, the Wallet Unit could contain attestations that have no subject, such as vouchers. Such attestations will be valid for any User that can present it
to a Relying Party.

Please note that:

- the topic of Wallet Units for legal persons, possibly containing a legal-person PID, has has been removed from this ARF in view of the development of a separate business wallet.
- this ARF assumes that a User device is a personal device,
meaning that the User will not share it with other people, and that only the
User can access and control the Wallet Unit. This also implies that all PIDs and
attestations on the Wallet Unit pertain to that User (or to entities represented
by, or objects owned by or linked to, that User).

The use of a Wallet Unit by citizens is not mandatory under the [European
Digital Identity Regulation]. However, each Member State will provide at least
one European Digital Identity Wallet within 24 months after the entry into force
of the Implementing Acts referred to in the [European Digital Identity
Regulation].

### 3.3 Wallet Providers

Wallet Providers are Member States or organisations either mandated or
recognised by Member States making a Wallet Solution available to Users. All
Wallet Solutions must be certified as described in [Chapter 7](#7-wallet-solution-certification-and-risk-management).

A Wallet Provider makes a combination of several products and Trust Services
available to a User, which give the User sole control over the use of their
Person Identification Data (PID) and Electronic Attestations of Attributes
(QEAA, PuB-EAA or EAA), and any other personal data within their Wallet Unit.
This also implies guaranteeing a User sole control over sensitive cryptographic
material (e.g., private keys) related to their Wallet Unit.

Wallet Providers are responsible for ensuring compliance with the requirements
for Wallet Solutions.

From the viewpoint of the other actors in the EUDI Wallet ecosystem, the Wallet
Provider is responsible for all components of the Wallet Unit. These components
are described in [Section 4.3.2](#432-components-of-a-wallet-unit). In
particular, the Wallet Provider is responsible for ensuring that the Wallet
Instance can access a Wallet Secure Cryptographic Device (WSCD) that has a level
of security sufficient to ensure that the Wallet Unit can achieve Level of
Assurance High, as required in the [European Digital Identity Regulation] for the PID.
This is true even if the WSCD is not delivered by the Wallet Provider but
is integrated into the User device.
For more information, see [Section 4.5](#45-wscd-architecture-types). Other actors
in the ecosystem do not need to interact with or explicitly trust a WSCA or WSCD
supplier. As explained in [Section 6.5.3.4](#6534-wallet-provider-issues-one-or-more-wuas-to-the-wallet-unit)),
Wallet Providers sign Wallet Unit Attestations (WUA) and Wallet Instance Attestations (WIA) and issue them to the Wallet Unit. A WUA
attests that the Wallet Unit and all of its components, including the WSCA/WSCD or keystore and the public keys included in the WUA,
comply with the relevant requirements. A WIA only attests the integrity of the Wallet Instance (i.e., the app installed on the User device).

### 3.4 Person Identification Data (PID) Providers

PID Providers are trusted entities responsible for:

- verifying the identity of the User in compliance with LoA high requirements,
- issuing a PID to the Wallet Unit, and
- making available, in a privacy-preserving way, information for Relying Parties
to verify the validity of the PID.

The terms and conditions of these services are for each Member State to determine.

PID Providers may be the same organisations that today issue official identity
documents, electronic identity means, etc. PID Providers may be the same
organisations as Wallet Providers. In case an organisation acts as both a PID
Provider and a Wallet Provider, it complies with all requirements for both PID
Providers and Wallet Providers.

### 3.5 Trusted List or LoTE Provider

A Trusted List or LoTE Provider is a body responsible for maintaining, managing,
and publishing Trusted Lists and/or Lists of Trusted Entities (LoTE).

Within the EUDI Wallet ecosystem, Trusted Lists exist for the following entities:

- QEAA Providers, see [Section 3.6](#36-qualified-electronic-attestation-of-attributes-qeaa-providers),
- PuB-EAA Providers, see [Section 3.7](#37-eaa-issued-by-or-on-behalf-of-a-public-sector-body-responsible-for-an-authentic-source-pub-eaa-providers).

Lists of Trusted Entities exist for:

- Wallet Providers, see [Section 3.3](#33-wallet-providers),
- PID Providers, see [Section 3.4](#34-person-identification-data-pid-providers),
- Access Certificate Authorities, see [Section 3.18](#318-access-certificate-authorities),
- Providers of registration certificates, see [Section 3.19](#319-providers-of-registration-certificates).

Notes:

- There is no Trusted List or LoTE for Relying Parties. The expected number of Relying
Parties in the Union would make this infeasible. Instead, a Relying Party
receives one or more access certificate(s) from an Access Certificate Authority (see [Section 3.18](#318-access-certificate-authorities)), and these
certificates allow a Wallet Unit to authenticate the Relying Party.
- Wallet Providers, PID Providers, Access Certificate Authorities, and Providers
of registration certificates are not trust service providers in the sense of the
[European Digital Identity Regulation]. For that reason, they are included in a LoTE, not in a Trusted List in the sense of [Article 22](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv%3AOJ.L_.2014.257.01.0073.01.ENG#d1e2162-73-1).
- Non-qualified EAA Providers are trust service providers in the sense of the
[European Digital Identity Regulation]. Therefore, Trusted Lists and Trusted
List Providers may also exist for non-qualified EAA Providers. However, this is
out of scope of the ARF.

These Trusted Lists and LoTEs are described in more detail in [Sections 6.2.2](#622-wallet-provider-notification),
[6.3.2](#632-pid-provider-or-attestation-provider-registration-and-notification)
and [6.4.2](#642-relying-party-registration). Some
Trusted Lists or LoTEs contain the trust anchors of the relevant entities. A trust anchor
is a combination of a public key and the identifier of the associated entity and
may be used to verify signatures created by that entity.

An entity's status as a trusted entity can be verified by checking whether they
are present on the relevant Trusted List or LoTE. In order to be put on a Trusted List or LoTE, relevant entities must be notified to the Commission by a Member State. For all mentioned entities except Wallet Providers, this
happens after the entity has been registered by a Registrar in the Member State,
see [Section 3.17](#317-registrars).

For more information and high-level requirements, please refer to [Topic 27](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2316-topic-27---registration-of-pid-providers-providers-of-qeaas-pub-eaas-and-non-qualified-eaas-and-relying-parties)
and to [Topic 31](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2320-topic-31---pid-provider-wallet-provider-attestation-provider-and-access-certificate-authority-notification-and-publication).

### 3.6 Qualified Electronic Attestation of Attributes (QEAA) Providers

Qualified EAAs are provided by Qualified Trust Service Providers (QTSPs). The
general trust framework for QTSPs (see Chapter III, Section 3 of the [European
Digital Identity Regulation] applies also to QEAA Providers, but specific rules
for the Trust Service of issuing QEAAs may be defined as well.

QEAA Providers maintain an interface to Wallet Units to provide QEAAs upon
request. Potentially, they also maintain an interface towards Authentic Sources
to verify the value of User attributes, as specified in
[Topic 42](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2324-topic-42---requirements-for-qtsps-to-access-authentic-sources).

It is likely that for most QEAAs, a QEAA Provider will need to verify the
identity of a User when issuing a QEAA. It is up to each QEAA Provider to
implement the necessary User authentication processes, in compliance with all
applicable national and Union legislation. Note that, when User identity
verification is necessary, it is likely that the User requesting a QEAA already
possesses a PID. This would enable the QEAA Provider to carry out User
identification and authentication at LoA high, by requesting and verifying
User attributes from the PID in the Wallet Unit.

The terms and conditions of these services are for each QEAA Provider to
determine, beyond what is specified in the [European Digital Identity Regulation].

### 3.7 EAA issued by or on behalf of a public sector body responsible for an authentic source (PuB-EAA) Providers

As specified in the [European Digital Identity Regulation], an attestation may
be issued by or on behalf of a public sector body responsible for an Authentic
Source. This ARF calls such an attestation a PuB-EAA. For a description of
Authentic Sources, see [Section 3.10](#310-authentic-sources). A public sector
body primarily is a state, regional or local authority, or a body governed by
public law.

A PuB-EAA Provider, meaning a public sector body issuing PuB-EAAs, is not a
QTSP. However, a PuB-EAA Provider has a qualified certificate, issued by a QTSP,
that allows it to sign PuB-EAAs. A Relying Party verifies a PuB-EAA by first
verifying the signature over the PuB-EAA, and subsequently verifying the
signature of the qualified PuB-EAA Provider certificate. For more details, refer
to [Section 6.6.3.6](#6636-relying-party-instance-verifies-the-authenticity-of-the-pid-or-attestation).
The [European Digital Identity Regulation] stipulates that PuB-EAAs, like QEAAs,
have the same legal effect as attestations in paper form. It is up to the Member
States to define terms and conditions for the provisioning of PuB-EAAs, but
PuB-EAA Providers will comply with the same technical specifications and
standards as Providers of PIDs and other attestations.

For the precise and legally binding definitions and obligations regarding the
issuance of PuB-EAAs, please refer to the [European Digital Identity Regulation].

### 3.8 Non-Qualified Electronic Attestation of Attributes (EAA) Providers

Non-qualified EAAs can be provided by any (non-qualified) Trust Service
Provider. While they will be supervised under the [European Digital Identity
Regulation], it can be assumed that other legal or contractual frameworks will
mostly govern the rules for provision, use and recognition of EAAs. Those other
frameworks may cover policy areas such as educational credentials, digital
payments, although they may also rely on Qualified Electronic Attestation of
Attributes Providers. For non-qualified EAAs to be used, EAA Providers offer
Users a way to request and obtain these EAAs. This implies that these
non-qualified EAA Providers comply with the Wallet Unit interface
specifications. The terms and conditions of issuing EAAs and related services
are subject to sectoral rules.

### 3.9 Qualified Electronic Signature Remote Creation (QESRC) Providers

The Wallet Unit will allow the User to create qualified electronic signatures or
seals over any data. This will also enhance the use of the Wallet Unit for
signing, in a natural and convenient way. The creation of a qualified electronic
signature or seal by the Wallet Unit can be achieved by means of a local QSCD, as discussed in [Section 4.3.2](#432-components-of-a-wallet-unit).

However, the Wallet Unit can also connect to a remote QSCD managed by a QTSP, called a Qualified Electronic Signature Remote Creation (QESRC) Provider. As part of the EUDI Wallet ecosystem, the use of common interfaces and protocols for provisioning qualified electronic signatures and seals will create a unified European market for QESRC Providers.

Besides providers of qualified electronic signatures and seals, also remote providers
of non-qualified electronic signatures or seals may exist. However, such
providers are out of scope of this ARF.

### 3.10 Authentic Sources

Authentic Sources are public or private repositories or systems, recognised or
required by law, containing attributes about natural or legal persons. Authentic
Sources are sources for attributes on, for instance, address, age, gender, civil
status, family composition, nationality, education and training qualifications
titles and licences, professional qualifications titles and licences, public
permits and licences, or financial and company data.

Authentic Sources are required to provide an interface to QEAA Providers to
verify the authenticity of the above attributes, either directly or via
designated intermediaries recognised at national level. Authentic Sources may
act as PuB-EAA Providers if they meet the requirements of the [European Digital
Identity] Regulation, see [Section 3.7](#37-eaa-issued-by-or-on-behalf-of-a-public-sector-body-responsible-for-an-authentic-source-pub-eaa-providers).
In [Figure 1](#31-introduction) this is indicated by the arrow 'provides
qualified data'.

### 3.11 Relying Parties, Relying Party Instances, and intermediaries

#### 3.11.1 Relying Parties

A Relying Party is a service provider requesting attributes contained within a
PID, QEAA, PuB-EAA or EAA from the Wallet Unit, subject to the approval of the
User and within the limits of applicable legislation and rules.

> Note: As specified in the [European Digital Identity Regulation], legally
speaking, the term 'Relying Party' includes Attestation Providers (i.e., QEAA
Providers, PuB-EAA Providers, and non-qualified EAA Providers), as well as
service providers. However, technically speaking the responsibilities of
Attestation Providers are quite different from those of service providers, as is
the way they interact with Wallet Units. Therefore, for clarity the term
'Relying Party' is used in all parts of the ARF exclusively to mean a service
provider interacting with a Wallet Unit to request and receive attributes from
an attestation.

The reason for a Relying Party to rely on the Wallet Unit may be a legal
requirement, a contractual agreement, or their own decision. In particular, the
[European Digital Identity Regulation] requires that providers of very large
online platforms must accept the EUDI Wallet for their user authentication
processes.

To rely on Wallet Units for the purpose of providing a service, Relying Parties
register at a Registrar in the Member State where they are established.
Registration includes the attributes that the Relying Party intends to request
from Wallet Units. See [Section 6.4.2](#642-relying-party-registration) for more
information on Relying Party registration. When processing a presentation
request, a Wallet Unit verifies that the Relying Party only requests attributes
that it registered, if the User has indicated that such a check must be
performed. The Wallet Unit will warn the User if this is not the case. This is
explained in [Section 6.6.3.3](#6633-wallet-unit-allows-user-to-verify-that-relying-party-does-not-request-more-attributes-than-it-registered).

In addition, an Attestation Provider may embed a disclosure policy in an
attestation. Such a policy indicates to which Relying Parties a Wallet Unit
should (or should not) present that attestation. When processing a presentation
request, the Wallet Unit evaluates the policy based on data provided by the
Relying Party, and warns the User if the outcome of that evaluation is
negative. Please refer to [Section 6.6.3.4](#6634-wallet-unit-evaluates-embedded-disclosure-policy-if-present)
for more information.

#### 3.11.2 Relying Party Instances

A Relying Party uses a system consisting of software and hardware to interact
with Wallet Units. The ARF calls such a system a Relying Party Instance. A
Relying Party Instance maintains an interface with Wallet Units to request PIDs and attestations. It implements Relying Party authentication, using an access
certificate obtained by the Relying Party, as described in
[Section 6.6.3.2](#6632-wallet-unit-authenticates-the-relying-party-instance).
Note that a Relying Party can operate multiple Relying Party Instances.

#### 3.11.3 Intermediaries

So-called intermediaries form a special class of Relying Party. Article 5b (10)
of the [European Digital Identity Regulation] states "Intermediaries acting on
behalf of relying parties shall be deemed to be relying parties and shall not
store data about the content of the transaction". Such an intermediary is a
party that offers services to Relying Parties to, on their behalf, connect to
Wallet Units and request the User attributes that these Relying Parties need.
The intermediary then sends the presented attributes to the intermediated
Relying Party. This implies that an intermediary performs all tasks assigned to
a Relying Party in this ARF on behalf of the intermediated Relying Party.

For a more detailed description of the interactions between an intermediated Relying Party, an intermediary, and a Wallet Unit, see [Section 6.6.5](#665-pid-or-attestation-presentation-to-an-intermediary).

### 3.12 Conformity Assessment Bodies (CAB)

Conformity Assessment Bodies (CAB) are public or private bodies that are
accredited by a national accreditation body, which itself is designated by
a Member State according to [Regulation 765/2008](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:32008R0765)
Article 6c (3). In particular, CABs are accredited to carry out assessments on
which Member States will rely before issuing a Wallet Solution or providing the
'qualified' status to a Trust Service Provider.

Wallet Solutions will be certified by CABs. QTSPs will be audited regularly by CABs.

The standards and schemes used by CABs to fulfil their tasks to certify Wallet
Solutions are discussed in [Chapter 7](#7-wallet-solution-certification-and-risk-management).

### 3.13 Supervisory Bodies

Supervisory Bodies review the proper functioning of Wallet Providers and other
actors in the EUDI Wallet ecosystem. Supervisory Bodies will be created and
appointed by the Member States. The Supervisory Bodies will be notified to the
Commission by the Member States.

### 3.14 Device Manufacturers and Related Subsystems Providers

In the EUDI Wallet ecosystem, commercial actors such as device manufacturers and
related subsystems providers fulfil an important role to enable a Wallet Unit to
work smoothly and securely. Device manufacturers and related subsystem providers
provide a platform on which a Wallet Unit can be built. Wallet Providers ensure
that their Wallet Units use that platform to ensure usability, security,
stability and connectivity. The components provided by device manufacturers and
providers of related subsystems may include, among others, hardware, operating
systems, secure cryptographic hardware, libraries, and app stores.

### 3.15 Attestation Scheme Providers for QEAAs, PuB-EAAs and EAAs

An Attestation Scheme Provider defines a specific attestation type (e.g., QEAA,
PuB-EAA, or EAA) and publishes two complementary artefacts:

1. A human-readable Attestation Rulebook; see [Section 5.4](#54-attestation-rulebooks-and-attestation-schemes),
the authoritative documentation that explains what the attestation represents
and how it works, detailing identifiers, semantics, encodings, constraints, and
processing rules, trust model;
2. A machine-readable attestation scheme that
mirrors the Rulebook so software can build requests to Wallet Units and validate
responses at runtime.

Relying Parties use the Rulebook to decide whether and how to adopt an
attestation and to prepare their systems, while their Relying Party Instances
rely on the attestation scheme in production.

For PID, the European Commission publishes the applicable
Rulebook.

Moreover, the Commission operates a catalogue of schemes and Rulebooks, setting
the related technical specifications, standards, and procedures, so ecosystem
participants can discover available attestations and understand how to request
and verify their attributes; A broad array of attestation schemes, including
sector-specific ones, is critical for interoperability and uptake. For more
information see [Section 5.5](#55-catalogue-of-attributes-and-catalogue-of-attestation-schemes).

### 3.16 National Accreditation Bodies

National Accreditation Bodies (NAB), under [Regulation (EC) No 765/2008](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:32008R0765),
are the bodies in Member States that perform accreditation with authority
derived from the Member State. NABs accredit CABs ([Section 3.12](#312-conformity-assessment-bodies-cab))
as competent, independent, and supervised professional certification bodies in
charge of certifying Wallet Solutions against normative document(s) establishing
the relevant requirements. NABs monitor the CABs to which they have issued an
accreditation certificate.

### 3.17 Registrars

All PID Providers, QEAA Providers, PuB-EAA Providers, non-qualified EAA
Providers and Relying Parties in the EUDI Wallet ecosystem are registered by a
Registrar in the Member State where they reside. As a result of registering an
entity,

- Data about the entity is registered by the Registrar and made available online
in human-readable and machine-readable format to any interested party. In
particular,
    - For a Relying Party, the Registrar mainly registers which attributes the
    Relying Party intends to request from Wallet Units, and for what purpose.
    The Registrar also registers if the Relying Party intends to use the
    services of an intermediary (see [Section 3.11.3](#3113-intermediaries)) to
    interact with Wallet
    Units, and if so, which one.
    - For a PID Provider, QEAA Provider, PuB-EAA Provider, or non-qualified EAA
    Provider, the Registrar registers the attestation type(s) this entity wants
    to issue to Wallet Units, for example, diplomas, driving licenses, or vehicle
    registration cards.
- Registered entities receive one or more access certificate(s) from an Access Certificate
Authority, as described in [Section 3.18](#318-access-certificate-authorities).
- If supported by the Registrar, a registered entity also receives a
registration certificate, as discussed in [Section 3.19](#319-providers-of-registration-certificates).

The process and terms and conditions for registering will be determined by each
Member State.

### 3.18 Access Certificate Authorities

Access Certificate Authorities issue an access certificate to all PID Providers,
QEAA Providers, PuB-EAA Providers, and non-qualified EAA Providers in the EUDI Wallet ecosystem. In addition, each Relying Party in the ecosystem also receives one or more access certificates, one for each of its Relying Party Instances. When these entities interact with a Wallet Unit to issue or request a PID or attestation, they will present an access
certificate to prove their authenticity and validity. In order to receive an
access certificate, an entity must be registered by a Registrar as described in
[Section 3.17](#317-registrars).

> Note: In the Implementing Acts, the term ‘wallet-relying party access certificate’ refers to the certificate used by relying parties to authenticate towards wallets. The ARF further clarifies that a Relying Party may operate multiple technical systems (‘Relying Party Instances’, see [Section 3.11.2](#3112-relying-party-instances)) to interact with Wallet Units, and that each of these needs a separate access certificate to do so. However, the legal subject of all of these access certificates is the wallet-relying party.

Access Certificate Authorities are notified by a Member State to the Commission.
As part of the notification process, the trust anchors of the Access CA are
included in a List of Trusted Entities (LoTE) by a Trusted List or LoTE Provider. A trust anchor is the
combination of a public key and an identifier for the associated entity. Wallet
Units need these trust anchors to verify the signatures over the access
certificates presented to them when a new PID or attestation is issued or when
they receive an attribute presentation request from a Relying Party.

The Trusted List or LoTE Provider signs and publishes the Access CA LoTE and
makes the URL of the LoTE available to a common trust infrastructure
maintained by the Commission. Using the
common infrastructure, any entity in the EUDI Wallet ecosystem will be able to
find all Trusted Lists and LoTEs in the ecosystem.

In order to enable detection of any event in which an access certificate was
issued erroneously or fraudulently, an
Access Certificate Authority logs all access certificates in a Certificate
Transparency log, once such a log is available for access certificates. For
more information, see the [Discussion Paper for Topic S](./discussion-topics/s-certificate-transparancy.md).
For high-level requirements on Certificate Transparency, see [Topic 55](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2333-topic-55---certificate-transparency).

### 3.19 Providers of registration certificates

If a Registrar has a policy of issuing registration certificates, it has one or
more associated Provider(s) of registration certificates. Such a Provider issues
one or more registration certificates to each registered Relying Party, PID
Provider, QEAA Provider, PuB-EAA Provider, and non-qualified EAA Provider. Each
registration certificate contains (a subset of) the data registered for that
entity, as described in [Section 3.17](#317-registrars).

A registration certificate is signed by the Provider of registration
certificates that issued it. Commission Implementing Regulation 2024/2982
requires a Wallet Unit to authenticate and validate the registration
certificate, if available. If no registration certificate is available, the same
information can also be retrieved from the Registrar's online service. This
enables Users:

- for a Relying Party they are interacting with, to verify that the attributes
being requested by the Relying Party are within the scope of their registered
attributes. This provides assurance that the request is legitimate and
trustworthy.
- for a PID Provider or Attestation Provider they are interacting with, to
verify that the issued attestation is within the scope of their registered
attestations. This provides assurance that the attestation is legitimate and
trustworthy.

Like Access Certificate Authorities (see previous section), Providers of
registration certificates are notified by a Member State to the Commission.
Their trust anchors are put on a List of Trusted Entities, such that they can be found by
Wallet Units and used to verify a registration certificate received from a
Relying Party.
