---
name: "arf-presentation-flows"
description: "Use when implementing presentation flows, OpenID4VP integration, verifier endpoints, or proximity flows. Covers same-device/cross-device remote presentation, BLE/NFC proximity, OID4VP profiling, DC API."
sections:
  - "4.4 Data presentation flows"
  - "4.4.1 Overview"
  - "4.4.2 Proximity presentation flows"
  - "4.4.3 Remote presentation transaction flows"
  - "5.6 Protocols for secure data exchange between Wallet Units and Relying Parties"
  - "5.6.1 Attestation presentation"
  - "5.6.2 Transactional data using [ISO/IEC 18013-5] and [OpenID4VP]"
---

<!-- ARF version: v2.8.0 -->
<!-- Tokens: ~4837 -->

### 4.4 Data presentation flows

#### 4.4.1 Overview

This section defines four distinct communication flows that can be used when a
Wallet Unit presents a PID or attestation to a Relying Party Instance:

- **Proximity Supervised Flow**: In this flow, the User and their User
Device are physically near the Relying Part Instance. PIDs and attestations
are exchanged using proximity technology (e.g., NFC, Bluetooth) between the
Wallet Unit and the Relying Party Instance. Both devices may be with or without
internet connectivity. A human representative of the Relying Party supervises
the process.
- **Proximity Unsupervised Flow**: This flow is like the supervised flow, but
the Wallet Unit presents attestations to a machine, without human supervision.
The interfaces and protocols used in this flow are the same as for the proximity
supervised flow, and are described in [Section 4.4.2](#442-proximity-presentation-flows).
- **Remote Same-Device Flow**: In this flow, the User utilises a web browser or
another application on their User device to access a Relying Party's a service.
If consuming the service requires the Relying Party to obtain specific
attributes from the User's Wallet Unit, the Relying Party sends a presentation
request to the Wallet Unit. As explained in [Section 4.4.3.2](#4432-same-device-remote-presentation-flows),
this request is managed by the web browser on the User's device, utilising a
solution like the [W3C Digital Credentials API].
- **Remote Cross-Device Flow**: In this flow, the User uses a web browser on a
device other than the User device on which their Wallet Unit is installed to
access the Relying Party's service. This other device could be for instance a
desktop, laptop, or another mobile device. If the Relying Party needs to send a
presentation request to the User's Wallet Unit, it presents this request to the
web browser on the other device. Again using the [W3C Digital Credentials API],
this web browser sets up a secure communication channel between the other device
and the User's device. [Section 4.4.3.3](#4433-cross-device-remote-presentation-flows)
explains this in more detail.

Specific use cases integrate one or more of these flows. Each of these flows is
described in more detail in one of the next sections.

#### 4.4.2 Proximity presentation flows

Figure 3 shows how attestation presentation works when the User and their User
Device are physically near the Relying Part Instance and do not have (or do not
want to use) an internet connection between them. In this case, the [ISO/IEC
18013-5] standard specifies how a communication channel is set up and how a
presentation request and the corresponding response are exchanged using
short-range communication technologies.

![Figure 3](media/Figure_3_Proximity_Flow.png)
*Figure 3: Proximity presentations*

An attribute presentation flow according to ISO/IEC 18013-5 begins when the User
opens the Wallet Instance and instructs it to display a QR code or present an
NFC tag. This QR code or NFC tag contains the information necessary to establish
an NFC, BLE, or Wi-Fi Aware connection. The Relying Party Instance scans the QR
code or the NFC tag and sets up a connection towards the Wallet Unit. The QR
code or NFC tag also contains the information necessary to create an
authenticated and encrypted secure channel on top of the NFC, BLE, or Wi-Fi
Aware connection between both entities.

For high-level requirements, see [Topic 24](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2314-topic-24---user-identification-in-proximity-scenarios).

Note that a Wallet Unit and a Relying Party do not have to use proximity
technologies if they are close together. They are still free to use a remote
flow according to [Section 4.4.3](#443-remote-presentation-transaction-flows).
However, there may be situations where either the Wallet Unit or the Relying
Party Instance does not have an internet connection. In such cases, Wallet Units
must be able to use a proximity presentation flow, if it is close to a Relying
Party Instance supporting the [ISO/IEC 18013-5] standard.

#### 4.4.3 Remote presentation transaction flows

##### 4.4.3.1 Introduction

Remote presentation transaction flows are use cases in which the Relying Party
Instance is remote from the User and the User device. The Relying Party Instance
requests data from the Wallet Unit over the internet, using a browser. These use
cases can be further distinguished as same-device flows, in which the browser is
running on the same device as the Wallet Unit, and cross-device flows, where the
browser is on a different device.

Remote presentation flows come with a number of challenges that are not present
for proximity flows:

1. **Secure Cross-Device Flows**: Cross-device flows are vulnerable to phishing
and relay attacks, necessitating enhanced security measures. Proximity checks,
managed by the operating system of the User device, can mitigate the risks
derived from these vulnerabilities by leveraging built-in security features to
verify the authenticity of interactions, ensuring they are both secure and
reliable.
1. **Wallet Unit Selection**: In remote flows, where interactions
do not originate from the Wallet Unit, Users may encounter difficulties in
selecting the appropriate Wallet Unit to fulfil a specific
presentation request, particularly when multiple Wallet Units are present on the
device. A unified interface provided by the web browser and the device operating
system can streamline this process, offering a seamless and intuitive User
experience.
1. **Invocation Mechanism**: Establishing a communication channel between the
Wallet Unit and the remote Relying Party Instance presents challenges due to
inconsistent invocation methods. One approach considered by standardisation
bodies involves using custom URI schemes, such as "mdoc://" or "openid4vp://".
In this approach, the device operating system would trigger the Wallet Unit when
the Relying Party Instance requests a connection via a custom URI. Another
approach is the use of domain-bound universal links (a.k.a. app links). However,
relying on custom URI schemes or universal links introduces variability in User
experiences across different browsers and operating systems, resulting in
operational inefficiencies and potential security risks. An interface provided by
the web browser and the device OS does not need custom URL schemes or universal links
for invoking a Wallet Unit.
1. **Clear Origin Verification**: Protecting against relay attacks requires precise
identification of the Relying Party Instance's origin. Including the origin
information, such as the website domain or app package name, within the
presentation request ensures the authenticity of the request and enhances trust
for both Wallet Units and Users.
1. **Session binding**: When presenting a PID or attestation to a remote Relying
Party Instance, Users have to switch contexts. Existing protocols may enable
attacks where the contexts are not bound to each other, resulting in session
hijacking. Using an interface provided by the web browser and the device OS
allows information about a session to be embedded in a presentation request. At
the same time, the browser and the operating system handle proper context
switching, preventing session hijacking.

The next sections describe how these challenges might be solved for both
same-device and cross-device remote presentation flows, by using the [W3C
Digital Credentials API]. This API is expected to establish a consistent method
for invoking Wallet Units, addressing these challenges.

The current version of the [W3C Digital Credentials API] extends the Credential Management
Level 1 API (the same API used by WebAuthn / Passkeys (see [Section 4.7](#47-possible-implementations-of-pseudonyms))
to allow websites to request an attestation. This is achieved by providing a
sequence of "presentation requests", where each presentation request includes an
"exchange protocol" and "request data". The format of the request data are
specific to the exchange protocol. The Digital Credentials API specifications
will include a registry of supported protocols. For more information see the
[Topic F: Digital Credentials API](./discussion-topics/f-digital-credential-api.md)
discussion paper.

However, the **[W3C Digital Credentials API]** is still under development and
has not yet been released as a **W3C Recommendation**. The use of this API by
Wallet Units and Relying Parties is optional, and custom URL schemes may be used
as well.
If a Wallet Unit implements a custom URL scheme, it will need to implement
mitigations for the challenges described in this section.

For the [W3C Digital Credentials API] to be mandated by this ARF in the future,
it will have to align with the following principles and expectations:

###### Alignment with EUDI Wallet Principles

The DC API implementations must meet critical expectations regarding **functionality,
neutrality, privacy,** and **governance**.

- **Expected Functionality**: It must support both Wallet Selection and
Invocation for attestation **presentation** and **issuance**, and it **shall**
support the protocols specified in the Implementing Acts for remote
presentation and issuance. It must also enable **Secure Cross-Device Flows**
to mitigate phishing and relay attacks.
- **Technological Neutrality**: The API **shall** preserve neutrality, avoiding
vendor-specific extensions. Implementations **shall not** restrict, block, or
discriminate against specific protocols, credential formats, or attestation
types. Any EUDI Wallet Solution must be able to use the API **without additional
vendor vetting**.
- **Privacy and Responsibility**: The API must not compromise User privacy. The
Wallet Unit and Relying Parties are responsible for **user consent**. The Wallet
Unit retains **full responsibility** over attestation management, ensuring the
operating system does not override or disrupt its security functions. The
attestation matching mechanism used by the operating system must be
**privacy-preserving**, only accessing the minimum necessary information without
disclosing attributes or values.
- **Availability**: It must prevent Denial-of-Service attacks against Wallet
Units by ensuring Attestation Providers or Relying Parties cannot send multiple
invalid requests.

###### Status and Cross-Device Protocol Requirements

Moreover, the API has not been implemented yet by all browsers and operating
systems, though it is currently a **W3C Working Draft** (latest from October
2025). For cross-device flows, the underlying **CTAP protocol** must also meet
specific requirements:

- **Transport Preferences**: Browsers and operating systems **shall** prefer
short-range CTAP transports (e.g., USB, NFC, or BLE) but **shall additionally
support** the **Hybrid transport** (which uses a tunnel server to link
the devices) and apply a policy-based selection with graceful fallback.
- **Alternative Tunnel Endpoints**: The CTAP Hybrid flow specification shall be
extended to support tunnel endpoints that are regulated under EU legislation and
supervised by EU authorities. Such endpoints SHALL be supported by corresponding
browsers and operating systems, and users SHOULD be able to select and configure
their preferred regulated endpoint.

##### 4.4.3.2 Same-device remote presentation flows

![Figure 4](media/Figure_4_Remote_Same-Device_Flow.png)
*Figure 4: Remote same-device presentations*

Compared to Figure 2, Figure 4 shows additional detail. In particular, it shows
the browser on the User device and the relevant interfaces of this browser:

- The **Remote same-device presentation** interface establishes communication
between the web browser and a remote Relying Party Instance, which may operate
on a server managed by the Relying Party. This interface may comply with the
[Digital Credentials API], which is a browser API that is currently being
standardised within the W3C.
- The **Wallet Instance-platform API** interface is a mechanism provided by the device's
operating system that may implement the Digital Credentials API mechanism at OS
level. There are however no current plans to standardise this interface on the
level of the API calls. These calls will be specified in the developer
documentation for the respective OS. One of the main properties of this API is
that a Wallet Unit receives reliable information regarding the origin of the
presentation request.

Obviously, the browser also has a User interface allowing the User to interact
with it. This interface will not be standardised in the context of the EUDI
Wallet ecosystem.

A remote same-device attribute presentation flow begins when the User accesses
the Relying Party's website using a browser on their device. The website may
provide an option for the User to present attributes from their Wallet Unit,
typically via a button or similar interface. When the User selects this option,
the browser may ask the User for permission to initiate the presentation flow. Upon
granting permission, the Relying Party Instance sends a presentation request
compliant with the OpenID4VP specification to the browser via the Digital
Credentials API. The browser, working in tandem with the device's operating
system (OS), forwards the request to the Wallet Unit using the Wallet Instance-platform API.
If the device hosts multiple Wallet Units, the browser and OS will determine
which Wallet Unit should handle the request. This decision may involve
consulting the User.

The selected Wallet Unit processes the presentation request and seeks the
User's approval before returning the requested attributes in an encrypted format
to the browser. The browser then forwards this encrypted response to the remote
Relying Party Instance.

Figure 4 also illustrates an inter-app attribute presentation flow. In this
scenario, an application on the User's device, such as a banking or shopping
app, interacts with the Wallet Unit over the Wallet Instance-platform API. This app acts as
the Relying Party Instance, possibly in cooperation with a remote server of the
entity that provisioned the app. The app can use the User attributes retrieved
from the Wallet Unit itself, for example for User authentication or to
automatically fill in data fields like User name and address. Alternatively, the
app can send these User attributes to the remote server. All requirements on
Relying Parties in this ARF, such as those regarding Relying Party registration
and authentication, User consent, and other aspects, are applicable in this use
case as well.

In this use case, the attribute presentation flow begins when the User opens the
app and initiates a request for attributes from the Wallet Unit via the
WI-platform API. Notably, this is the same API used in remote same-device
presentation flow involving a browser. The primary difference lies in the origin
information included in the presentation request, which may vary.

##### 4.4.3.3 Cross-device remote presentation flows

![Figure 5](media/Figure_5_Remote_Cross-Device_Flow.png)
Figure 5: Remote cross-device presentations

A remote cross-device attribute presentation flow begins when the User uses a
browser on a device different from their User device to visit the website of the
Relying Party. The website may offer the User the possibility to present
attributes from their Wallet Unit, for example by clicking a button. If the User
does so, the browser may ask the User for permission to initiate the
presentation flow. If the User allows this, the Relying Party Instance sends a
presentation request to the browser over the Digital Credentials API. The
browser then establishes a tunnel towards the User device, using the FIDO CTAP
2.2 hybrid flow, see section 11.5 of [CTAP]. Note that this flow is also used
for FIDO Passkeys. This is done as follows:

 1. The browser presents a QR code that includes information about the tunnel
 endpoint, as well as keys that will be used for establishing a secure channel
 over this tunnel.
 2. The User scans the QR code using the camera on the User device.
 3. The User device emits a BLE advertisement, which is received by the browser.
 The advertisement includes, in an encrypted form, information required for
 establishing the secure tunnel. This advertisement is used as a proximity
 check: the tunnel cannot be established if the User device and the device on
 which the browser runs are not close to each other.
 4. A tunnel is established between the two devices.

The browser then sends the OpenID4VP-compliant presentation request to the User
device. If there are multiple Wallet Instances present on the User device, the
device OS will determine to which of these the request will be forwarded,
possibly after consulting the User. The selected Wallet Unit will process the
presentation request and, after requesting approval from the User, will return
the requested attributes in encrypted format to the browser, using the
established tunnel. The browser will forward the response to the remote Relying
Party Instance.

Note that the Wallet Instance does not see any difference between the
cross-device flow and the same-device flow. In both cases, it receives an
OpenID4VP-compliant presentation request over the Wallet Instance-platform API described in
the previous section.

##### 4.4.3.4 Profiling the use of [OpenID4VP] in remote presentation flows

As mentioned above, for both same-device and cross-device remote presentation
flows, the messages used to request and present attestations comply with
[OpenID4VP]. The OpenID Foundation is standardising a profile for the W3C
Digital Credentials API, that will define how OpenID4VP will be used over this
API.

---

### 5.6 Protocols for secure data exchange between Wallet Units and Relying Parties

#### 5.6.1 Attestation presentation

##### 5.6.1.1 Introduction

Within the EUDI Wallet ecosystem, the protocol specified in ISO/IEC 18013-5 is
used for proximity attestation presentation flows, while the protocol specified
in OpenID4VP is used for remote attestation presentation flows. This section
briefly describes both of these protocols.

##### 5.6.1.2 Proximity attestation presentation using ISO/IEC 18013-5

ISO/IEC 18013-5 specifies the following aspects related to secure data exchange
for attestation presentations:

1. Message structures and transaction flows allowing a Wallet Unit and a Relying
Party to request and present attestations.
2. Proximity interface specifications, allowing a Wallet Unit and a Relying
Party to set up a communication channel using QR code or NFC, and to
subsequently communicate over BLE, NFC, or Wi-Fi Aware.
3. Security mechanisms ensuring
    - the confidentiality and authenticity of all data exchanged between a
    Wallet Unit and a Relying Party,
    - Relying Party authentication, see [Section 6.6.3.2](#6632-wallet-unit-authenticates-the-relying-party-instance).

As already explained in [Section 5.3.2](#532-isoiec-18013-5-and-isoiec-23220-2),
although ISO/IEC 18013-5 nominally specifies the mobile driving licence, all of
the above aspects are generic and can be used for any type of attestation.

Whereas ISO/IEC 18013-5 specifies proximity transaction flows only.
ISO/IEC 18013-7 specifies how to request and present ISO/IEC 18013-5-compliant
attestations in remote transaction flows.

##### 5.6.1.3 Remote attestation presentation using [OpenID4VP]

The [OpenID4VP] standard defines message structures, transaction flows, and an
HTTP-based interface specification for attestation presentations by Wallet Units
to Relying Parties. [OpenID4VP] also specifies security mechanisms ensuring:

- the confidentiality and authenticity of all data exchanged between a Wallet
Unit and a Relying Party,
- Relying Party authentication.

[OpenID4VP] is suitable only for remote presentation transaction flows.

[OpenID4VP] can be used for presenting attestations in different formats,
including especially the formats used within the EUDI Wallet ecosystem. Within
this ecosystem, [SD-JWT VC]-compliant attestations are always requested and
presented using [OpenID4VP], while [ISO/IEC 18013-5]-compliant attestations are
requested and presented using [OpenID4VP] in remote transaction flows.

Since [OpenID4VP] contains a number of options, the use of the profile for
'OpenID for Verifiable Presentations for IETF SD-JWT VC' specified in [HAIP] is
necessary to ensure interoperability between Wallet Units and Relying Parties.

#### 5.6.2 Transactional data using [ISO/IEC 18013-5] and [OpenID4VP]

In some use cases, a Relying Party must be able to include additional data in
the attestation presentation request. Primary examples include strong customer
authentication for payments, see [Section 2.6.4](#264-strong-user-authentication-for-electronic-payments),
and the creation of qualified electronic signatures, see [Section 2.4](#24-qualified-electronic-signatures).
In the case of strong customer authentication for payments, the Relying Party
sends payment information, such as the payment amount and the payee, to the
Wallet Unit. In the case of electronic signatures, the Relying Party may send (a
representation of) data to be signed to the Wallet Unit. In [Topic 20](./annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2313-topic-20---strong-user-authentication-for-electronic-payments),
such data is called transactional data.

The Wallet Unit will process the transactional data in a use-case specific way,
and, after consulting the User, will sign a (representation of the)
transactional data to authenticate it. The Wallet Unit will then return the
signed data in the presentation response, together with the presented
attributes, if any.

Both [ISO/IEC 18013-5] and [OpenID4VP] allow for sending, authenticating, and
returning transactional data. In both protocols, the presentation request can be
extended with use-case specific (proprietary) transactional data. The Wallet
Unit can subsequently sign this data by including it in the device binding
process, see [Section 6.6.3.8](#6638-relying-party-instance-verifies-device-binding).
Therefore, no extensions of the presentation response are necessary to return
the signed transactional data.
