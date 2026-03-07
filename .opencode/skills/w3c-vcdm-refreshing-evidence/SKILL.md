---
name: "w3c-vcdm-refreshing-evidence"
description: "Use when implementing advanced credential semantics in W3C VCDM. Covers: refreshing, terms of use, and evidence."
sections:
  - "5.4 Refreshing"
  - "5.5 Terms of Use"
  - "5.6 Evidence"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~5134 -->

### 5.4 Refreshing
        

        
It is useful for systems to enable the manual or automatic refresh of an expired
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). For more information about validity periods for
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), see Section [A.7 Validity Periods](https://www.w3.org/TR/vc-data-model-2.0/#validity-periods).
This specification defines a `refreshService` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property), which
enables an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) to include a link to a refresh service.
        
        
The [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) can include the refresh service as an element inside the
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) if it is intended for either the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) or
the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) (or both), or inside the [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) if it
is intended for the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) only. In the latter case, this enables the
[holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to refresh the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) before creating a
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) to share with a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier). In the former
case, including the refresh service inside the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
enables either the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) or the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) to perform future
updates of the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential).
        
        
The refresh service is only expected to be used when either the
[credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) has expired or the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) does not publish
[credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) status information. [Issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) are advised not to put the
`refreshService` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) in a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
that does not contain public information or whose refresh service is not
protected in some way.
        

        
          refreshService
          
The value of the `refreshService` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) MUST be one or more
refresh services that provides enough information to the recipient's software
such that the recipient can refresh the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). Each
`refreshService` value MUST specify its `type`. The precise content of each
refresh service is determined by the specific `refreshService` [type](https://www.w3.org/TR/vc-data-model-2.0/#dfn-type)
definition.
          
        

        
        
    [Example 27](https://www.w3.org/TR/vc-data-model-2.0/#example-use-of-the-refreshservice-property-by-an-issuer): Use of the refreshService property by an issuer
   ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://w3id.org/age/v1"
  ],
  "type": ["VerifiableCredential", "AgeVerificationCredential"],
  "issuer": "did:key:z6MksFxi8wnHkNq4zgEskSZF45SuWQ4HndWSAVYRRGe9qDks",
  "validFrom": "2024-04-03T00:00:00.000Z",
  "validUntil": "2024-12-15T00:00:00.000Z",
  "name": "Age Verification Credential",
  "credentialSubject": {
    "overAge": 21
  },
  "refreshService": {
    "type": "VerifiableCredentialRefreshService2021",
    "url": "https://registration.provider.example/flows/reissue-age-token",
    "refreshToken": "z2BJYfNtmWRiouWhDrbDQmC2zicUPBxsPg"
  }
}
```
      

        
In the example above, the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) specifies an automatic
`refreshService` that can be used by POSTing the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to
the refresh service `url`. Note that this particular verifiable credential is
not intended to be shared with anyone except for the original issuer.
        

        Note: Non-authenticated credential refresh
Placing a `refreshService` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) in a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) so that it is available to [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) can
remove control and consent from the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) and allow the
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to be issued directly to the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier),
thereby bypassing the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders).

---

### 5.5 Terms of Use
        

        
Terms of use can be used by an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) or a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to
communicate the terms under which a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) was issued. The [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) places their terms
of use inside the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). The [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) places their
terms of use inside a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation). This specification defines
a `termsOfUse` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) for expressing terms of use
information.
        

        
The value of the `termsOfUse` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) might be used
to tell the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) any or all of the following, among other things:
        

        
          - 
the procedures or policies that were used in issuing the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), by providing, for example, a pointer to a public location
(to avoid "phone home" privacy issues) where these procedures or policies
can be found, or the name of the standard that defines them
          
          - 
the rules and policies of the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) that apply to the presentation
of this [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier), by providing,
for example, a pointer to a public location (to avoid "phone home" privacy
issues) where these rules or policies can be found
          
          - 
the identity of the entity under whose authority the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) issued
this particular [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
          
        

        
          termsOfUse
          
The value of the `termsOfUse` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) MUST specify one or
more terms of use policies under which the creator issued the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential)
or [presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation). If the recipient (a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) or
[verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)) is not willing to adhere to the specified terms of use, then
they do so on their own responsibility and might incur legal liability if they
violate the stated terms of use. Each `termsOfUse` value MUST specify
its [type](https://www.w3.org/TR/vc-data-model-2.0/#dfn-type), for example, `TrustFrameworkPolicy`, and MAY specify its
instance `id`. The precise contents of each term of use is determined
by the specific `termsOfUse` [type](https://www.w3.org/TR/vc-data-model-2.0/#dfn-type) definition.
          
        

        
        
    [Example 28](https://www.w3.org/TR/vc-data-model-2.0/#example-use-of-the-termsofuse-property-by-an-issuer): Use of the termsOfUse property by an issuer
   ```
{
  {
    "@context": [
      "https://www.w3.org/ns/credentials/v2",
      "https://www.w3.org/ns/credentials/undefined-terms/v2"
    ],
    "id": "urn:uuid:08e26d22-8dca-4558-9c14-6e7aa7275b9b",
    "type": [
      "VerifiableCredential",
      "VerifiableAttestation",
      "VerifiableTrustModel",
      "VerifiableAuthorisationForTrustChain"
    ],
    "issuer": "did:ebsi:zZeKyEJfUTGwajhNyNX928z",
    "validFrom": "2021-11-01T00:00:00Z",
    "validUntil": "2024-06-22T14:11:44Z",
    "credentialSubject": {
      "id": "did:ebsi:zvHWX359A3CvfJnCYaAiAde",
      "reservedAttributeId": "60ae46e4fe9adffe0bc83c5e5be825aafe6b5246676398cd1ac36b8999e088a8",
      "permissionFor": [{
        "schemaId": "https://api-test.ebsi.eu/trusted-schemas-registry/v3/schemas/zHgbyz9ajVuSProgyMhsiwpcp8g8aVLFRNARm51yyYZp6",
        "types": [
          "VerifiableCredential",
          "VerifiableAttestation",
          "WorkCertificate"
        ],
        "jurisdiction": "https://publications.europa.eu/resource/authority/atu/EUR"
      }]
    },
    "termsOfUse": {
      "type": "TrustFrameworkPolicy",
      "trustFramework": "Employment&Life",
      "policyId": "https://policy.example/policies/125",
      "legalBasis": "professional qualifications directive"
    },
    "credentialStatus": {
      "id": "https://api-test.ebsi.eu/trusted-issuers-registry/v5/issuers/did:ebsi:zvHWX359A3CvfJnCYaAiAde/attributes/60ae46e4fe9adffe0bc83c5e5be825aafe6b5246676398cd1ac36b8999e088a8",
      "type": "EbsiAccreditationEntry"
    },
    "credentialSchema": {
      "id": "https://api-test.ebsi.eu/trusted-schemas-registry/v3/schemas/zCSHSDwrkkd32eNjQsMCc1h8cnFaxyTXP5ByozyVQXZoH",
      "type": "JsonSchema"
    }
  }
}
```
      

        
In the example above, the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) is asserting that the legal basis
under which the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) has been issued is the
"professional qualifications directive" using the "Employment&Life" trust
framework, with a specific link to the policy.
        

        
This feature is expected to be used by government-issued [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to instruct digital wallets to limit their use to similar
government organizations in an attempt to protect citizens from unexpected use
of sensitive data. Similarly, some [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) issued by private
industry are expected to limit use to within departments inside the
organization, or during business hours. Implementers are urged to read more
about this evolving feature in the appropriate section of the Verifiable
Credentials Implementation Guidelines [[VC-IMP-GUIDE](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-imp-guide)] document.

---

### 5.6 Evidence
        

        
Evidence can be included by an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) to provide the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) with
additional supporting information in a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). This could be
used by the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) to establish the confidence with which it relies on the
claims in the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). For example, an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) could check
physical documentation provided by the [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) or perform a set of
background checks before issuing the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential). In certain scenarios, this
information is useful to the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) when determining the risk associated
with relying on a given [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential).
        

        
This specification defines the `evidence` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) for expressing evidence
information.
        

        
          evidence
          
If present, the value of the `evidence` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) MUST be either a single
object or a set of one or more objects. The following [properties](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) are defined
for every evidence object:
            
              id
              
The `id` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) is OPTIONAL. It MAY be used to provide a unique identifier
for the evidence object. If present, the normative guidance in Section
[4.4 Identifiers](https://www.w3.org/TR/vc-data-model-2.0/#identifiers) MUST be followed.
              
              type
              
The `type` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) is REQUIRED. It is used to express the type of evidence
information expressed by the object. The related normative guidance in Section
[4.5 Types](https://www.w3.org/TR/vc-data-model-2.0/#types) MUST be followed.
              
            
          
        

        Note: See Implementation Guide for strategies for providing evidence
For information about how attachments and references to [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) and
non-credential data might be supported by the specification, see Section
[5.3 Integrity of Related Resources](https://www.w3.org/TR/vc-data-model-2.0/#integrity-of-related-resources).
        

        
        
    [Example 29](https://www.w3.org/TR/vc-data-model-2.0/#example-example-of-evidence-supporting-a-skill-achievement-credential): Example of evidence supporting a skill achievement credential
   ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://purl.imsglobal.org/spec/ob/v3p0/context-3.0.3.json"
  ],
  "id": "http://1edtech.edu/credentials/3732",
  "type": [
    "VerifiableCredential",
    "OpenBadgeCredential"
  ],
  "issuer": {
    "id": "https://1edtech.edu/issuers/565049",
    "type": "Profile"
  },
  "credentialSubject": {
    "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
    "type": "AchievementSubject",
    "name": "Alice Smith",
    "activityEndDate": "2023-12-02T00:00:00Z",
    "activityStartDate": "2023-12-01T00:00:00Z",
    "awardedDate": "2024-01-01T00:00:00Z",
    "achievement": [{
      "id": "urn:uuid:d46e8ef1-c647-419b-be18-5e045d1c4e64",
      "type": ["Achievement"],
      "name": "Basic Barista Training",
      "criteria": {
        "narrative": "Team members are nominated for this badge by their supervisors, after passing the Basic Barista Training course."
      },
      "description": "This achievement certifies that the bearer is proficient in basic barista skills."
    }]
  },
  "evidence": [{
      // url to an externally hosted evidence file/artifact
      "id": "https://videos.example/training/alice-espresso.mp4",
      "type": ["Evidence"],
      "name": "Talk-aloud video of double espresso preparation",
      "description": "This is a talk-aloud video of Alice demonstrating preparation of a double espresso drink.",
      // digest hash of the mp4 video file
      "digestMultibase": "uELq9FnJ5YLa5iAszyJ518bXcnlc5P7xp1u-5uJRDYKvc"
    }
  ]
}
```
      
        
In the `evidence` example above, the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) is asserting that they have
video of the [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) of the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) demonstrating the achievement.
        

        Note: Evidence has a different purpose from securing mechanisms
The `evidence` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) provides information that is different from and
information to the securing mechanism used. The `evidence` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) is
used to express supporting information, such as documentary evidence, related to
the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). In contrast, the securing mechanism is used to
express machine-verifiable mathematical proofs related to the authenticity of
the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) and integrity of the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). For more
information about securing mechanisms, see Section [4.12 Securing Mechanisms](https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanisms).
