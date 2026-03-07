---
name: "oid4vp-overview"
description: "Use when needing an overview of OpenID4VP, its terminology, or the difference between same-device and cross-device presentation flows. Covers: Verifier, Wallet, VP Token, vp_token response type, nonce, authorization request/response model."
---

<!-- ARF version: 1.0-final-2025-07-09 -->
<!-- Tokens: ~3583 -->

## 1. Introduction
This specification defines a mechanism on top of OAuth 2.0 [RFC6749] for requesting and delivering Presentations of Credentials. Credentials and Presentations can be of any format, including, but not limited to W3C Verifiable Credentials Data Model [VC_DATA], ISO mdoc [ISO.18013-5], and IETF SD-JWT VC [I-D.ietf-oauth-sd-jwt-vc].Â¶
OAuth 2.0 [RFC6749] is used as a base protocol as it provides the required rails to build a simple, secure, and developer-friendly Credential presentation layer on top of it. Moreover, implementers can, in a single interface, support Credential presentation and the issuance of Access Tokens for access to APIs based on Credentials in the Wallet. OpenID Connect [OpenID.Core] deployments can also extend their implementations using this specification with the ability to transport Credential Presentations.Â¶
This specification can also be combined with [SIOPv2], if implementers require OpenID Connect features, such as the issuance of Self-Issued ID Tokens [SIOPv2].Â¶
Additionally, it defines how to use OpenID4VP in conjunction with the Digital Credentials API (DC API) [W3C.Digital_Credentials_API]. See section Appendix A for all requirements applicable to implementers of OpenID4VP over the DC API. Except where it explicitly references other sections of this specification, that section is self-contained, and its implementers can ignore the rest of the specification.Â¶


### 1.1. Additional Authors

Tobias Looker (MATTR)Â¶

          Adam Lemmon (MATTR)Â¶

        


### 1.2. Errata revisions
The latest revision of this specification, incorporating any errata updates, is published at openid-4-verifiable-presentations-1_0. The text of the final specification as approved will always be available at openid-4-verifiable-presentations-1_0-final. When referring to this specification from other documents, it is recommended to reference openid-4-verifiable-presentations-1_0.Â¶


### 1.3. Requirements Notation and Conventions
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.Â¶

---

## 2. Terminology
This specification uses the terms "Access Token", "Authorization Request", "Authorization Response", "Client", "Client Authentication", "Client Identifier", "Grant Type", "Response Type", "Token Request" and "Token Response" defined by OAuth 2.0 [RFC6749], the terms "End-User" and "Entity" as defined by OpenID Connect Core [OpenID.Core], the terms "Request Object" and "Request URI" as defined by [RFC9101], the term "JSON Web Token (JWT)" defined by JSON Web Token (JWT) [RFC7519], the term "JOSE Header" defined by JSON Web Signature (JWS) [RFC7515], the term "JSON Web Encryption (JWE)" defined by [RFC7516], and the term "Response Mode" defined by OAuth 2.0 Multiple Response Type Encoding Practices [OAuth.Responses].Â¶
Base64url-encoded denotes the URL-safe base64 encoding without padding defined in Section 2 of [RFC7515].Â¶
This specification also defines the following terms. In the case where a term has a definition that differs, the definition below is authoritative.Â¶

        Biometrics-based Holder Binding:
        Ability of the Holder to prove legitimate possession of a Credential by demonstrating a certain biometric trait, such as a fingerprint or face. One example of a Credential with biometric Holder Binding is a mobile driving license [ISO.18013-5], which contains a portrait of the Holder.Â¶

        
Claims-based Holder Binding:
        Ability of the Holder to prove legitimate possession of a Credential by proving certain claims, e.g., name and date of birth, for example by presenting another Credential. Claims-based Holder Binding allows long-term, cross-device use of a Credential as it does not depend on cryptographic key material stored on a certain device. One example of such a Credential could be a diploma.Â¶

        
Credential:
        A set of one or more claims about a subject made by a Credential Issuer. In this specification, Credentials are usually Verifiable Credentials (defined below). Note that the definition of the term "Credential" in this specification is different from that in [OpenID.Core].Â¶

        
Credential Format Identifier:
        An identifier to denote a specific Credential Format in the context of this specification. This identifier implies the use of parameters specific to the respective Credential Format.Â¶

        
Credential Issuer:
        An entity that issues Credentials. Also called Issuer.Â¶

        
Cryptographic Holder Binding:
        Ability of the Holder to prove legitimate possession of a Credential by proving control over the same private key during the issuance and presentation. Mechanism might depend on the Credential Format. For example, in jwt_vc_json Credential Format, a Credential with Cryptographic Holder Binding contains a public key or a reference to a public key that matches to the private key controlled by the Holder.Â¶

        
Digital Credentials API:
        The Digital Credentials API (DC API) refers to the W3C Digital Credentials API [W3C.Digital_Credentials_API] on the Web Platform and its equivalent native APIs on App Platforms (such as Credential Manager on Android).Â¶

        
Holder:
        An entity that receives Credentials and has control over them to present them to the Verifiers as Presentations.Â¶

        
Holder Binding or Key Binding:
        Ability of the Holder to prove legitimate possession of a Credential.Â¶

        
Issuer-Holder-Verifier Model:
        A model for exchanging claims, where claims are issued in the form of Credentials independent of the process of presenting them as Presentations to the Verifiers. An issued Credential may be used multiple times.Â¶

        
Origin:
        An identifier for the calling website or native application, asserted by the web or app platform. A web origin is the combination of a scheme/protocol, host, and port, with port being omitted when it matches the default port of the scheme. An app platform may use a linked web origin, or use a platform-specific URI for the app origin. For example, the Verifier for the organization MyExampleOrg is served from https://verify.example.com. The web origin is https://verify.example.com with https being the scheme, verify.example.com being the host, and the port is not explicitly included as 443 is the default port for the protocol https. The native applications origin on some platforms will also be https://verify.example.com and on other platforms, may be platform:pkg-key-hash:Z4OFzVVSZrzTRa3eg79hUuHy12MVW0vzPDf4q4zaPs0.Â¶

        
Presentation:
        Data that is presented to a specific Verifier, derived from a Credential. In this specification, Presentations are usually Verifiable Presentations including Holder Binding (as defined below), but may also be Presentations without Holder Binding (discussed in Section 5.3).Â¶

        
VP Token:
        An artifact containing one or more Presentations returned as a response to an Authorization Request. The structure of VP Tokens is defined in Section 8.1.Â¶

        
Verifier:
        An entity that requests, receives, and validates Presentations. The Verifier is a specific case of an OAuth 2.0 Client, just like a Relying Party (RP) in [OpenID.Core].Â¶

        
Verifiable Credential (VC):
        An Issuer-signed Credential whose authenticity can be cryptographically verified. Can be of any format used in the Issuer-Holder-Verifier Model, including, but not limited to those defined in [VC_DATA] (VCDM), [ISO.18013-5] (mdoc), and [I-D.ietf-oauth-sd-jwt-vc] (SD-JWT VC).Â¶

        
Verifiable Presentation (VP):
        A Presentation with a cryptographic proof of Holder Binding. Can be of any format used in the Issuer-Holder-Verifier Model, including, but not limited to those defined in [VC_DATA] (VCDM), [ISO.18013-5] (mdoc), and [I-D.ietf-oauth-sd-jwt-vc] (SD-JWT VC).Â¶

        
Wallet:
        An entity used by the Holder to receive, store, present, and manage Credentials and key material. There is no single deployment model of a Wallet: Credentials and keys can both be stored/managed locally, or by using a remote self-hosted service, or a remote third-party service.Â¶

---

## 3. Overview
This specification defines a mechanism to request and present Credentials. The baseline of the protocol uses HTTPS messages and redirects as defined in OAuth 2.0. Additionally, the specification defines a separate mechanism where OpenID4VP messages are sent and received over the Digital Credentials API (DC API) [W3C.Digital_Credentials_API] instead of HTTPS messages and redirects.Â¶
As the primary extension, OpenID for Verifiable Presentations introduces the new response type vp_token, which allows a Verifier to request and receive Verifiable Presentations and Presentations in a container designated as VP Token. A VP Token contains one or more Verifiable Presentations and/or Presentations in the same or different Credential formats. Consequently, the result of an OpenID4VP interaction is one or more Verifiable Presentations and/or Presentations instead of an Access Token.Â¶
This specification supports any Credential format used in the Issuer-Holder-Verifier Model, including, but not limited to those defined in [VC_DATA] (VCDM), [ISO.18013-5] (mdoc), and [I-D.ietf-oauth-sd-jwt-vc] (SD-JWT VC). Credentials of multiple formats can be presented in the same transaction. The examples given in the main part of this specification use W3C Verifiable Credentials, while examples in other Credential formats are given in Appendix B.Â¶
OpenID for Verifiable Presentations supports scenarios where the Authorization Request is sent both when the Verifier is interacting with the End-User using the device that is the same or different from the device on which requested Credential(s) are stored.Â¶
This specification supports the response being sent using a redirect but also using an HTTP POST request. This enables the response to be sent across devices, or when the response size exceeds the redirect URL character size limitation.Â¶
In summary, OpenID for Verifiable Presentations is a framework that requires profiling
to achieve interoperability. Profiling means defining:Â¶

what optional features are used or mandatory to implement, e.g., response encryption;Â¶

        which values are permitted for parameters, e.g., Credential Format Identifiers;Â¶

        optionally, extensions for new features.Â¶

      


### 3.1. Same Device Flow
Figure 1 is a diagram of a flow where the End-User presents a Credential to a Verifier interacting with the End-User on the same device that the device the Wallet resides on.Â¶
The flow utilizes simple redirects to pass Authorization Request and Response between the Verifier and the Wallet. The Presentations are returned to the Verifier in the fragment part of the redirect URI, when Response Mode is fragment.Â¶
Note: The diagram does not illustrate all the optional features of this specification.Â¶


          
```
+--------------+   +--------------+                                    +--------------+
|   End-User   |   |   Verifier   |                                    |    Wallet    |
+--------------+   +--------------+                                    +--------------+
        |                 |                                                   |
        |    Interacts    |                                                   |
        |---------------->|                                                   |
        |                 |  (1) Authorization Request                        |
        |                 |  (DCQL query)                                     |
        |                 |-------------------------------------------------->|
        |                 |                                                   |
        |                 |                                                   |
        |   End-User Authentication / Consent                                 |
        |                 |                                                   |
        |                 |  (2)   Authorization Response                     |
        |                 |  (VP Token with Presentation(s))                  |
        |                 |<--------------------------------------------------|

```

Figure 1:
Same Device Flow
          

(1) The Verifier sends an Authorization Request to the Wallet. It contains a Digital Credentials Query Language (DCQL, see Section 6) query that describes the requirements of the Credential(s) that the Verifier is requesting to be presented. Such requirements could include what type of Credential(s), in what format(s), which individual Claims within those Credential(s) (Selective Disclosure), etc. The Wallet processes the Authorization Request and determines what Credentials are available matching the Verifier's request. The Wallet also authenticates the End-User and gathers consent to present the requested Credentials.Â¶
(2) The Wallet prepares the Presentation(s) of the Credential(s) that the End-User has consented to. It then sends to the Verifier an Authorization Response where the Presentation(s) are contained in the vp_token parameter.Â¶


### 3.2. Cross Device Flow
Figure 2 is a diagram of a flow where the End-User presents a Credential to a Verifier interacting with the End-User on a different device as the device the Wallet resides on.Â¶
In this flow, the Verifier prepares an Authorization Request and renders it as a QR Code. The End-User then uses the Wallet to scan the QR Code. The Presentations are sent to the Verifier in a direct HTTP POST request to a URL controlled by the Verifier. The flow uses the Response Type vp_token in conjunction with the Response Mode direct_post, both defined in this specification. In order to keep the size of the QR Code small and be able to sign and optionally encrypt the Request Object, the actual Authorization Request contains only the Client Identifier and Request URI (as required by [RFC9101]), which the Wallet uses to retrieve the actual Authorization Request data.Â¶
Note: The diagram illustrates neither all parameters nor all optional features of this specification.Â¶
Note: The usage of the Request URI as defined in [RFC9101] does not depend on any other choices made in the protocol extensibility points, i.e., it can be used in the Same Device Flow, too.Â¶


          
```
+--------------+   +--------------+                                    +--------------+
|   End-User   |   |   Verifier   |                                    |    Wallet    |
|              |   |  (device A)  |                                    |  (device B)  |
+--------------+   +--------------+                                    +--------------+
        |                 |                                                   |
        |    Interacts    |                                                   |
        |---------------->|                                                   |
        |                 |  (1) Authorization Request                        |
        |                 |      (Request URI)                                |
        |                 |-------------------------------------------------->|
        |                 |                                                   |
        |                 |  (2) Request the Request Object                   |
        |                 |<--------------------------------------------------|
        |                 |                                                   |
        |                 |  (2.5) Respond with the Request Object            |
        |                 |      (DCQL query)                                 |
        |                 |-------------------------------------------------->|
        |                 |                                                   |
        |   End-User Authentication / Consent                                 |
        |                 |                                                   |
        |                 |  (3)   Authorization Response as HTTP POST        |
        |                 |  (VP Token with Presentation(s))                  |
        |                 |<--------------------------------------------------|

```

Figure 2:
Cross Device Flow
          

(1) The Verifier sends to the Wallet an Authorization Request that contains a Request URI from where to obtain the Request Object containing Authorization Request parameters.Â¶
(2) The Wallet sends an HTTP GET request to the Request URI to retrieve the Request Object.Â¶
(2.5) The HTTP GET response returns the Request Object containing Authorization Request parameters. It contains a DCQL query that describes the requirements of the Credential(s) that the Verifier is requesting to be presented. Such requirements could include what type of Credential(s), in what format(s), which individual Claims within those Credential(s) (Selective Disclosure), etc. The Wallet processes the Request Object and determines what Credentials are available matching the Verifier's request. The Wallet also authenticates the End-User and gathers their consent to present the requested Credentials.Â¶
(3) The Wallet prepares the Presentation(s) of the Credential(s) that the End-User has consented to. It then sends to the Verifier an Authorization Response where the Presentation(s) are contained in the vp_token parameter.Â¶
