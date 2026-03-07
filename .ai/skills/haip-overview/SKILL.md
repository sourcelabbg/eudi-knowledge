---
name: "haip-overview"
description: "Use when understanding the EUDI High Assurance Interoperability Profile for OpenID4VC. Covers: scope, terminology, overview of profiled specs, and general requirements for EUDI interoperability."
sections:
  - "1. Introduction"
  - "1.1. Target Audience/Usage"
  - "1.2. Errata Revisions"
  - "1.3. Requirements Notation and Conventions"
  - "2. Terminology"
  - "3. Scope"
  - "3.1. Assumptions"
  - "3.2. Additional scenarios"
  - "3.3. Standards Requirements"
  - "3.4. Out of Scope"
  - "4. OpenID for Verifiable Credential Issuance"
  - "4.1. Issuer Metadata"
  - "4.2. Credential Offer"
  - "4.3. Authorization Endpoint"
  - "4.4. Token Endpoint"
  - "4.5. Credential Endpoint"
---

<!-- ARF version: 1.0-2025-03-04 -->
<!-- Tokens: ~5417 -->

## 1. Introduction
This specification defines a set of requirements for the existing specifications to enable interoperability among Issuers, Wallets, and Verifiers of Credentials where a high level of security and privacy is required. This specification is an interoperability profile that can be used by implementations in various contexts, be it a certain industry or a certain regulatory environment. Note that while this specification is aimed at high assurance use-cases, it can also be used for lower assurance use-cases.
This specification aims to achieve a level of security and privacy that includes the following properties:

- Authenticity of claims: There is strong assurance that the claims within a Credential or Presentation are valid and bound to the correct Holder. This involves the policies and procedures used to collect and maintain the claims, the authentication of the Holder during issuance, and the protection of claim authenticity both at rest (in the wallet) and during presentation. The scope for this specification is: security of the issuance process, protection of issued credentials, and mechanisms for the Verifiers to access trustworthy information about the Issuer.

        - Holder authentication: There is strong assurance that the Credential is presented by its legitimate Holder in a given transaction. This involves proof of Holder binding, which can be validated through several methods. The scope for this specification includes secure presentation of key-bound credentials and supporting Claim-based Binding when built on top of this functionality.

      
Note: This specification defines the technical means by which holder authentication can be proven and claim authenticity can be protected using certain protocol and credential format features. Out of scope are concrete holder authentication mechanisms (which ensure only the holder can sign the presentation) and policies and procedures (as this is a technical interoperability profile and not a policy definition).
Note: This specification fulfils some, but not all, of the requirements to meet the "High" Level of Assurance (LoA) as defined in the eIDAS Regulation [[eIDAS2.0](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#eIDAS2.0)]. While this specification defines features intended for scenarios targeting a high level of security, these features must be combined with additional measures outside of the scope of HAIP to achieve LoA High compliance.
This specification contains profiles of other specifications. It refers to the specifications required for implementations to interoperate among each other and for the optionalities mentioned in the referenced specifications, defines the set of features to be mandatory to implement.
The specification uses OpenID for Verifiable Credential Issuance [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)] and OpenID for Verifiable Presentations [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)] as the base protocols for issuance and presentation of Credentials, respectively. The credential formats used are IETF SD-JWT VC as specified in [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#I-D.ietf-oauth-sd-jwt-vc)] and ISO mdoc [[ISO.18013-5](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#ISO.18013-5)]. Credentials in both IETF SD-JWT VC [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#I-D.ietf-oauth-sd-jwt-vc)] and ISO mdoc [[ISO.18013-5](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#ISO.18013-5)] formats can be issued following a single interaction with the Authorization Server.
A full list of the open standards used in this specification can be found in [Section 3.3](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#standards-requirements).


### 1.1. Target Audience/Usage
The target audience of this specification is implementers who require a high level of security and privacy for their solutions. A non-exhaustive list of the interested parties includes anyone implementing [eIDAS 2.0](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401183), [California Department of Motor Vehicles](https://www.dmv.ca.gov/portal/), [Open Wallet Foundation (OWF)](https://openwallet.foundation/), [IDunion](https://idunion.org/?lang=en), [GAIN](https://gainforum.org/), and [the Trusted Web project of the Japanese government](https://trustedweb.go.jp/en), but is expected to grow to include other jurisdictions and private sector companies.


### 1.2. Errata Revisions
The latest revision of this specification, incorporating any errata updates, is published at [openid4vc-high-assurance-interoperability-profile-1_0](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html). The text of the final specification as approved will always be available at [openid4vc-high-assurance-interoperability-profile-1_0-final](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-final.html). When referring to this specification from other documents, it is recommended to reference [openid4vc-high-assurance-interoperability-profile-1_0](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html).


### 1.3. Requirements Notation and Conventions
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [[RFC2119](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC2119)] [[RFC8174](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC8174)] when, and only when, they appear in all capitals, as shown here.

---

## 2. Terminology
This specification uses the terms "Holder", "Issuer", "Verifier", "Wallet", "Wallet Attestation", "Credential Type" and "Verifiable Credential" as defined in [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)] and [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)].
This specification also defines the following term. In the case where a term has a definition that differs, the definition below is authoritative.

        Ecosystem:
        A group of Issuers, Wallets and Verifiers that have a common set of rules by which they operate. The rules may be determined, for example, by a regulation, law or domain/sector.

---

## 3. Scope
This specification enables interoperable implementations of the following flows:

- Issuance of Credentials using OpenID for Verifiable Credential Issuance

        - Presentation of Credentials using OpenID for Verifiable Presentations with redirects

        - Presentation of Credentials using OpenID for Verifiable Presentations with the W3C Digital Credentials API

      
Implementations of this specification do not have to implement all the flows listed above, but they MUST be compliant to all the requirements for a flow they choose to implement, as well as the requirements in the non-flow specific sections.
For each flow, at least one of the Credential profiles defined in [Section 6](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#vc-profiles) MUST be supported:

- IETF SD-JWT VC

        - ISO mdocs

      
A parameter listed as optional to be implemented in a specification that is being profiled (e.g., OpenID4VCI, OpenID4VP, W3C Digital Credentials API, IETF SD-JWT VC, and ISO mdoc) remains optional unless stated otherwise in this specification.
The Profile of OpenID4VCI defines Wallet Attestation and Key Attestation.
The Profile of IETF SD-JWT VC defines the following aspects:

- Status management of the Credentials, including revocation

        - Cryptographic Key Binding

        - Issuer key resolution

        - Issuer identification (as prerequisite for trust management)

      
Note that when OpenID4VP is used, the Wallet and the Verifier can either be remote or in-person.


### 3.1. Assumptions
Assumptions made are the following:

- The Issuer uses the Wallet features defined in this specification (via Wallet invocation mechanism)

          - There are mechanisms in place for Verifiers to discover Wallets' and Issuers' capabilities

          - There are mechanisms in place for Wallets to discover Verifiers' capabilities

          - There are mechanisms in place for Issuers to discover Wallets' capabilities

        


### 3.2. Additional scenarios
Below is a non-exhaustive list of scenarios that can be realized with this specification:

- Combined Issuance of IETF SD-JWT VC and ISO mdoc

          - Both issuer-initiated and wallet-initiated issuance

          - Issuance and presentation of Credentials with and without cryptographic holder binding

        


### 3.3. Standards Requirements
The standards that are being profiled in this specification are:

- OpenID for Verifiable Credential Issuance [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)]

          - OpenID for Verifiable Presentations [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)]

          - W3C Digital Credentials API [[w3c.digital_credentials_api](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#w3c.digital_credentials_api)]

          - SD-JWT-based Verifiable Credentials (SD-JWT VC) [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#I-D.ietf-oauth-sd-jwt-vc)]

          - ISO/IEC 18013-5:2021 Personal identification - ISO-compliant driving licence Part 5: Mobile driving licence (mDL) application [[ISO.18013-5](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#ISO.18013-5)]

        
Note that these standards in turn build upon other underlying standards, and requirements in those underlying standards also need to be followed.


### 3.4. Out of Scope
The following items are out of scope for the current version of this specification, but might be added in future versions:

- Trust Management refers to authorization of an Issuer to issue certain types of credentials, authorization of the Wallet to be issued certain types of credentials, authorization of the Verifier to receive certain types of credentials. Although X.509 PKI is extensively utilized in this specification, the methods for establishing trust or obtaining root certificates are out of the scope of this specification.

          - Protocol for presentation of Verifiable Credentials for offline use-cases, e.g. over BLE.

---

## 4. OpenID for Verifiable Credential Issuance
When implementing OpenID for Verifiable Credential Issuance, both the Wallet and the Credential Issuer:

- MUST support the authorization code flow.

        - MUST support at least one of the following Credential Format Profiles defined in [Section 6](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#vc-profiles): IETF SD-JWT VC or ISO mdoc. Ecosystems SHOULD clearly indicate which of these formats, IETF SD-JWT VC, ISO mdoc, or both, are required to be supported.

        - MUST comply with the provisions of [[FAPI2_Security_Profile](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#FAPI2_Security_Profile)] that are applicable to this specification. This includes, but is not limited to using PKCE [[RFC7636](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC7636)] with `S256` as the code challenge method, Pushed Authorization Requests (PAR) [[RFC9126](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC9126)] (where applicable) and the `iss` value in the Authorization response [[RFC9207](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC9207)].

      
The following aspects of [[FAPI2_Security_Profile](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#FAPI2_Security_Profile)] are further profiled:

- Sender-constrained access token: MUST support DPoP as defined in [[RFC9449](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC9449)]. Note that this requires Wallets to be prepared to handle the `DPoP-Nonce` HTTP response header from the Credential Issuer's Nonce Endpoint, as well as from other applicable endpoints of the Credential Issuer and Authorization Server.

      
The following aspects of [[FAPI2_Security_Profile](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#FAPI2_Security_Profile)] do not apply to this specification:

- Client authentication: Wallet Attestation as defined in [Section 4.4.1](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#wallet-attestation) can be used.

        - Pushed Authorization Requests (PAR): Only required when using the Authorization Endpoint as defined in Section 5 of [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)].

        - Cryptography and secrets: [Section 7](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#crypto-suites) overrides the requirements in Section 5.4.1 clause 1.

      
Note that some optional parts of [[FAPI2_Security_Profile](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#FAPI2_Security_Profile)] are not applicable when using only OpenID for Verifiable Credential Issuance, e.g., MTLS or OpenID Connect.
Ecosystems SHOULD clearly indicate whether the Wallets and the Issuers need to support Issuer-initiated, Wallet-initiated Issuance or both, including how to send Credential Offer. If Issuer-initiated flows are supported, they MUST use the Credential Offer as defined in Section 4.1 of [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)].
Note that Ecosystems that aim for a stronger separation between the different Issuers and Wallets are expected to prefer the Issuer-initiated issuance flows and those with stronger integration into wallets (more wallet-centric Ecosystems) will likely prefer the Wallet-initiated Issuance.
If batch issuance is supported, the Wallet SHOULD use it rather than making consecutive requests for a single Credential of the same Credential Dataset. The Issuer MUST indicate whether batch issuance is supported by including or omitting the `batch_credential_issuance` metadata parameter. The Issuer’s decision may be influenced by various factors, including, but not limited to, trust framework requirements, regulatory constraints, applicable laws or internal policies.
Additional requirements for OpenID4VCI are defined in [Section 7](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#crypto-suites) and [Section 8](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#hash-algorithms).


### 4.1. Issuer Metadata
The Authorization Server MUST support metadata according to [[RFC8414](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC8414)].
The Credential Issuer MUST support metadata retrieval according to Section 12.2.2 of [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)].
The Credential Issuer metadata MUST include a scope for every Credential Configuration it supports.
When Ecosystem policies require Issuer Authentication to a higher level than possible with TLS alone, signed Credential Issuer Metadata as specified in Section 11.2.3 in [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)]
MUST be supported by both the Wallet and the Issuer. Key resolution to validate the signed Issuer
Metadata MUST be supported using the `x5c` JOSE header parameter as defined in [[RFC7515](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC7515)]. In this case, the X.509 certificate of the trust anchor MUST NOT be included in the `x5c` JOSE header of the signed request. The X.509 certificate signing the request MUST NOT be self-signed.
Wallets that render images provided by the Credential Issuer in its metadata defined in Section 12.2.4 of [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)] (e.g., the logo of a specific credential) have certain requirements. Such wallets MUST support both the SVG and PNG formats. They also MUST support images conveyed through both data URIs and HTTPS URLs.
If the Issuer supports Credential Configurations that require key binding, as indicated by the presence of `cryptographic_binding_methods_supported`, the `nonce_endpoint` MUST be present in the Credential Issuer Metadata.


### 4.2. Credential Offer

- The Grant Type `authorization_code` MUST be supported as defined in Section 4.1.1 in [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)]

          - For Grant Type `authorization_code`, the Issuer MUST include a scope value in order to allow the Wallet to identify the desired Credential Type. The Wallet MUST use that value in the `scope` Authorization parameter.

          - As a way to invoke the Wallet the custom URL scheme `haip-vci://` MAY be supported. Implementations MAY support other ways to invoke Wallets as agreed upon by trust frameworks/Ecosystems/jurisdictions, including but not limited to using other custom URL schemes or claimed "https" scheme URIs.

        
Note: The Authorization Code flow does not require a Credential Offer from the Issuer to the Wallet. However, it is included in the feature set to allow for Issuer initiated Credential issuance.
Both Issuer and Wallet MUST support Credential Offer in both same-device and cross-device flows.


### 4.3. Authorization Endpoint

- Wallets MUST authenticate themselves at the PAR endpoint using the same rules as defined in [Section 4.4](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#token-endpoint) for client authentication at the token endpoint.

          - MUST use the `scope` parameter to communicate Credential Type(s) to be issued. The scope value MUST map to a specific Credential Type. The scope value may be pre-agreed, obtained from the Credential Offer, or the Credential Issuer Metadata.

        


### 4.4. Token Endpoint

- Refresh tokens are RECOMMENDED to be supported for Credential refresh. For details, see Section 13.5 in [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)].

        
Note: Issuers SHOULD consider how long a refresh token is allowed to be used to refresh a credential, as opposed to starting the issuance flow from the beginning. For example, if the User is trying to refresh a Credential more than a year after its original issuance, the usage of the refresh tokens is NOT RECOMMENDED.


#### 4.4.1. Wallet Attestation
Wallets MUST use, and Issuers MUST require, an OAuth2 Client authentication mechanism at OAuth2 Endpoints that support client authentication (such as the PAR and Token Endpoints).
Ecosystems that desire wallet-issuer interoperability on the level of Wallet Attestations SHOULD require Wallets to support the authentication mechanism and Wallet Attestation format specified in Appendix E of [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)]. When doing so, they might need to define additional Ecosystem-specific claims contained in the attestation. Alternatively, Ecosystems MAY choose to rely on other Wallet Attestation formats.
Additional rules apply when using the format defined in Appendix E of [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)]:

- the public key certificate, and optionally a trust certificate chain excluding the trust anchor, used to validate the signature on the Wallet Attestation MUST be included in the `x5c` JOSE header of the Client Attestation JWT

            - Wallet Attestations MUST NOT be reused across different Issuers. They MUST NOT introduce a unique identifier specific to a single Wallet instance. The subject claim for the Wallet Attestation MUST be a value that is shared by all Wallet instances using the present type of wallet implementation. See section 15.4.4 of [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)] for details on the Wallet Attestation subject.

            - if applicable, the `client_id` value in the PAR request MUST be the string in the `sub` value in the client attestation JWT.

            - Wallets MUST perform client authentication with the Wallet Attestation at OAuth2 Endpoints that support client authentication.

          


### 4.5. Credential Endpoint


#### 4.5.1. Key Attestation
Wallets MUST support key attestations. Ecosystems that desire wallet-issuer interoperability on the level of key attestations SHOULD require Wallets to support the format specified in Appendix D of [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)], in combination with the following proof types:

- 
              `jwt` proof type using `key_attestation`

            - 
              `attestation` proof type

          
When using the format specified in Appendix D of [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)]:

- The public key used to validate the signature on the key attestation MUST be included in the `x5c` JOSE header of the key attestation

            - The X.509 certificate of the trust anchor MUST NOT be included in the `x5c` JOSE header of the key attestation.

            - The X.509 certificate signing the key attestation MUST NOT be self-signed.

            - The X.509 certificate profiles to be used are out of scope of this specification.

          
Alternatively, Ecosystems MAY choose to rely on other key attestation formats, meaning they would need to use a proof type other than `attestation`, define a new proof type, or expand the `jwt` proof type to support other key attestation formats.
If batch issuance is used and the Credential Issuer has indicated (via `cryptographic_binding_methods_supported` metadata parameter) that cryptographic holder binding is required, all public keys used in Credential Request SHOULD be attested within a single key attestation.
