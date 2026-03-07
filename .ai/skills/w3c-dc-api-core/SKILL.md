---
name: "w3c-dc-api-core"
description: "Use when implementing the W3C Digital Credentials API for browser-based credential exchange. Covers: DigitalCredential interface, navigator.credentials.get() extensions, credential management integration, and permissions policy."
sections:
  - "Introduction"
  - "Model"
  - "Scope"
  - "The Digital Credentials API"
  - "Extensions to `CredentialRequestOptions` dictionary"
  - "The `DigitalCredentialRequestOptions` dictionary"
  - "The `DigitalCredentialGetRequest` dictionary"
  - "Extensions to `CredentialCreationOptions` dictionary"
  - "The `DigitalCredentialCreationOptions` dictionary"
  - "The `DigitalCredentialCreateRequest` dictionary"
  - "The `DigitalCredential` interface"
  - "Integration with Credential Management API"
  - "[[\\DiscoverFromExternalSource]](origin, options, sameOriginWithAncestors) internal method"
  - "[[\\Store]](credential, sameOriginWithAncestors) internal method"
  - "[[\\Create]](origin, options, sameOriginWithAncestors) internal method"
  - "[[\\type]] internal slot"
  - "[[\\discovery]] internal slot"
  - "User permission"
  - "Permissions Policy integration"
  - "Registry of protocols"
  - "General inclusion criteria"
  - "Change process"
---

<!-- ARF version: draft-2025 -->
<!-- Tokens: ~5675 -->

## Introduction
    
      This document defines an API enabling a website to request presentation
      and issuance of a [=digital credential=].
    
    
      The API design is agnostic to both credential [=digital
      credential/presentation requests|presentation=] [=digital
      credential/exchange protocols=], credential [=digital credential/issuance
      request|issuance=] [=digital credential/issuance protocols|protocols=]
      and credential formats. However, to promote interoperability this
      document includes a [[[#protocol-registry]]].
    
    
      The API is designed to support the following goals:
    
    
      - Keep the acts of [=digital credential/presentation
      requests|requesting=] and [=digital credential/issuance
      requests|issuing=] separate from the specific [=digital
      credential/exchange protocol=] and [=digital credential/issuance
      protocol=] respectively; thereby enabling the extensibility of such
      protocols and credential formats.
      
      - Require [=digital credential/presentation requests=] and [=digital
      credential/issuance requests=] to be unencrypted, enabling user-agent
      inspection for risk analysis.
      
      - Assume opaque (i.e., encrypted) [=digital credential/presentation
      responses=] and [=digital credential/issuance responses=], enabling
      issuers, verifiers, and holders to control where potentially sensitive
      personally identifiable information is exposed.
      
      - Require [=transient activation=] to perform [=digital
      credential/presentation requests=] or [=digital credential/issuance
      requests=], ensuring that sites cannot silently query for nor issue
      digital credentials, nor communicate with wallet providers, without the
      user's active participation and confirmation of each action.
      
      - Enable platform-provided credential selection UX when multiple wallet
      applications have credentials that match a [=digital
      credential/presentation request=].
      
      - Enable platform-provided wallet selection UX when multiple wallet
      applications support an [=digital credential/issuance request=].
      
      - Enable platforms to provide secure cross-device [=digital
      credential/presentation requests=] and [=digital credential/issuance
      requests=] with proximity checks.
      
    
    
      [=Digital credentials=] of many types can be presented and issued using
      this API. Examples of these
      types include:
    
    
      - a driving license, passport, or other identity card issued by a
      government institution
      
      - a travel authorization document issued by an embassy or consulate
      
      - a proof of employment issued by a public or private organization
      
      - a proof of education or professional training issued by an
      institution
      
      - and many other scenarios as described in Verifiable Credentials Use
      Cases

---

## Model
    
      The goal of the definitions in this section is to reuse or establish
      terminology that is common across a variety of digital credential formats
      and protocols. Discussions surrounding these definitions are active and
      the definitions are likely to change over the next several months.
    
    
      
        Digital credential
      
      
        A cryptographically signed digital document containing one or more
        [=claims=] made by an [=issuer=] about one or more [=subjects=].
        
          This specification is currently focused on digital credentials
          pertaining to people.
        
      
      
        Presentation request
      
      
        A presentation request is a request for a [=digital credential=]
        composed of [=digital credential/request data=] and a [=digital
        credential/exchange protocol=].
      
      
        request data
      
      
        A format that [=verifier=] software or a [=user agent=] uses, via an
        [=digital credential/exchange protocol=], to request a [=digital
        credential=] from a [=holder=].
      
      
        Presentation response
      
      
        A format that a [=holder's=] software, such as a digital wallet, uses,
        via an [=digital credential/exchange protocol=], to respond to a
        [=digital credential/presentation request=] by a [=verifier=].
      
      
        Issuance request
      
      
        An issuance request is a request to issue a [=digital credential=]
        composed of some [=digital credential/issuance request data=] and an
        [=digital credential/issuance protocol=].
      
      
        issuance request data
      
      
        A data structure that an [=issuer=] or a [=user agent=], via an
        [=digital credential/issuance protocol=], to request the issuance of a
        [=digital credential=] by an [=issuer=].
      
      
        Issuance response
      
      
        A format that [=holder=] uses, via an [=digital credential/issuance
        protocol=], to respond to an [=digital credential/issuance request=] by
        an [=issuer=].
      
      
        Exchange protocol
      
      
        A standardized protocol used for exchanging a [=digital credential=]
        between a [=holder=] and a [=verifier=]. A protocol is identified by a
        [=digital credential/protocol identifier=]. See section also
        [[[#protocol-registry]]].
      
      
        Protocol identifier
      
      
        A [=string=] composed of one or more [=ASCII lower alpha=] [=code
        points=], zero or more U+002D HYPHEN-MINUS [=code points=], and zero or
        more [=ASCII digit=] [=code points=] (in any order). For example,
        "123a-protocol", "abc", or simply "a".
      
      
        Issuance protocol
      
      
        A standardized protocol used for communication between an [=issuer=]
        and a [=holder=] during the issuance of a [=digital credential=]. The
        issuance protocol is identified by a [=digital credential/protocol
        identifier=]. See also section [[[#protocol-registry]]].

---

## Scope
    
      The following items are within the scope of this specification:
    
    
      - Requesting a [=digital credential=], including mechanisms for secure
      presentation.
      
      - Requesting issuance of a [=digital credential=].
      
      - Ensuring that when an API call is made, the website does not learn
      anything about the a holder's [=digital credentials=] or their software
      unless the [=user agent=] has previously received user consent.
      
      - Ensuring that any installed application software will not learn
      anything about a given [=request=] unless the [=holder=] explicitly
      consents to use that software.
      
    
    
      The following items are out of scope:
    
    
      - UI/UX considerations, with the exception of privacy considerations,
      which are addressed to ensure the protection of user data during the
      request process.

---

## The Digital Credentials API
    
      The Digital Credentials API leverages the [[[credential-management]]]
      specificaion, allowing [=user agents=] to mediate the [=digital
      credential/issuance=] and [=digital credential/presentation=] of
      [=digital credentials=].
    
    
      The API allows [=digital credential/presentation request|requesting=] a
      [=digital credential=] from the user agent, which in turn presents a
      [=credential chooser=] to the user, allowing them to select a [=digital
      credential=] that can fulfill the request. This is done by the website
      calling the `navigator.credentials.`{{CredentialsContainer/get()}}
      method, which runs the [=request a credential=] algorithm of
      [[[credential-management]]]. That algorithm then calls back into this
      specification's {{DigitalCredential}} interface's
      {{DigitalCredential/[[DiscoverFromExternalSource]](origin, options,
      sameOriginWithAncestors)}} internal method.
    
    
      Additionally, the API also allows [=digital credential/Issuance
      request|requesting issuance=] of a [=digital credential=], which
      initiates an mediated issuance flow between the user agent and/or a
      [=holder=]. This is done by calling the
      `navigator.credentials.`{{CredentialsContainer/create()}} method, which
      runs the [=create a credential=] algorithm of
      [[[credential-management]]]. That algorithm then calls back into this
      specification's {{DigitalCredential}} interface's
      {{Credential/[[Create]](origin,options, sameOriginWithAncestors)}}
      internal method.
    
    
      Please see [[[#credential-management-integration]]] for complete details
      of how to integrate with the [[[credential-management]]] specification.
    
    
      
        The following example shows how to request a digital credential using
        the Digital Credentials API. The entry point for the API is the
        `navigator.credentials.`{{CredentialsContainer/get()}} method, which is
        used to request a [=digital credential=] from the user agent. If the
        user agent supports [=digital credential/presentation
        requests|presentation=], it allows the user to select a digital
        credential through a [=credential chooser=]:
      
      ```
<button>Verify Identity</button>
        <script>
          const button = document.querySelector("button");
          button.addEventListener("click", async () => {
            try {
              const credential = await navigator.credentials.get({
                digital: {
                  requests: [{
                    protocol: "example-protocol",
                    data: { /* request data */ }
                  }]
                }
              });

              // Post it back to the server for decryption and verification
              const response = await fetch("/verify-credential", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json"
                },
                body: JSON.stringify(credential, null, 2)
              });

              // Check response
              if (!response.ok) {
                throw new Error("Failed to verify credential");
              }

              // Render the verification result
              displayVerificationResult(await response.json());

            } catch (error) {
              console.error("Error requesting digital credential:", error);
            }
          });
        </script>
```
    
    
      Simliarly, when a site needs to [=digital credential/issuance|issue=] a
      digital credential, the Digital Credentials API mediates the issuance of
      a digital credential between the site, the user agent, and the
      [=holder=].
    
    
      
        The following example shows how to request the issuance of a digital
        credential using the Digital Credentials API. To issue a digital
        credential, a site calls the
        `navigator.credentials.`{{CredentialsContainer/create()}} method,
        which, if the user agent supports issuance, would initiate the issuance
        flow:
      
      ```
<button>Request Digital Credential Issuance</button>
        <script>
          const button = document.querySelector("button");
          button.addEventListener("click", async () => {
            try {
              const credential = await navigator.credentials.create({
                digital: {
                  requests: [{
                    protocol: "example-issuance-protocol",
                    data: { /* issuance request data */ }
                  }]
                }
              });
            } catch (error) {
              console.error("Error issuing digital credential:", error);
            }
          });
        </script>
```
    
### Extensions to `CredentialRequestOptions` dictionary
    ```
partial dictionary CredentialRequestOptions {
      DigitalCredentialRequestOptions digital;
    };
```
#### The `digital` member
    
      The digital member
      allows for options to configure the request for a [=digital credential=].
    
### The `DigitalCredentialRequestOptions` dictionary
    ```
dictionary DigitalCredentialRequestOptions {
      required sequence<DigitalCredentialGetRequest> requests;
    };
```
#### The `requests` member
    
      The requests
      specify an [=digital credential/exchange protocol=] and [=digital
      credential/request data=], which the user agent MAY match against a
      holder's software, such as a digital wallet.
    
### The `DigitalCredentialGetRequest` dictionary
    
      The {{DigitalCredentialGetRequest}} dictionary represents a [=digital
      credential/presentation request=]. It is used to specify an [=digital
      credential/exchange protocol=] and some [=digital credential/request
      data=], which the user agent MAY match against software used by a holder,
      such as a digital wallet.
    
    ```
dictionary DigitalCredentialGetRequest {
        required DOMString protocol;
        required object data;
      };
```
#### The `protocol` member
    
      The protocol member
      denotes the [=digital credential/exchange protocol=].
    
    
      The {{DigitalCredentialCreateRequest/protocol}} member's value can be one
      of the well-defined protocol identifiers defined in
      [[[#protocol-registry]]] or a custom protocol identifier.
    
#### The `data` member
    
      The data member is
      the [=digital credential/request data=] to be handled by the holder's
      credential provider, such as a digital identity wallet.
    
### Extensions to `CredentialCreationOptions` dictionary
    ```
partial dictionary CredentialCreationOptions {
      DigitalCredentialCreationOptions digital;
    };
```
#### The `digital` member
    
      The digital member
      allows for options to configure the issuance of a [=digital credential=].
    
### The `DigitalCredentialCreationOptions` dictionary
    ```
dictionary DigitalCredentialCreationOptions {
      sequence<DigitalCredentialCreateRequest> requests;
    };
```
#### The `requests` member
    
      The requests
      specify an [=digital credential/issuance protocol=] and [=digital
      credential/request data=], which the user agent MAY forward to a
      [=holder=].
    
### The `DigitalCredentialCreateRequest` dictionary
    
      The {{DigitalCredentialCreateRequest}} dictionary represents an [=digital
      credential/issuance request=]. It is used to specify an [=digital
      credential/issuance protocol=] and some [=digital credential/request
      data=], to communicate the issuance request between the issuer and the
      holder.
    
    ```
dictionary DigitalCredentialCreateRequest {
      required DOMString protocol;
      required object data;
    };
```
#### The `protocol` member
    
      The protocol
      member denotes the [=digital credential/issuance protocol=].
    
    
      The {{DigitalCredentialCreateRequest/protocol}} member's value is be one
      of the well-defined keys defined in [[[#protocol-registry]]] or any other
      custom one.
    
#### The `data` member
    
      The data member
      is the [=digital credential/request data=] to be handled by the holder's
      credential provider, such as a digital identity wallet.
    
### The `DigitalCredential` interface
    
      The DigitalCredential interface represents a conceptual
      [=digital credential=].
    
    
      [=User mediation=] is always
      {{CredentialMediationRequirement/"required"}}. [=Request a
      credential|Requesting a DigitalCredential credential=] does not support
      {{CredentialMediationRequirement/"conditional"}},
      {{CredentialMediationRequirement/"optional"}}, or
      {{CredentialMediationRequirement/"silent"}} [=user mediation=]. If
      {{CredentialsContainer/get()}} is called with anything other than
      {{CredentialMediationRequirement/"required"}}, a {{TypeError}} will be
      thrown.
    
    ```
[Exposed=Window, SecureContext]
    interface DigitalCredential : Credential {
      [Default] object toJSON();
      readonly attribute DOMString protocol;
      [SameObject] readonly attribute object data;
      static boolean userAgentAllowsProtocol(DOMString protocol);
    };
```
    
      {{DigitalCredential}} instances are [=Credential/origin bound=].
    
#### The `protocol` member
    
      The protocol member is the
      [=digital credential/exchange protocol=] that was used to request the
      [=digital credential=], or the [=digital credential/issuance protocol=]
      that was used to issue the [=digital credential=].
    
#### The `data` member
    
      The data member is the
      credential's response data. It contains the subset of JSON-parseable
      object types.
    
#### The userAgentAllowsProtocol() method
    
      The {{DigitalCredential/userAgentAllowsProtocol()}} method allows digital
      credential [=verifiers=] to determine which [=digital credential/exchange
      protocols=] and [=digital credential/issuance protocols=] the user agent
      allows.
    
    
      This method does not convey [=digital credential/exchange protocol=] or
      [=digital credential/issuance protocol=] support in the underlying
      OS/platform.
    
    
      User agents MUST NOT vary the response value based on any information
      about availability of hardware, presence or configuration of software,
      wallets, credential providers, or digital credentials, or user
      configuration or preferences. If the response value varied, the user
      agent would introduce risks both of fingerprinting and of silently
      revealing other details about user behavior or configuration. The
      response value SHOULD vary only by user agent major version and indicate
      whether the browser supports distributing requests with that protocol to
      underlying platform or provider.
    
    
      When this method is invoked, the user agent MUST execute the following
      algorithm:
    
    
      - If |protocol| is not a [=digital credential/protocol identifier=],
      return `false`.
      
      - Return `true` if the user agent allows |protocol|, otherwise return
      `false`.

---

## Integration with Credential Management API
    
### [[\DiscoverFromExternalSource]](origin, options, sameOriginWithAncestors) internal method
    
      When invoked, the [[\DiscoverFromExternalSource]](origin, options,
      sameOriginWithAncestors) internal method MUST:
    
    
      - Let |global| be [=this=]'s [=relevant global object=].
      
      - Let |document| be |global|'s [=associated `Document`=].
      
      - If |document| is not a [=Document/fully active descendant of a
      top-level traversable with user attention=], [=exception/throw=]
      {{"NotAllowedError"}} {{DOMException}}.
      
      - If |window| does not have [=transient activation=],
      [=exception/throw=] {{"NotAllowedError"}} {{DOMException}}.
      
      - [=Consume user activation=] of |window|.
      
      - Let |requests| be |options|'s {{CredentialRequestOptions/digital}}'s
      {{DigitalCredentialRequestOptions/requests}} member.
      
      - If |requests| is empty, [=exception/throw=] a {{TypeError}}.
      
      - [=List/For each=] |request| of |requests|:
        
          - [=serialize a JavaScript value to a JSON string|Serialize=]
          |request| to a JSON string. [=exception/throw|Re-throw=] any
          [=exception=].
          
        
      
      - 
        
          Details of how to actually get the [=digital credential=] are
          forthcoming.
        
      
      - Return a {{DigitalCredential}}.
      
    
### [[\Store]](credential, sameOriginWithAncestors) internal method
    
      When invoked, the [[\Store]](credential, sameOriginWithAncestors)
      MUST call the default implementation of {{Credential}}'s
      {{Credential/[[Store]](credential, sameOriginWithAncestors)}} internal
      method with the same arguments.
    
### [[\Create]](origin, options, sameOriginWithAncestors) internal method
    
      When invoked, the [[\Create]](origin, options,
      sameOriginWithAncestors) internal method, if the user agent doesn't
      support issuance, call the default implementation of {{Credential}}'s
      {{Credential/[[Create]](origin,options, sameOriginWithAncestors)}}
      internal method with the same arguments. Otherwise:
    
    
      - Let |global| be [=this=]'s [=relevant global object=].
      
      - Let |document| be |global|'s [=associated `Document`=].
      
      - If |document| is not a [=Document/fully active descendant of a
      top-level traversable with user attention=], [=exception/throw=]
      {{"NotAllowedError"}} {{DOMException}}.
      
      - If |window| does not have [=transient activation=],
      [=exception/throw=] {{"NotAllowedError"}} {{DOMException}}.
      
      - [=Consume user activation=] of |window|.
      
      - Let |requests| be |options|'s {{CredentialCreationOptions/digital}}'s
      {{DigitalCredentialCreationOptions/requests}} member.
      
      - If |requests| is empty, [=exception/throw=] a {{TypeError}}.
      
      - [=List/For each=] |request| of |requests|:
        
          - [=serialize a JavaScript value to a JSON string|Serialize=]
          |request| to a JSON string. [=exception/throw|Re-throw=] any
          [=exception=].
          
        
      
      - 
        
          Details of how to actually issue the [=digital credential=] are
          forthcoming.
        
      
      - Return a newly constructed {{DigitalCredential}} with
      {{DigitalCredential/protocol}} initialized to the protocol that was used
      to issue this credential, and {{DigitalCredential/data}} initialized to
      an [=digital credential/issuance response=] defined by that [=digital
      credential/issuance protocol=].
      
    
### [[\type]] internal slot
    
      The {{DigitalCredential}} [=interface object=] has an internal slot named
      [[\type]]
      whose value is "digital".
    
### [[\discovery]] internal slot
    
      The {{DigitalCredential}} [=interface object=] has an internal slot named
      [[\discovery]]
      whose value is "remote".
    
    
### User permission
      
        The Digital Credential API is a [=powerful feature=] that
        requires [=express permission=] from an end-user. This requirement is
        normatively enforced when calling {{CredentialsContainer}}'s
        {{CredentialsContainer/get()}} method.

---

## Permissions Policy integration
      
        This specification defines a [=policy-controlled feature=] identified
        by the string "digital-credentials-get".
        Its [=policy-controlled feature/default allowlist=] is [=default
        allowlist/'self'=].

---

## Registry of protocols
    
      Initiating the registration a protocol is done by filing an
      issue in our GitHub repository.
    
    
      The following is the registry of [=digital credential/exchange
      protocols=] and [=digital credential/issuance protocols=] that are
      supported by this specification.
    
    
      It is expected that this registry will be become a [=W3C registry=] in
      the future.
    
### General inclusion criteria
    
      The below criteria are a work in progress and are likely to change as
      this document evolves.
    
    
      To be included in the registry, the [=digital credential/exchange
      protocol=]:
    
    
      - MUST be standardized at a consortium the W3C liaises with
      
      - MUST be defined in a specification which is freely and publicly
      available at the stable URL listed in the registry.
      
      - MUST define a representation, as either a [[WebIDL]] [=dictionary=]
      or a JSON object, of the [=digital credential/exchange protocol=] request
      structure (i.e., the [=dictionary=] which defines the semantics and
      validation of the {{DigitalCredentialGetRequest}}'s
      {{DigitalCredentialGetRequest/data}} member) and the [=digital
      credential/issuance protocol=] request structure (i.e., the
      [=dictionary=] which defines the semantics and validation of the
      {{DigitalCredentialCreateRequest}}'s
      {{DigitalCredentialCreateRequest/data}} member).
      
      - MUST define a representation, as either a [[WebIDL]] [=dictionary=]
      or a JSON object, of the [=digital credential/exchange protocol=]
      response structure (i.e., the [=dictionary=] which defines the semantics
      and validation of the {{DigitalCredential}}'s {{DigitalCredential/data}}
      member.
      
      - MUST define validation rules for members of the request and response
      structures.
      
      - MUST have undergone privacy review by the W3C's Privacy Working Group and
      [Federated Identity Working
      Group](https://www.w3.org/groups/wg/fedid/).
        
          Once an expression of registration is received via GitHub, the
          registry maintainers will organize the privacy review with the
          [Privacy Working
          Group](https://www.w3.org/groups/wg/privacy/) . Please see the [[[security-privacy-questionnaire]]] for
          the kind of questions that will be asked of the protocol you are
          registering.
        
      
      - MUST have undergone security review by the Security Interest Group.
      
      - MUST have implementation commitment from at least one browser engine,
      one credential provider/wallet, and one issuer or verifier (depending on
      the protocol type). Each component MUST be from independent
      organizations.
      
      - MUST have formally recorded consensus by the Federated Identity
      Working Group to be included in the registry.
      
    
#### Presentation-specific inclusion criteria
    
      To be included as a presentation protocol in the registry (used with
      `navigator.credentials.get`), the [=digital credential/exchange
      protocol=]:
    
    
      - MUST support response encryption.
      
      - MUST encrypt any response containing personally identifiable
      information (PII).
      
    
### Change process
    
      To add a new [=digital credential/exchange protocol=] to the registry, or
      to update an existing one:
    
    
      
        Define a [=digital credential/protocol identifier=].
      
      
        The [=digital credential/protocol identifier=] MUST be a unique string
        that is not already in use in the registry. The [=digital
        credential/protocol identifier=] MUST uniquely define the set of
        required parameters and/or behavior that a digital credential provider
        implementation needs to support to successfully handle the request. If
        the set of required parameters or behaviors is updated in a way which
        would require a digital credential provider to also require an update
        to remain functional, a new protocol identifier MUST be assigned and be
        added to the registry.
      
      
        Specify a protocol
        type.
      
      
        The protocol type is either "Presentation" for presentation protocols
        used with `navigator.credentials.get` or "Issuance" for issuance
        protocols used with `navigator.credentials.create`.
      
      
        Describe the
        protocol.
      
      
        The description MUST be a brief summary of the protocol's purpose and
        use case.
      
      
        Provide a link to the
        specification.
      
      
        The specification MUST be a stable URL that points to the authoritative
        source for the protocol, including validation rules.
      
    
    
      [=User agents=] MUST support the following [=digital credential/exchange
      protocols=]:
    
    
      
        Table of officially registered [=digital credential/exchange
        protocols=].
      
      
        
          
            [=digital credential/Protocol identifier=]
          
          
            [=registry/Type=]
          
          
            [=registry/Description=]
          
          
            [=registry/link|Specification=]
          
        
      
      
        
          
            Coming soon...
