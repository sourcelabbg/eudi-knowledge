---
name: "arf-wallet-lifecycle"
description: "Use when implementing Wallet Unit lifecycle: installation, activation (device data collection, user authentication setup, WUA/WIA issuance), management, and uninstallation."
sections:
  - "6.5 Trust throughout a Wallet Unit lifecycle"
  - "6.5.1 Wallet Unit lifecycle"
  - "6.5.2 Wallet Instance installation"
  - "6.5.3 Wallet Unit activation"
  - "6.5.4 Wallet Unit management"
  - "6.5.5 Wallet Instance uninstallation"
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~9075(LARGE) -->

### 6.5 Trust throughout a Wallet Unit lifecycle

#### 6.5.1 Wallet Unit lifecycle

[Section 4.6.4](#464-wallet-unit) above presented the lifecycle of a Wallet Unit:

1. The Wallet Instance that is part of the Wallet Unit is installed on a device
by a User. The required trust relationships for installation are discussed in
[Section 6.5.2](#652-wallet-instance-installation) below.
2. Next, the Wallet Unit is activated by the Wallet Provider and the User and
becomes operational. The goals and required trust relationships for activation
are discussed in [Section 6.5.3](#653-wallet-unit-activation).
3. Once in the **Operational** or **Valid** state, the Wallet Unit is managed by
the User and the Wallet Provider. This management includes at least revoking the
Wallet Unit when necessary. This is discussed in [Section
6.5.4](#654-wallet-unit-management). Management will also include regular
updates of the Wallet Instance application to ensure its continued security and
functionality. However, this is not further defined in this chapter.
4. The User may uninstall the Wallet Instance; see [Section 6.5.5](#655-wallet-instance-uninstallation).

#### 6.5.2 Wallet Instance installation

##### 6.5.2.1 Required trust relationships

The lifecycle of a Wallet Unit starts when a User decides to install a Wallet
Instance application on their device. This application in an instance of a
Wallet Solution, which is provided to the User by a Wallet Provider.

When downloading and installing the Wallet Instance, the following trust
relationships are established:

1. On behalf of the User, the OS of the User's device and the relevant app store
verify that the Wallet Instance (i.e., the application the User is installing)
is genuine and authentic and does not contain any malware or other threats.
2. The User verifies that they can obtain the PID(s) they need in an instance of
this Wallet Solution. If the relevant PID Provider does not support the Wallet
Solution, the User will not be able to use the Wallet Unit for obtaining those
PID(s).

The next two sections discuss these trust relationships. For high-level
requirements regarding Wallet Instance installation, see [Topic 40](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2323-topic-40---wallet-instance-installation-and-wallet-unit-activation-and-management),
section A.

##### 6.5.2.2 Wallet Solution authenticity is verified

To ensure that the User can trust the Wallet Solution, Wallet Providers
preferably make their certified Wallet Solutions available for installation via
the official app store of the relevant operating system (e.g., Android, iOS).
This allows the operating system of the device to perform relevant checks
regarding the authenticity of the app. It also allows Users to use the same
well-known channel for obtaining a Wallet Instance as they use for obtaining
other apps. Finally, it avoids a situation where a User must allow side-loading
of apps, which would increase the risk of unintentionally installing malicious
apps.

If a Wallet Provider makes its Wallet Solution available for installation
through other means than the official OS app store, it implements a mechanism
allowing the User to verify the authenticity of the Wallet Unit. Moreover, the
Wallet Provider provides clear instructions to the User on how to install the
Wallet Unit, including:

- instructions on how to verify the authenticity of the Wallet Instance to be
installed. This can be done, for example, by comparing the hash value of the
application downloaded by the User with a hash value published by the Wallet
Provider.
- instructions on bypassing of any operating system limitations on side-loading
of apps, if applicable, and ensuring that these limitations are restored after
the Wallet Instance has been installed.

Note: The [European Digital Identity Regulation] does not exclude the
possibility that a Wallet Instance may be installed on a non-mobile device, for
example a server. The requirements above also apply for the installation of a
Wallet Unit on a User device that is not a mobile device, and for which no
official operating system app store may exist.

##### 6.5.2.3 User validates that Wallet Solution is usable with relevant PID

A User installs a Wallet Unit because they want to obtain and use one or more
PIDs. However, PID Providers are not required to support all Wallet Solutions in
the EUDI Wallet ecosystem. 'Support' here means that the PID Provider is willing
to issue a PID to an instance of a given Wallet Solution on request of the User.
Instead, a PID Provider may choose to support only a single Wallet Solution or a
limited number of Wallet Solutions. Therefore, each PID Provider will publish a
list of Wallet Solutions that they support, such that a User that wants to
request a PID from that PID Provider knows which Wallet Unit they should
install. This list could be published, for example, on the PID Provider's
website.

Conversely, a Wallet Solution is not required to support all PID Providers,
where 'support' means that it is able to request the issuance of a PID from a
PID Provider. Each Wallet Provider will, prior to or during installation of a
Wallet Instance, let the User know which PID Providers are supported by this
Wallet Solution.

For QEAAs, PuB-EAAs, and non-qualified EAAs, the situation is different.
Providers of such attestations will support all Wallet Solutions and are not
allowed to discriminate between them when processing a request for the issuance
of an attestation. Conversely, a Wallet Solution supports all Attestation
Providers, and cannot discriminate between different Attestation Providers when
requesting the issuance of an attestation at the User's request.

#### 6.5.3 Wallet Unit activation

##### 6.5.3.1 Introduction

After installation of the Wallet Instance, the new Wallet Instance will contact
the Wallet Provider to start the activation process. For successful Wallet Unit
activation, the following trust relations are established:

1. The Wallet Instance authenticates the Wallet Provider, meaning that
the instance is sure that it is dealing with the genuine Wallet Provider who
provided it to the User.
2. The Wallet Provider authenticates the Wallet Instance. This means
that the Wallet Provider is sure that the instance is indeed a true
instance of their Wallet Solution, and not a fake app.

Both of these trust relationships are the responsibility of the Wallet Provider.
The ARF does not specify how these trust relationships can be satisfied.

During the activation process, at least the following steps happen:

1. The Wallet Provider requests data about the User's device from the Wallet
Instance.
2. The Wallet Provider requests the User to set up at least one User
authentication mechanism.
3. The Wallet Provider issues one or more Wallet Unit Attestations to the Wallet Unit.
4. The Wallet Provider issues one or more Wallet Instance Attestations to the Wallet Unit.
5. The Wallet Provider sets up a User account for the User.

These steps are described in the sections below. For high-level requirements
regarding Wallet Unit activation, see [Topic 40](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2323-topic-40---wallet-instance-installation-and-wallet-unit-activation-and-management),
section B.

##### 6.5.3.2 Wallet Provider requests data about the User's device from the Wallet Instance

###### 6.5.3.2.1 Data collection for WSCA/WSCD and keystore deployment

The Wallet Instance connects to the Wallet Provider to be activated. Then, the
Wallet Provider requests data about the User's device from the Wallet Instance.
This data includes the characteristics of the WSCD(s) and keystores available to the device for securely storing cryptographic keys and data. The Wallet Provider needs this information to deploy a WSCA/WSCD in the Wallet Unit, and to be able to issue one or Wallet Unit Attestations to the Wallet Unit, see [Section 6.5.3.4](#6534-wallet-provider-issues-one-or-more-wuas-to-the-wallet-unit).

Notes:

- As discussed in [Section 4.5](#45-wscd-architecture-types), a WSCD may be
integrated directly within the User's device. Examples of this include an e-SIM,
a UICC, an embedded Secure Element, or native secure hardware accessible via the
device's OS. If so, the Wallet Instance will discover the presence of such a
WSCD during activation and will communicate the characteristics of the WSCD to
the Wallet Provider. In some cases, the Wallet Provider will subsequently deploy
a WSCA to the WSCD to facilitate communication between the Wallet Instance and
the WSCD.
- Sometimes, the User's device does not contain a local WSCD, or the local WSCD
does not have the security posture necessary to enable the Wallet Unit to be an
identity means at LoA High, or the Wallet Provider does not want to use a local
WSCD. In such a case, the Wallet Provider ensures the Wallet Unit gets access to
a remote HSM operated by the Wallet Provider.

###### 6.5.3.2.2 Data collection for Wallet Solution maintenance

In addition, the need for Wallet Solution maintenance may require the Wallet
Provider to monitor its operational Wallet Instances. It is customary for mobile
application developers to collect limited bug and error reports at runtime for
improvement purposes. Error logs collected never contain personal data of the
User. A list of possible data types to be collected, reasons for collection, and
how the Wallet Instance monitoring should occur (frequency, mechanisms, does the
collection require Wallet User's approval beyond standard app vendor practices)
is collected in the following table:

| Data type | Reason for monitoring (if applicable, regulation) | Monitoring frequency etc. |
| --- | --- | --- |
| Runtime errors | Uncaught errors in production code | runtime and crash logs |
| UX and telemetry information | UX field analysis, may not be used to obtain behavioural data | runtime logs - *user consent preferred* |
| OS version and health data | OS vulnerabilities | At Wallet Unit activation or OS update/upgrade and at continuous security posture monitoring |
| Wallet SDK and SW library versions | Wallet Instance code vulnerabilities | At Wallet Unit roll out (as part of CI/CD process), at continuous security posture monitoring |
| User locale/localisation data | Catching localisation related errors | runtime and crash logs - *user consent preferred* |
| Wallet Instance version | Old version related vulnerabilities or errors | At Wallet Unit activation, at continuous security posture monitoring |
| Supported WSCA/WSCDs | Cryptography related incompatibilities | At Wallet Unit activation, at continuous security posture monitoring |
| WSCx capabilities supported | Cryptography configuration for EUDI Wallet use cases | At Wallet Unit activation |
| Unique device identifier such as IDFV or persisted UUID (iOS) or AndroidID (Android) | Up-to-date list of Wallet Instance related device installations, potential malicious use (unrecognised identifier) | At Wallet Unit activation |
| Sensor identifiers and patch levels | Up-to-date sensor hardware | At Wallet Unit activation, at continuous security posture monitoring |
| Hardware-level details on device | Identify known hardware-based problems or vulnerabilities | At Wallet Unit activation |
| BLE radio presence | Security of proximity use cases | At Wallet Unit activation |
| NFC support | Security of proximity use cases | At Wallet Unit activation |

###### 6.5.3.2.3 Data collection for fraud or risk signal monitoring

Although complete fraud or risk signal collection is not in scope of the ARF,
Wallet Providers keep an active understanding of each individual Wallet
Instance's security posture, provided this can be done in a privacy-preserving
way. A list of information related to fraud or risk signals that is often
collected in context of mobile devices, is presented in the table below, with an
indication whether the data should be collected by the Wallet Provider.

| Data or tool type | Reason for security posture monitoring (if applicable, regulation) | Monitoring at Wallet Instance |
| --- | --- | --- |
| Device OS | Detect potential OS vulnerabilities | OK - see previous table |
| Device type | Detect potential type-specific vulnerabilities | OK - see previous table |
| Behavioural data | Detect unusual transaction detection, including possible account takeovers (ATO) | Not OK (privacy preservation) |
| Device fingerprinting | Flag logins from unfamiliar devices, ATO | Not relevant - Wallet Provider has list of devices with an active Wallet Instance |
| Geolocation (IP address) | Network-layer anomaly detection, ATO | Not OK (privacy preservation) |
| Geolocation (GNSS) | Geospatial anomaly detection, ATO | Not OK (privacy preservation) |
| Active phone call detection | Detect authorised push payment fraud / phishing / social engineering | Not OK (privacy preservation) |
| VPN detection | Detect attempted identity or location masking through VPN | Not OK |
| Incognito mode detection | Detect attempts at hiding malicious activity or multiple login attempts | Not relevant |
| Device rooting/jailbreaking detection | Detect compromised device security as a whole | OK |
| Emulator detection | Detect emulation of User device by fraudsters | OK |
| Malware detection | Identify and neutralise malicious software | OK |

For high-level requirements on Wallet Solution maintenance and the collection of
fraud and risk signals by Wallet Provider, see [Topic 56](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2334-topic-56---wallet-provider-support-and-maintenance).

##### 6.5.3.3 Wallet Unit requests User to set up two User authentication mechanisms

###### 6.5.3.3.1 Introduction

During Wallet Unit activation, the Wallet Unit ensures that the Users sets up
two User authentication mechanisms. The first of these mechanisms is implemented
by the OS of the User's device and will be used before any operation of the
Wallet Unit. The second mechanism is implemented by the WSCA/WSCD and will be
used additionally when a PID or an attestation bound to the WSCA/WSCD is issued,
presented, or deleted.

These two mechanisms are described in the next two subsections. See also the
requirements on User authentication in [Topic 40](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2323-topic-40---wallet-instance-installation-and-wallet-unit-activation-and-management),
Section C.

###### 6.5.3.3.2 OS-level User authentication before any operation

During Wallet Unit activation, the Wallet Instance forces the operating system
of the User's device to activate a multi-factor User authentication mechanism,
if this is not already active. One of the authentication factors for this
mechanism is the possession of the device and the other is knowledge-based or
inherence-based. The Wallet Instance ensures that the authentication mechanism
has security policies that are adequate for any operation of the Wallet Unit,
excluding the issuance or presentation of PIDs, WUAs describing the WSCA/WSCD,
and attestations bound to the WSCA/WSCD. As described in the next section, for
these actions User authentication by the WSCA/WSCD is necessary.

Actions for which OS-level authentication is sufficient include generating and
presenting pseudonyms, accessing the transaction log via the dashboard, data
export and migration, requesting the erasure of personal data by a Relying
Party, and reporting a Relying Party to a Data Protection Authority. It also
includes issuing, presenting, and deleting of attestations that are either not
device-bound or bound to a keystore rather than the WSCA/WSCD. This implies that
it must be possible to unlock the keystore(s) available to the Wallet Unit using
this User authentication mechanism.

The User can optionally decide to use a Wallet Instance-specific PIN in addition
to the OS-level User authentication mechanism.

User authentication to the Wallet Unit using the OS-level mechanism (plus
optional PIN) will take place whenever the User opens the Wallet Instance,
before the Wallet Unit performs any operation. This is necessary to prevent
anyone except the User from accessing the Wallet Unit and inspecting the User's
attestations and attribute values, as this data is personal and might be
sensitive.

###### 6.5.3.3.3 WSCA/WSCD-level User authentication before cryptographic operations

An additional User authentication, performed by the WSCA/WSCD, happens when the
Wallet Unit must perform any cryptographic operation involving cryptographic
assets in the WSCA/WSCD. This will happen at least when:

- The User instructs the Wallet Unit to request the issuance of a new PID, see
[Section 6.6.2](#662-pid-or-attestation-issuance),
- The Wallet Unit asks the User for approval to present some attributes from a
PID to a Relying Party, see [Section 6.6.3.5](#6635-wallet-unit-obtains-user-approval-for-presenting-selected-attributes),
- The User deletes a PID in their Wallet Unit, see [Section 6.6.7](#667-pid-or-attestation-deletion).

In addition, if an Attestation Provider requested during issuance that the
cryptographic assets of their attestation are stored and managed in the
WSCA/WSCD, the WSCA/WSCD will also perform User authentication before such an
attestation is issued, presented, or deleted.

Note that, as discussed in the first bullet in [Section 6.6.3.9](#6639-relying-party-instance-verifies-or-trusts-user-binding),
these User authentication mechanisms can also play a
role in ensuring User binding for PIDs or device-bound attestations. User
binding allows a Relying Party to trust that the person presenting a PID or
attestation is the User to whom the PID or the attestation was issued.

##### 6.5.3.4 Wallet Provider issues one or more WUAs to the Wallet Unit

During the activation of a Wallet Unit, the Wallet Provider issues one or more
Wallet Unit Attestations to the Wallet Unit. The Wallet Unit Attestation (WUA)
is a signed information object that has three main purposes:

- It describes the capabilities and properties of the Wallet Unit, and
especially a WSCA/WSCD or a keystore that is part of it. This allows a PID
Provider or an Attestation Provider to verify that the Wallet Unit complies with
the Provider's requirements and therefore is fit to receive a PID or a
device-bound attestation from the Provider.
- Moreover, the WUA is device-bound, meaning it contains one or more public
keys. The Wallet Provider attests that the private keys corresponding to these
public keys are managed by the WSCA/WSCD described in the WUA. During the
issuance of a PID or an attestation (see [Section 6.6.2.3](#6623-pid-provider-or-attestation-provider-validates-the-wallet-unit)),
a PID Provider or Attestation Provider can use each of these public keys to bind
a new PID or attestation to.
- Lastly, a WUA contains information allowing a PID Provider or an Attestation
Provider to verify that the Wallet Provider did not revoke the Wallet Unit
Attestation, and hence the Wallet Unit itself. The WUA and the revocation
mechanisms for Wallet Units are described in [Topic 38](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2322-topic-38---wallet-unit-revocation).

High-level requirements for the WUA can be found in [Topic 9](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a236-topic-9---wallet-unit-attestation-and-wallet-instance-attestation).
The detailed format of the WUA, as well as the way in which it is used, is
specified in the [Technical Specification 3](./technical-specifications/ts3-wallet-unit-attestation.md).

A Wallet Unit does not send a WUA to an Attestation Provider if the attestation
it is requesting is not device-bound. For non-device-bound attestations, the
Attestation Provider does not need to receive public keys to include in the
attestations, and neither does it need information about the WSCA/WSCD or
keystore.

To ensure User privacy, the Wallet Unit presents WUAs only to PID Providers and
Attestation Providers, but not to Relying Parties. This is because PID Providers
and Attestation Providers have a valid business reason to know these properties,
whereas Relying Parties do not. Moreover, a Wallet Unit will present each WUA
only once. Apart from preventing linkability, this is also to prevent that the
public keys in the WUA are used in multiple PIDs or attestations.

Regarding the WUA validity period, an important requirement in [CIR 2024/2977]
Article 5, 4.(b) is that a PID Provider must revoke a PID when the Wallet Unit
to which that PID was issued is revoked. Therefore, a PID Provider, must be able
to regularly check whether the Wallet Provider revoked the WUA the PID Provider
obtained from the Wallet Unit during PID issuance, during the entire validity
period of the PID. This implies that

- the validity period of a PID cannot exceed
the end of validity of the WUA received by the PID Provider during issuance.
Therefore, the validity period of WUAs needs to be sufficiently long; [Technical Specification 3](./technical-specifications/ts3-wallet-unit-attestation.md) requires that a Wallet Unit can always present a WUA for the WSCA/WSCD with a remaining validity period of at least 31 days.
- a WUA contains the information necessary to enable the PID Provider to do a revocation
check for the WUA. See also [Section 6.6.2.4](#6624-pid-provider-or-attestation-provider-verifies-that-wua-is-not-revoked).

The responsibilities of the Wallet Provider regarding issuance of a WUA are
similar to those of a PID Provider or Attestation Provider regarding the
issuance of a PID or an attestation. This means that after the initial issuance
of a WUA during activation, the Wallet Provider will manage the WUA and will
issue new WUAs to the Wallet Unit as needed, during the lifetime of the Wallet
Unit.

##### 6.5.3.5 Wallet Provider issues one or more WIAs to the Wallet Unit

During the activation of a Wallet Unit, the Wallet Provider also issues one or
more Wallet Instance Attestations (WIA) to the Wallet Unit. Similar to WUAs,
WIAs are information objects signed by the Wallet Provider. Like WUAs, they are
device-bound; they contain a public key. However, a WIA differs from a WUA in a
few aspects:

- WIAs contain information about the Wallet Instance only.
- WIAs are short-lived (less than 24 hours) and therefore do not contain
revocation information.
- The private key corresponding to the public key in the WIA is managed by the
Wallet Instance; it does not have to be managed by the WSCD/WSCA or a keystore.
- A Wallet Unit sends a WIA to an Attestation Provider for both device-bound and
non-device-bound attestations.

Similar to WUAs, Wallet Unit presents WIAs only to PID Providers and Attestation
Providers, but not to Relying Parties.

[Technical Specification 3](./technical-specifications/ts3-wallet-unit-attestation.md)
contains more information and requirements on the WIA.

##### 6.5.3.6 Wallet Provider sets up a User account for User

The User needs a User account at the Wallet Provider to ensure that they can
request the revocation of their Wallet Unit in case of theft or loss. The Wallet
Provider associates the Wallet Unit with the User account. The Wallet Provider
registers one or more backend-based User authentication methods that the Wallet
Provider will use to authenticate the User. Note that:

- The Wallet Provider does not need to know any real-world attributes of the
User, unless this is deemed necessary for PID activation, see [Section 6.6.2.6](#6626-user-activates-the-pid).
Otherwise, the User can use a pseudonym to register, for example an e-mail address.
If the Wallet Provider wants to request additional User attributes, for instance
to be able to provide additional services, they are free to do so if the User
consents.
- In any case, User details registered by the Wallet Provider will not be
included in a WUA or a WIA. They are strictly for use by the Wallet Provider only.

##### 6.5.3.7 Wallet Provider ensures User can verify they are using a trusted, certified Wallet Solution

According to the [European Digital Identity Regulation], the User needs to be
provided with a means to verify that they are installing or (after activation)
are indeed using a trusted, certified Wallet Solution. The solution specified in
this ARF to comply with this requirement is a Trust Mark view in the User
interface of the Wallet Instance. When the User invokes this Trust Mark, it:

- renders the official Trust Mark graphics and/or logo,
- shows an informational text about Wallet Solution certification, localised for
the User's device language, and
- provides web links to a list of certified Wallet Solutions, as well as to a
web page containing certification information of User's Wallet Solution.

The information in the third bullet is hosted and managed dynamically by the
European Commission. The [Technical Specification 1](./technical-specifications/ts1-eudi-wallet-trust-mark.md)
on the EUDI Wallet Trust Mark concentrates on defining the exact technical
contents and the provisioning process to enable the User interface view rendering at the
Wallet Instance.
[Topic 19](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2312-topic-19---user-navigation-requirements-dashboard-logs-for-transparency)
sets the high-level requirements for the Trust Mark as part of the Wallet Unit
dashboard functionality. [Topic 40](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2323-topic-40---wallet-instance-installation-and-wallet-unit-activation-and-management)
specifies what is required regarding the Trust Mark upon Wallet Unit activation
and maintenance.

#### 6.5.4 Wallet Unit management

##### 6.5.4.1 Introduction

Starting from Wallet Unit activation and until the Wallet Instance is
uninstalled by the User, a Wallet Unit is managed by the User and the Wallet
Provider. The Wallet Provider is responsible at least to:

- update the Wallet Unit by installing new versions of the Wallet Solution on
the User's device as necessary;
- update the WUAs and WIAs in the Wallet Unit as necessary; see [Sections 6.5.3.4](#6534-wallet-provider-issues-one-or-more-wuas-to-the-wallet-unit) and [6.5.3.5](#6535-wallet-provider-issues-one-or-more-wias-to-the-wallet-unit).
- revoke the Wallet Unit when needed; see [Section 6.5.4.2](#6542-wallet-unit-revocation).
- ensure that the Wallet Provider cannot access the contents of
the Wallet Unit, in particular to learn the value of any User attestations or
attributes, as well as the contents of the transaction log kept by the Wallet
Unit.
- support procedures for migrating the PIDs and attestations it contains to a different
Wallet Solution. See [Section 6.5.4.3](#6543-migrating-the-pids-and-attestations-in-a-wallet-unit-to-a-different-wallet-solution)

To allow Wallet Unit management, the following trust relations are established:

1. When contacting the Wallet Provider, for instance to request the revocation
of the Wallet Unit, the User authenticates the Wallet Provider. This means the
User is sure that they are visiting the website or the User portal of the
genuine Wallet Provider who is responsible for the User's Wallet Unit, and not a
spoofed website or portal. This risk can be partly mitigated by using standard
mechanisms such as TLS server authentication. However, in addition the User will
need to be vigilant as well, just as with any website on the internet.
1. When contacted by a User, the Wallet Provider authenticates the User. This
means that the Wallet Provider is sure that the User is indeed the User that was
associated with the Wallet Unit during activation. For this, the Wallet Provider
uses the authentication methods established in the User's account during
activation, see [Section 6.5.3](#653-wallet-unit-activation).A
1. When the Wallet Unit and the Wallet Provider set up a communication channel,
the Wallet Unit authenticates the Wallet Provider, meaning that the Wallet Unit
is sure that it is dealing with the genuine Wallet Provider. Similarly, the
Wallet Provider authenticates the Wallet Unit. This means that the Wallet
Provider is sure that the EUDI Wallet Instance is indeed a true instance of
their Wallet Solution, and not a fake app. This will be ensured by the Wallet
Provider. The ARF does not specify how these trust relationships can be
satisfied.
1. When contacted by a PID Provider to request Wallet Unit revocation, the
Wallet Provider authenticates the PID Provider. [Section 6.6.2.2](#6622-wallet-unit-authenticates-the-pid-provider-or-attestation-provider)
below describes how a Wallet Unit can do this during PID issuance; a Wallet
Provider can use the same mechanism.

For high-level requirements regarding Wallet Instance management, see [Topic 40](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2323-topic-40---wallet-instance-installation-and-wallet-unit-activation-and-management),
section C.

##### 6.5.4.2 Wallet Unit revocation

The Wallet Provider will revoke the Wallet Unit at least in the following circumstances:

- If the User requests the Wallet Provider to revoke the Wallet Unit,
for example in case of loss or theft of the User's device.
- If the Wallet Unit contains a PID, and the PID Provider requests the Wallet
Provider to revoke the Wallet Unit because the natural person using the Wallet
Unit has died. To identify the Wallet Unit that is to be revoked, the PID Provider uses a
Wallet Unit identifier provided by the Wallet Unit in the WUA during PID
issuance; see [Topic 9](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a236-topic-9---wallet-unit-attestation-and-wallet-instance-attestation).
This can be the same identifier used for enabling WUA revocation, for example an
URI to a Status List plus an index in that list; see [Topic 7](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a235-topic-7---attestation-revocation-and-revocation-checking).
- If the security of the Wallet Unit is breached or compromised.
- If the Wallet Solution is suspended (optionally) or when it is withdrawn
(mandatorily), see [Section 4.6.3](#463-wallet-solution).

Regarding the detection of a security breach or compromise in an individual
Wallet Unit, the Wallet Provider can use analysis mechanisms that allow
continuous detection of changes in signals relevant to the security posture of
the Wallet Instances it has deployed. These signals are discussed in [Section
6.5.3.2.3](#65323-data-collection-for-fraud-or-risk-signal-monitoring). The
Wallet Provider can potentially use a 4-level security posture framework as
introduced in the table below.

| Level | Posture status | Key indicators & checks | Wallet Provider policy response |
| ----- | -------------- | ----------------------- | ------------------------------- |
| **Level 4** | **Critical** (Red) | Confirmed Root/Jailbreak, Active Debugger/Emulator Detected, Private Key Compromised, Critical OS Vulnerability (unpatched) exploited, Wallet Instance integrity check failed (tampering detected), Use of a compromised WSCD-protected private key detected (**see also Note 1**). | Revocation of corresponding WUA(s). Force reinstallation of Wallet Instance on a vulnerability-free device before re-issuing WUAs. |
| **Level 3** | **High Risk** (Orange/Yellow) | High-risk, unpatched OS version detected, Failed biometric attempts exceeding high threshold, Unavailability of a local WSCA/WSCD due to repeated connection error or other errors. | Revocation of corresponding WUA(s). Require step-up authentication (e.g., PIN re-entry), or force re-activation of the Wallet Unit before re-issuing WUAs. |
| **Level 2** | **Moderate Risk** (Yellow/Green) | Minor integrity checks failed (e.g., non-critical file modification), Wallet Instance running in background with high resource usage, Failed PIN attempts (low threshold). | **Allow use, but limit scope** (e.g., restrict high-value presentations), force User re-authentication after inactivity. |
| **Level 1** | **Low Risk (Green)** | Successful device attestation, Wallet Instance integrity check passed, Current OS patch level. | **Full functionality** allowed, including presentation of high-value attestations (PID/QEAA). |

The Wallet Provider revokes a Wallet Unit by revoking its WUAs:

- If the Wallet Provider must revoke the entire Wallet Unit (for example by
request of the User or a PID Provider, or because there is a security breach of
the Wallet Instance or the OS of the User's device), then the Wallet Provider
revokes all WUAs related to keystores and to the WSCA/WSCD.
- If there is a security breach of the WSCA/WSCD, then the Wallet Provider
revokes the entire Wallet Unit by revoking all WUAs related to keystores and to
the WSCA/WSCD.
- If there is a security breach of a keystore, then the Wallet Provider at least
revokes all WUAs related to that keystore. The Wallet Provider also revokes the
WUAs related to the WSCA/WSCD and to the other keystores (if any), unless the
Wallet Provider creates a risk analysis showing that not doing this does not
lead to unacceptable risks. If the Wallet Provider does not revoke the other
WUAs, only the attestations bound to the revoked keystore will be impacted.
Other functionalities of the Wallet Unit, including the presentation of a PID,
will remain available to the User.

See [Section 4.6.4](#464-wallet-unit) for the full state diagram of the Wallet Unit. See [Section 6.6.2.4](#6624-pid-provider-or-attestation-provider-verifies-that-wua-is-not-revoked)
and sections referenced there for explanations of how PID Providers, Attestation
Providers, and Relying Parties deal with Wallet Unit revocation. See [Topic 38](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2322-topic-38---wallet-unit-revocation)
for high-level requirements on Wallet Unit revocation.

##### 6.5.4.3 Migrating the PIDs and attestations in a Wallet Unit to a different Wallet Solution

Article 5a 4 (g) of the [European Digital Identity Regulation] ensures the
User's rights to data portability. Data portability means that a User can
migrate to a different Wallet Solution. The User installs an instance of the new
Wallet Solution, and then wants to restore the PIDs and attestations in their
existing Wallet Unit to their new Wallet Unit. This should be possible with as
minimal an effort as possible, and independent of whether the User still has
access to their existing Wallet Unit.

This section introduces a Migration Object in each Wallet Unit. This object is a
list of PIDs and attestations contained in the Wallet Unit, together with the
information needed to request (re-)issuance of that PID or attestation. In
addition, the Migration Object also contains the transaction log kept by the
Wallet Unit, see [Section 6.6.3.13](#66313-wallet-unit-enables-the-user-to-report-suspicious-requests-by-a-relying-party-and-to-request-a-relying-party-to-erase-personal-data).
The Migration Object does not contain any private keys of PIDs or device-bound
attestations. In most security architectures for a Wallet Solution described in
[Section 4.5](#45-wscd-architecture-types), this is
impossible at least for PIDs, since the WSCA/WSCD that contains the PID private
keys does not allow their extraction under any circumstances. An exception may
be architectures in which PID private keys are managed in a remote HSM and the
migration is to a new Wallet Unit of the same Wallet Provider. However, in such
cases, restoring functionality of the PIDs in a new Wallet Unit does not
necessitate that private keys must be exported to another HSM. Rather, it
implies the User must be able to authenticate towards the existing HSM from the
new Wallet Unit, and be recognised as an existing User. For attestations bound
to a keystore (rather than a WSCA/WSCD), the properties of the keystore
determine if it's possible to export the attestation private keys to a location
of the User's choosing. Most keystores will note allow this.

The fact that the Migration Object does not contain private keys means that PIDs
and device-bound attestations cannot be backed up and restored from the object
in such a way that they are usable in a new Wallet Unit without involvement of
the PID Provider or Attestation Provider. Instead, the User must ask the
respective PID Provider(s) or Attestation Provider(s) to issue the PID(s) or
device-bound attestation(s) existing on the User's old Wallet Unit once again to
the new Wallet Unit. The only function of the Migration Object is to simplify
this process by listing the PIDs and attestations present in the existing Wallet
Unit, together with the information needed by the new Wallet Unit to start the
issuance process. For PIDs and device-bound attestations, the Migration Object
does not contain attribute values or attribute identifiers, as that data is
considered sensitive and is not useful anyway because of the limitations
explained above. Instead, the object contains a list of attestation types and
the related Attestation Providers.

For a non-device-bound attestation, there are no private keys stored in a
WSCA/WSCD or keystore and hence it is in principle possible to back up such an
attestation and restore it in a different Wallet Unit without involvement of the
Attestation Provider. For non-device-bound attestations, the Migration Object
therefore either contains the same data as for device-bound attestations, or it
contains all data including attribute identifiers.

The Migration Object is stored in such a way that its confidentiality is ensured
and that it can be used only by the User.

See [Topic 34](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2321-topic-34---migrate-to-a-different-wallet-solution)
for high-level requirements regarding migration.

The migration functionality of a Wallet Unit also enables backup and restore.
Backup and restore is needed in case the User has lost access to their current
Wallet Unit, for example in case of loss, theft, or breakdown. It is also needed
if the User wants to start using another Wallet Unit, for example because they
have bought a new device, need to factory-reset their existing device, or want
to migrate to another Wallet Solution. In all of these cases, the User wants to
restore the PIDs and attestations in their existing Wallet Unit on their new
Wallet Unit, with as minimal an effort as possible.

The [European Digital Identity Regulation] does not contain a requirement
mandating backup and restore functionality in the Wallet. However, Wallet
Providers will implement backup and restore functionality nevertheless,
because it will be expected by Users. In fact, the requirements in [Topic 34](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2321-topic-34---migrate-to-a-different-wallet-solution)
also ensure the possibility of backup and restore.

#### 6.5.5 Wallet Instance uninstallation

No trust relationships are required for Wallet Instance uninstallation; anybody
able to access the device of the User will be able to do this.

If the User uninstalls the Wallet Instance, the Wallet Instance tries to ensure
that the associated WSCA/WSCD and keystore(s) delete all sensitive data and
cryptographic keys related to the Wallet Unit, as well as all keys of PIDs and
device-bound attestations on the Wallet Unit. Note that in some cases this may
be a challenge, for instance if the WSCD is an external smart card and the User
does not present that card to the User device at the moment the User uninstalls
the Wallet Instance. Another example occurs when the WSCD or the keystore is a
remote HSM and the User device is offline at the moment the User uninstalls the
Wallet Instance. In such cases, the cryptographic keys will probably remain
present on the WSCD, even though they will never be used again. If needed, it is
up to the Wallet Provider to define how the Wallet Unit should handle such
situations. For example, an HSM manager could address such cases by deciding to
delete cryptographic keys in the HSM that are too old or haven't been used for
too long, while being aware of the risks in doing so.

If it supports the Digital Credentials API, see [Section 4.4.3](#443-remote-presentation-transaction-flows),
the Wallet Instance also discloses the fact that it is uninstalled to
the Digital Credentials API framework.
