---
name: "oid4vp-credential-formats"
description: "Use when implementing credential-format-specific OpenID4VP behaviour. Covers: W3C VC format params and claims matching, ISO mdoc (ISO 18013/23220) Handover and SessionTranscript, IETF SD-JWT VC format identifier, presentation response structures, and transaction data per format."
sections:
  - "Appendix B. Credential Format Specific Parameters and Rules"
  - "B.1. W3C Verifiable Credentials"
  - "B.2. Mobile Documents or mdocs (ISO/IEC 18013 and ISO/IEC 23220 series)"
  - "B.3. IETF SD-JWT VC"
---

<!-- ARF version: 1.0-final-2025-07-09 -->
<!-- Tokens: ~14364(LARGE) -->

## Appendix B. Credential Format Specific Parameters and Rules
OpenID for Verifiable Presentations is Credential Format agnostic, i.e., it is designed to allow applications to request and receive Presentations in any Credential Format. This section defines a set of Credential Format specific parameters and rules for some of the known Credential Formats. For the Credential Formats that are not mentioned in this specification, other specifications or deployments can define their own set of Credential Format specific parameters.


### B.1. W3C Verifiable Credentials
The following sections define the Credential Format specific parameters and rules for W3C Verifiable Credentials compliant to the [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)] specification and for W3C Verifiable Presentations of such Credentials.
If require_cryptographic_holder_binding is set to true in the Credential Query, the Wallet MUST return a Verifiable Presentation of a Verifiable Credential. Otherwise, a Verifiable Credential without Holder Binding MUST be returned.


#### B.1.1. Parameters in the meta parameter in Credential Query
The following is a W3C Verifiable Credentials specific parameter in the meta parameter in a Credential Query as defined in [Section 6.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#credential_query):

            
type_values:
            REQUIRED. A non-empty array of string arrays. The value of each element in the type_values array is a non-empty array specifying the fully expanded types (IRIs) that the Verifier accepts in a Presentation, after applying the @context to the Verifiable Credential. If a type value in a Verifiable Credential is not defined in any @context, it remains unchanged, i.e., remains a relative IRI after JSON-LD processing. For this reason, JSON-LD processing MAY be skipped in such cases and the relative IRI is considered to be the fully expanded type, as applying the @context would not alter the value. Implementations MAY use alternative mechanisms to obtain the fully expanded types, as long as the results are equivalent to those produced by JSON-LD processing. Each of the top-level arrays specifies one alternative to match the fully expanded type values of the Verifiable Credential against. Each inner array specifies a set of fully expanded types that MUST be present in the fully expanded types in the type property of the Verifiable Credential, regardless of order or the presence of additional types.

          

The following is a non-normative example of type_values within a DCQL query:

```
"type_values":[
  [
      "https://www.w3.org/2018/credentials#VerifiableCredential",
      "https://example.org/examples#AlumniCredential",
      "https://example.org/examples#BachelorDegree"
  ],
  [
      "https://www.w3.org/2018/credentials#VerifiableCredential",
      "https://example.org/examples#UniversityDegreeCredential"
  ],
  [
      "IdentityCredential"
  ]
]
```

The following is a non-normative example of a W3C Verifiable Credential that would match the type_values DCQL query above (other claims omitted for readability):

```
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://www.w3.org/2018/credentials/examples/v1"
  ],
  "type": ["VerifiableCredential", "UniversityDegreeCredential"]
}
```

The following is another non-normative example of a W3C Verifiable Credential that would match the type_values DCQL query above (other claims omitted for readability):

```
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://www.w3.org/2018/credentials/examples/v1"
  ],
  "type": ["VerifiableCredential", "BachelorDegree", "AlumniCredential"]
}
```

The following is another non-normative example of a W3C Verifiable Credential that would match the type_values DCQL query above (other claims omitted for readability):

```
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1"
  ],
  "type": ["VerifiableCredential", "IdentityCredential"]
}
```


#### B.1.2. Claims Matching
The claims_path parameter in the Credential Query as defined in [Section 6.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#credential_query) is used to specify the claims that the Verifier wants to receive in the Presentation. When used in the context of W3C Verifiable Credentials, the claims_path parameter always matches on the root of Verifiable Credential (not the Verifiable Presentation). Examples are shown in the following subsections.


#### B.1.3. Formats and Examples


##### B.1.3.1. VC signed as a JWT, not using JSON-LD
This section illustrates the presentation of a Credential conformant to [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)] that is signed using JWS, and does not use JSON-LD.


###### B.1.3.1.1. Format Identifier and Cipher Suites
The Credential Format Identifier is jwt_vc_json to request a W3C Verifiable Credential compliant to the [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)] specification or a Verifiable Presentation of such a Credential.
Cipher suites should use algorithm names defined in [IANA JOSE Algorithms Registry](https://www.iana.org/assignments/jose/jose.xhtml#web-signature-encryption-algorithms).


###### B.1.3.1.2. Example Credential
The following is a non-normative example of the payload of a JWT-based W3C Verifiable Credential that will be used throughout this section:

```
{
  "iss": "https://example.gov/issuers/565049",
  "nbf": 1262304000,
  "jti": "http://example.gov/credentials/3732",
  "sub": "did:example:ebfeb1f712ebc6f1c276e12ec21",
  "vc": {
    "@context": [
      "https://www.w3.org/2018/credentials/v1",
      "https://www.w3.org/2018/credentials/examples/v1"
    ],
    "type": [
      "VerifiableCredential",
      "IDCredential"
    ],
    "credentialSubject": {
      "given_name": "Max",
      "family_name": "Mustermann",
      "birthdate": "1998-01-11",
      "address": {
        "street_address": "Sandanger 25",
        "locality": "Musterstadt",
        "postal_code": "123456",
        "country": "DE"
      }
    }
  }
}
```


###### B.1.3.1.3. Metadata
The vp_formats_supported parameter of the Verifier metadata or Wallet metadata MUST have the Credential Format Identifier as a key, and the value MUST be an object consisting of the following name/value pair:


                  alg_values: OPTIONAL. A non-empty array containing identifiers of cryptographic algorithms supported for a JWT-secured W3C Verifiable Credential or W3C Verifiable Presentation. If present, the alg JOSE header (as defined in [[RFC7515](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7515)]) of the presented Verifiable Credential or Verifiable Presentation MUST match one of the array values.

              
The following is a non-normative example of client_metadata request parameter value in a request to present an W3C Verifiable Presentation.

```
{
  "vp_formats_supported": {
    "jwt_vc_json": {
      "alg_values": ["ES256", "ES384"]
    }
  }
}
```


###### B.1.3.1.4. Presentation Request
The requirements regarding the Credential to be presented are conveyed in the dcql_query parameter.
The following is a non-normative example of the contents of this parameter:

```
{
  "credentials": [
    {
      "id": "example_jwt_vc",
      "format": "jwt_vc_json",
      "meta": {
        "type_values": [["IDCredential"]]
      },
      "claims": [
        {"path": ["credentialSubject", "family_name"]},
        {"path": ["credentialSubject", "given_name"]}
      ]
    }
  ]
}
```


###### B.1.3.1.5. Presentation Response
The following requirements apply to the nonce and aud claims of the Verifiable Presentation:

the nonce claim MUST be the value of nonce from the Authorization Request;

                the aud claim MUST be the value of the Client Identifier, except for requests over the DC API where it MUST be the Origin prefixed with origin:, as described in [Appendix A.4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api_response).

              
The following is a non-normative example of the VP Token provided in the response (shortened for presentation):

```
{
  "example_jwt_vc": ["eY...QMA"]
}
```

The following is a non-normative example of the payload of the Verifiable Presentation in the VP Token in the last example:

```
{
  "iss": "did:example:ebfeb1f712ebc6f1c276e12ec21",
  "jti": "urn:uuid:3978344f-8596-4c3a-a978-8fcaba3903c5",
  "aud": "x509_san_dns:client.example.org",
  "nbf": 1541493724,
  "iat": 1541493724,
  "exp": 1573029723,
  "nonce": "n-0S6_WzA2Mj",
  "vp": {
    "@context": [
      "https://www.w3.org/2018/credentials/v1"
    ],
    "type": [
      "VerifiablePresentation"
    ],
    "verifiableCredential": [
      "eyJhb...ssw5c"
    ]
  }
}
```


##### B.1.3.2. LDP VCs
This section illustrates presentation of a Credential conformant to [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)] that is secured using Data Integrity, using JSON-LD.


###### B.1.3.2.1. Format Identifier and Cipher Suites
The Credential Format Identifier is ldp_vc to request a W3C Verifiable Credential compliant to the [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)] specification or a Verifiable Presentation of such a Credential.
Cipher suites should use Data Integrity compatible securing mechanisms defined in [Verifiable Credential Extensions](https://www.w3.org/TR/vc-extensions/#securing-mechanisms).


###### B.1.3.2.2. Example Credential
The following is a non-normative example of the payload of a Verifiable Credential that will be used throughout this section:

```
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://www.w3.org/2018/credentials/examples/v1",
    "https://w3id.org/security/data-integrity/v2"
  ],
  "id": "https://example.com/credentials/1872",
  "type": [
    "VerifiableCredential",
    "IDCredential"
  ],
  "issuer": {
    "id": "did:example:issuer"
  },
  "issuanceDate": "2025-03-19T00:00:00Z",
  "credentialSubject": {
    "given_name": "Max",
    "family_name": "Mustermann",
    "birthdate": "1998-01-11",
    "address": {
      "street_address": "Sandanger 25",
      "locality": "Musterstadt",
      "postal_code": "123456",
      "country": "DE"
    }
  },
  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "eddsa-rdfc-2022",
    "created": "2025-03-19T15:30:15Z",
    "proofValue": "z5C5b...EtszK",
    "proofPurpose": "assertionMethod",
    "verificationMethod": "did:example:issuer#keys-1"
  }
}
```


###### B.1.3.2.3. Metadata
The vp_formats_supported parameter of the Verifier metadata or Wallet metadata MUST have the Credential Format Identifier as a key, and the value MUST be an object consisting of the following name/value pairs:


                  proof_type_values: OPTIONAL. A non-empty array containing identifiers of proof types supported for a Data Integrity secured W3C Verifiable Presentation or W3C Verifiable Credential. If present, the proof type parameter (as defined in [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)]) of the presented Verifiable Credential or Verifiable Presentation MUST match one of the array values.

                
                  cryptosuite_values: OPTIONAL. A non-empty array containing identifiers of crypto suites supported with one of the algorithms listed in proof_type_values for a Data Integrity secured W3C Verifiable Presentation or W3C Verifiable Credential. Note that cryptosuite_values MAY be used if one of the algorithms in proof_type_values supports multiple crypto suites. If present, the proof cryptosuite parameter (as defined in [[VC_DATA_INTEGRITY](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA_INTEGRITY)]) of the presented Verifiable Credential or Verifiable Presentation MUST match one of the array values.

              
The following is a non-normative example of client_metadata request parameter value in a request to present an W3C Verifiable Presentation.

```
{
  "vp_formats_supported": {
    "ldp_vc": {
      "proof_type_values": [
        "DataIntegrityProof",
        "Ed25519Signature2020"
      ],
      "cryptosuite_values": [
        "ecdsa-rdfc-2019",
        "ecdsa-sd-2023",
        "ecdsa-jcs-2019",
        "bbs-2023"
      ]
    }
  }
}
```


###### B.1.3.2.4. Presentation Request
The requirements regarding the Credential to be presented are conveyed in the dcql_query parameter.
The following is a non-normative example of the contents of this parameter:

```
{
  "credentials": [
    {
      "id": "example_ldp_vc",
      "format": "ldp_vc",
      "meta": {
        "type_values": [["IDCredential"]]
      },
      "claims": [
        {"path": ["credentialSubject", "family_name"]},
        {"path": ["credentialSubject", "given_name"]},
        {"path": ["credentialSubject", "birthdate"]},
        {"path": ["credentialSubject", "address", "street_address"]},
        {"path": ["credentialSubject", "address", "locality"]},
        {"path": ["credentialSubject", "address", "postal_code"]},
        {"path": ["credentialSubject", "address", "country"]}
      ]
    }
  ]
}
```


###### B.1.3.2.5. Presentation Response
The following requirements apply to the challenge and domain claims within the proof object in the Verifiable Presentation:

the challenge claim MUST be the value of nonce from the Authorization Request;

                the domain claim MUST be the value of the Client Identifier, except for requests over the DC API where it MUST be the Origin prefixed with origin:, as described in [Appendix A.4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api_response).

              
The following is a non-normative example of the Verifiable Presentation in the vp_token parameter:

```
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://w3id.org/security/data-integrity/v2"
  ],
  "type": [
    "VerifiablePresentation"
  ],
  "verifiableCredential": [
    {
      "@context": [
        "https://www.w3.org/2018/credentials/v1",
        "https://www.w3.org/2018/credentials/examples/v1",
        "https://w3id.org/security/data-integrity/v2"
      ],
      "id": "https://example.com/credentials/1872",
      "type": [
        "VerifiableCredential",
        "IDCredential"
      ],
      "issuer": {
        "id": "did:example:issuer"
      },
      "issuanceDate": "2025-03-19T00:00:00Z",
      "credentialSubject": {
        "given_name": "Max",
        "family_name": "Mustermann",
        "birthdate": "1998-01-11",
        "address": {
          "street_address": "Sandanger 25",
          "locality": "Musterstadt",
          "postal_code": "123456",
          "country": "DE"
        }
      },
      "proof": {
        "type": "DataIntegrityProof",
        "cryptosuite": "eddsa-rdfc-2022",
        "created": "2025-03-19T15:30:15Z",
        "proofValue": "z5C5b...EtszK",
        "proofPurpose": "assertionMethod",
        "verificationMethod": "did:example:issuer#keys-1"
      }
    }
  ],
  "id": "ebc6f1c2",
  "holder": "did:example:holder",
  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "eddsa-rdfc-2022",
    "created": "2025-04-04T10:12:15Z",
    "challenge": "n-0S6_WzA2Mj",
    "domain": "x509_san_dns:client.example.org",
    "proofValue": "z5s8c...AD3a9d",
    "proofPurpose": "authentication",
    "verificationMethod": "did:example:holder#key-1"
  }
}
```


### B.2. Mobile Documents or mdocs (ISO/IEC 18013 and ISO/IEC 23220 series)
ISO/IEC 18013-5:2021 [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)] defines a mobile driving license (mDL) Credential in the mobile document (mdoc) format. Although ISO/IEC 18013-5:2021 [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)] is specific to mobile driving licenses (mDLs), the Credential format can be utilized with any type of Credential (or mdoc document types). The ISO/IEC 23220 series has extracted components from ISO/IEC 18013-5:2021 [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)] that are common across document types to facilitate the profiling of the specification for other document types. The core data structures are shared between ISO/IEC 18013-5:2021 [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)], ISO/IEC 23220-2 [[ISO.23220-2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.23220-2)], ISO/IEC 23220-4 [[ISO.23220-4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.23220-4)] which are encoded in CBOR and secured using COSE_Sign1.
The Credential Format Identifier for Credentials in the mdoc format is mso_mdoc.


#### B.2.1. Transaction Data
It is RECOMMENDED that each transaction data type defines a data element (NameSpace, DataElementIdentifier, DataElementValue) to be used to return the processed transaction data. Additionally, it is RECOMMENDED that it specifies the processing rules, potentially including any hash function to be applied, and the expected resulting structure.
Some document types support some transaction data ([Section 8.4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#transaction_data)) to be protected using mdoc authentication, as part of the DeviceSigned data structure [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)]. In those cases, the specifications of these document types include which transaction data types are supported, and the issuer includes the relevant data elements in the KeyAuthorizations. If a Wallet receives a request with a transaction_data type whose data element is unauthorized, the Wallet MUST reject the request due to an unsupported transaction data type.


#### B.2.2. Metadata
The vp_formats_supported parameter of the Verifier metadata or Wallet metadata MUST have the Credential Format Identifier as a key, and the value MUST be an object consisting of the following name/value pairs:


              issuerauth_alg_values: OPTIONAL. A non-empty array containing cryptographic algorithm identifiers. The Credential MUST be considered to fulfill the requirement(s) expressed in this parameter if one of the following is true: 1) The value in the array matches the 'alg' value in the IssuerAuth COSE header. 2) The value in the array is a fully specified algorithm according to [[I-D.ietf-jose-fully-specified-algorithms](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-jose-fully-specified-algorithms)] and the combination of the alg value in the IssuerAuth COSE header and the curve used by the signing key of the COSE structure matches the combination of the algorithm and curve identified by the fully specified algorithm. As an example, if the IssuerAuth structure contains an alg header with value -7 (which stands for ECDSA with SHA-256 in [[IANA.COSE](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#IANA.COSE)]) and is signed by a P-256 key, then it matches an issuerauth_alg_values element of -7 and -9 (which stands for ECDSA using P-256 curve and SHA-256 in [[I-D.ietf-jose-fully-specified-algorithms](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-jose-fully-specified-algorithms)]).

            
              deviceauth_alg_values: OPTIONAL. A non-empty array containing cryptographic algorithm identifiers. The Credential MUST be considered to fulfill the requirement(s) expressed in this parameter if one of the following is true: 1) The value in the array matches the 'alg' value in the DeviceSignature or DeviceMac COSE header. 2) The value in the array is a fully-specified algorithm according to [[I-D.ietf-jose-fully-specified-algorithms](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-jose-fully-specified-algorithms)] and the combination of the alg value in the DeviceSignature COSE header and the curve used by the signing key of the COSE structure matches the combination of the algorithm and curve identified by the fully-specified algorithm. 3) The alg of the DeviceMac COSE header is HMAC 256/256 (as described in Section 9.1.3.5 of [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)]) and the curve of the device key (from Table 22 of [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)]) matches a value in the array using the identifiers defined in the following table:

          

            
Table 2:
Mapping of curves to alg identifiers used for the HMAC 256/256 case
            

              
                Algorithm Name
                Algorithm Value
              
            
            
              
                HMAC 256/256 using ECDH with Curve P-256
                -65537
              
              
                HMAC 256/256 using ECDH with Curve P-384
                -65538
              
              
                HMAC 256/256 using ECDH with Curve P-521
                -65539
              
              
                HMAC 256/256 using ECDH with X25519
                -65540
              
              
                HMAC 256/256 using ECDH with X448
                -65541
              
              
                HMAC 256/256 using ECDH with brainpoolP256r1
                -65542
              
              
                HMAC 256/256 using ECDH with brainpoolP320r1
                -65543
              
              
                HMAC 256/256 using ECDH with brainpoolP384r1
                -65544
              
              
                HMAC 256/256 using ECDH with brainpoolP512r1
                -65545
              
            
          
Note: These are specified in OpenID4VP only for private use in this parameter in this specification, and might be superseded by a future registration in IANA.
For clarity, the following is a couple of non-normative examples of the deviceauth_alg_values parameter
The example below indicates the verifier supports DeviceMac with HMAC 256/256, where the MAC key is established via ECDH using keys on the P-256 curve as per Section 9.1.3.5 of [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)].

```
{
  "deviceauth_alg_values": [ -65537 ]
}
```

The example below indicates the verifier supports DeviceMac with HMAC 256/256, where the MAC key is established via ECDH using keys on the P-256 curve as per Section 9.1.3.5 of [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)], and DeviceSignature using ECDSA with the P-256 curve.

```
{
  "deviceauth_alg_values": [ -65537, -9 ]
}
```

The following is a non-normative example of client_metadata request parameter value in a request to present an ISO/IEC 18013-5 mDOC.

```
{
  "vp_formats_supported": {
    "mso_mdoc": {
      "issuerauth_alg_values": [-9, -50],

      "deviceauth_alg_values": [-9, -50]
    }
  }
}
```


#### B.2.3. Parameter in the meta parameter in Credential Query
The following is an ISO mdoc specific parameter in the meta parameter in a Credential Query as defined in [Section 6.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#credential_query).

            
doctype_value:
            REQUIRED. String that specifies an allowed value for the
doctype of the requested Verifiable Credential. It MUST
be a valid doctype identifier as defined in [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)].

          


#### B.2.4. Parameter in the Claims Query
The following are ISO mdoc specific parameters to be used in a Claims Query as defined in [Section 6.3](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#claims_query).

            intent_to_retain
            OPTIONAL. A boolean that is equivalent to IntentToRetain variable defined in Section 8.3.2.1.2.1 of [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)].

          


#### B.2.5. Presentation Response
An example DCQL query using the mdoc format is shown in [Appendix D](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#more_dcql_query_examples). The following is a non-normative example for a VP Token in the response:

```
{
  "my_credential": ["<base64url-encoded DeviceResponse>"]
}
```

The VP Token contains the base64url-encoded DeviceResponse CBOR structure as defined in ISO/IEC 18013-5 [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)] or ISO/IEC 23220-4 [[ISO.23220-4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.23220-4)]. Essentially, the DeviceResponse CBOR structure contains a signature or MAC over the SessionTranscript CBOR structure including the OpenID4VP-specific Handover CBOR structure.


#### B.2.6. Handover and SessionTranscript Definitions


##### B.2.6.1. Invocation via Redirects
If the presentation request is invoked using redirects, the SessionTranscript CBOR structure as defined in Section 9.1.5.1 in [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)] MUST be used with the following changes:


                DeviceEngagementBytes MUST be null.

              
                EReaderKeyBytes MUST be null.

              
                Handover MUST be the OpenID4VPHandover CBOR structure as defined below.

            

```
OpenID4VPHandover = [
  "OpenID4VPHandover", ; A fixed identifier for this handover type
  OpenID4VPHandoverInfoHash ; A cryptographic hash of OpenID4VPHandoverInfo
]

; Contains the sha-256 hash of OpenID4VPHandoverInfoBytes
OpenID4VPHandoverInfoHash = bstr

; Contains the bytes of OpenID4VPHandoverInfo encoded as CBOR
OpenID4VPHandoverInfoBytes = bstr .cbor OpenID4VPHandoverInfo

OpenID4VPHandoverInfo = [
  clientId,
  nonce,
  jwkThumbprint,
  responseUri
] ; Array containing handover parameters

clientId = tstr

nonce = tstr

jwkThumbprint = bstr

responseUri = tstr
```

The OpenID4VPHandover structure has the following elements:

The first element MUST be the string OpenID4VPHandover. This serves as a unique identifier for the handover structure to prevent misinterpretation or confusion.

              The second element MUST be a Byte String which contains the sha-256 hash of the bytes of OpenID4VPHandoverInfo when encoded as CBOR.

              
                The OpenID4VPHandoverInfo has the following elements:

The first element MUST be the client_id request parameter. If applicable, this includes the Client Identifier Prefix.

                  The second element MUST be the value of the nonce request parameter.

                  If the response is encrypted, e.g., using direct_post.jwt, the third element MUST be the JWK SHA-256 Thumbprint as defined in [[RFC7638](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7638)], encoded as a Byte String, of the Verifier's public key used to encrypt the response. Otherwise, the third element MUST be null. See [Appendix B.2.6.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#session_transcript_dc_api) for an explanation of why this is important.

                  The fourth element MUST be either the redirect_uri or response_uri request parameter, depending on which is present, as determined by the Response Mode.

                

            
Unless otherwise stated, the values of client_id, nonce, redirect_uri, and response_uri request parameters referenced above MUST be obtained from the Authorization Request query parameters if the request is unsigned, or from the signed Request Object if the request is signed.
The following is a non-normative example of the input JWK for calculating the JWK Thumbprint in the context of OpenID4VPHandoverInfo:

```
{
  "kty": "EC",
  "crv": "P-256",
  "x": "DxiH5Q4Yx3UrukE2lWCErq8N8bqC9CHLLrAwLz5BmE0",
  "y": "XtLM4-3h5o3HUH0MHVJV0kyq0iBlrBwlh8qEDMZ4-Pc",
  "use": "enc",
  "alg": "ECDH-ES",
  "kid": "1"
}
```

The following is a non-normative example of the OpenID4VPHandoverInfo structure:

```
Hex:

847818783530395f73616e5f646e733a6578616d706c652e636f6d782b6578633767
426b786a7831726463397564527276654b7653734a4971383061766c58654c486847
7771744158204283ec927ae0f208daaa2d026a814f2b22dca52cf85ffa8f3f8626c6
bd669047781c68747470733a2f2f6578616d706c652e636f6d2f726573706f6e7365

CBOR diagnostic:

84                                 # array(4)
  78 18                            #   string(24)
    783530395f73616e5f646e733a6578 #     "x509_san_dns:ex"
    616d706c652e636f6d             #     "ample.com"
  78 2b                            #   string(43)
    6578633767426b786a783172646339 #     "exc7gBkxjx1rdc9"
    7564527276654b7653734a49713830 #     "udRrveKvSsJIq80"
    61766c58654c48684777717441     #     "avlXeLHhGwqtA"
  58 20                            #   bytes(32)
    4283ec927ae0f208daaa2d026a814f #     "B\x83ì\x92zàò\x08Úª-\x02j\x81O"
    2b22dca52cf85ffa8f3f8626c6bd66 #     "+"Ü¥,ø_ú\x8f?\x86&Æ½f"
    9047                           #     "\x90G"
  78 1c                            #   string(28)
    68747470733a2f2f6578616d706c65 #     "https://example"
    2e636f6d2f726573706f6e7365     #     ".com/response"
```

The following is a non-normative example of the OpenID4VPHandover structure:

```
Hex:

82714f70656e494434565048616e646f7665725820048bc053c00442af9b8eed494c
efdd9d95240d254b046b11b68013722aad38ac

CBOR diagnostic:

82                                 # array(2)
  71                               #   string(17)
    4f70656e494434565048616e646f76 #     "OpenID4VPHandov"
    6572                           #     "er"
  58 20                            #   bytes(32)
    048bc053c00442af9b8eed494cefdd #     "\x04\x8bÀSÀ\x04B¯\x9b\x8eíILïÝ"
    9d95240d254b046b11b68013722aad #     "\x9d\x95$\x0d%K\x04k\x11¶\x80\x13r*­"
    38ac                           #     "8¬"
```

The following is a non-normative example of the SessionTranscript structure:

```
Hex:

83f6f682714f70656e494434565048616e646f7665725820048bc053c00442af9b8e
ed494cefdd9d95240d254b046b11b68013722aad38ac

CBOR diagnostic:

83                                 # array(3)
  f6                               #   null
  f6                               #   null
  82                               #   array(2)
    71                             #     string(17)
      4f70656e494434565048616e646f #       "OpenID4VPHando"
      766572                       #       "ver"
    58 20                          #     bytes(32)
      048bc053c00442af9b8eed494cef #       "\x04\x8bÀSÀ\x04B¯\x9b\x8eíILï"
      dd9d95240d254b046b11b6801372 #       "Ý\x9d\x95$\x0d%K\x04k\x11¶\x80\x13r"
      2aad38ac                     #       "*­8¬"
```


##### B.2.6.2. Invocation via the Digital Credentials API
If the presentation request is invoked using the Digital Credentials API, the SessionTranscript CBOR structure as defined in Section 9.1.5.1 in [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#ISO.18013-5)] MUST be used with the following changes:


                DeviceEngagementBytes MUST be null.

              
                EReaderKeyBytes MUST be null.

              
                Handover MUST be the OpenID4VPDCAPIHandover CBOR structure as defined below.

            
Note: The following section contains a definition in Concise Data Definition Language (CDDL), a language used to define data structures - see [[RFC8610](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC8610)] for more details. bstr refers to Byte String, defined as major type 2 in CBOR and tstr refers to Text String, defined as major type 3 in CBOR (encoded in utf-8) as defined in section 3.1 of [[RFC8949](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC8949)].

```
OpenID4VPDCAPIHandover = [
  "OpenID4VPDCAPIHandover", ; A fixed identifier for this handover type
  OpenID4VPDCAPIHandoverInfoHash ; A cryptographic hash of OpenID4VPDCAPIHandoverInfo
]

; Contains the sha-256 hash of OpenID4VPDCAPIHandoverInfoBytes
OpenID4VPDCAPIHandoverInfoHash = bstr

; Contains the bytes of OpenID4VPDCAPIHandoverInfo encoded as CBOR
OpenID4VPDCAPIHandoverInfoBytes = bstr .cbor OpenID4VPDCAPIHandoverInfo

OpenID4VPDCAPIHandoverInfo = [
  origin,
  nonce,
  jwkThumbprint
] ; Array containing handover parameters

origin = tstr

nonce = tstr

jwkThumbprint = bstr
```

The OpenID4VPDCAPIHandover structure has the following elements:

The first element MUST be the string OpenID4VPDCAPIHandover. This serves as a unique identifier for the handover structure to prevent misinterpretation or confusion.

              The second element MUST be a Byte String which contains the sha-256 hash of the bytes of OpenID4VPDCAPIHandoverInfo when encoded as CBOR.

              
                The OpenID4VPDCAPIHandoverInfo has the following elements:

The first element MUST be the string representing the Origin of the request as described in [Appendix A.2](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api_request). It MUST NOT be prefixed with origin:.

                  The second element MUST be the value of the nonce request parameter.

                  For the Response Mode dc_api.jwt, the third element MUST be the JWK SHA-256 Thumbprint as defined in [[RFC7638](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7638)], encoded as a Byte String, of the Verifier's public key used to encrypt the response. If the Response Mode is dc_api, the third element MUST be null. For unsigned requests, including the JWK Thumbprint in the SessionTranscript allows the Verifier to detect whether the response was re-encrypted by a third party, potentially leading to the leakage of sensitive information. While this does not prevent such an attack, it makes it detectable and helps preserve the confidentiality of the response.

                

            
The following is a non-normative example of the input JWK for calculating the JWK Thumbprint in the context of OpenID4VPDCAPIHandoverInfo:

```
{
  "kty": "EC",
  "crv": "P-256",
  "x": "DxiH5Q4Yx3UrukE2lWCErq8N8bqC9CHLLrAwLz5BmE0",
  "y": "XtLM4-3h5o3HUH0MHVJV0kyq0iBlrBwlh8qEDMZ4-Pc",
  "use": "enc",
  "alg": "ECDH-ES",
  "kid": "1"
}
```

The following is a non-normative example of the OpenID4VPDCAPIHandoverInfo structure:

```
Hex:

837368747470733a2f2f6578616d706c652e636f6d782b6578633767426b786a7831
726463397564527276654b7653734a4971383061766c58654c486847777174415820
4283ec927ae0f208daaa2d026a814f2b22dca52cf85ffa8f3f8626c6bd669047

CBOR diagnostic:

83                                 # array(3)
  73                               #   string(19)
    68747470733a2f2f6578616d706c65 #     "https://example"
    2e636f6d                       #     ".com"
  78 2b                            #   string(43)
    6578633767426b786a783172646339 #     "exc7gBkxjx1rdc9"
    7564527276654b7653734a49713830 #     "udRrveKvSsJIq80"
    61766c58654c48684777717441     #     "avlXeLHhGwqtA"
  58 20                            #   bytes(32)
    4283ec927ae0f208daaa2d026a814f #     "B\x83ì\x92zàò\x08Úª-\x02j\x81O"
    2b22dca52cf85ffa8f3f8626c6bd66 #     "+"Ü¥,ø_ú\x8f?\x86&Æ½f"
    9047                           #     "\x90G"
```

The following is a non-normative example of the OpenID4VPDCAPIHandover structure:

```
Hex:

82764f70656e4944345650444341504948616e646f7665725820fbece366f4212f97
62c74cfdbf83b8c69e371d5d68cea09cb4c48ca6daab761a

CBOR diagnostic:

82                                 # array(2)
  76                               #   string(22)
    4f70656e4944345650444341504948 #     "OpenID4VPDCAPIH"
    616e646f766572                 #     "andover"
  58 20                            #   bytes(32)
    fbece366f4212f9762c74cfdbf83b8 #     "ûìãfô!/\x97bÇLý¿\x83¸"
    c69e371d5d68cea09cb4c48ca6daab #     "Æ\x9e7\x1d]hÎ\xa0\x9c´Ä\x8c¦Ú«"
    761a                           #     "v\x1a"
```

The following is a non-normative example of the SessionTranscript structure:

```
Hex:

83f6f682764f70656e4944345650444341504948616e646f7665725820fbece366f4
212f9762c74cfdbf83b8c69e371d5d68cea09cb4c48ca6daab761a

CBOR diagnostic:

83                                 # array(3)
  f6                               #   null
  f6                               #   null
  82                               #   array(2)
    76                             #     string(22)
      4f70656e49443456504443415049 #       "OpenID4VPDCAPI"
      48616e646f766572             #       "Handover"
    58 20                          #     bytes(32)
      fbece366f4212f9762c74cfdbf83 #       "ûìãfô!/\x97bÇLý¿\x83"
      b8c69e371d5d68cea09cb4c48ca6 #       "¸Æ\x9e7\x1d]hÎ\xa0\x9c´Ä\x8c¦"
      daab761a                     #       "Ú«v\x1a"
```


### B.3. IETF SD-JWT VC
This section defines how Credentials complying with [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)] can be presented to the Verifier using this specification.
If require_cryptographic_holder_binding is set to true in the Credential Query, the Wallet MUST return an SD-JWT [[I-D.ietf-oauth-selective-disclosure-jwt](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-selective-disclosure-jwt)] with a Key Binding JWT (SD-JWT+KB) as the Verifiable Presentation. SD-JWTs that do not support Holder Binding (i.e., do not have a cnf Claim) cannot be returned in this case.
If require_cryptographic_holder_binding is set to false, an SD-JWT without the Key Binding JWT MAY be returned.


#### B.3.1. Format Identifier
The Credential Format Identifier is dc+sd-jwt.


#### B.3.2. Example Credential
The following is a non-normative example of the unsecured payload of an IETF SD-JWT VC that will be used throughout this section:

```
{
  "vct": "https://credentials.example.com/identity_credential",
  "given_name": "John",
  "family_name": "Doe",
  "birthdate": "1940-01-01"
}
```

The following is a non-normative example of an IETF SD-JWT VC using the unsecured payload above, containing claims that are selectively disclosable.

```
{
  "_sd": [
    "3oUCnaKt7wqDKuyh-LgQozzfhgb8gO5Ni-RCWsWW2vA",
    "8z8z9X9jUtb99gjejCwFAGz4aqlHf-sCqQ6eM_qmpUQ",
    "Cxq4872UXXngGULT_kl8fdwVFkyK6AJfPZLy7L5_0kI",
    "TGf4oLbgwd5JQaHyKVQZU9UdGE0w5rtDsrZzfUaomLo",
    "jsu9yVulwQQlhFlM_3JlzMaSFzglhQG0DpfayQwLUK4",
    "sFcViHN-JG3eTUyBmU4fkwusy5I1SLBhe1jNvKxP5xM",
    "tiTngp9_jhC389UP8_k67MXqoSfiHq3iK6o9un4we_Y",
    "xsKkGJXD1-e3I9zj0YyKNv-lU5YqhsEAF9NhOr8xga4"
  ],
  "iss": "https://example.com/issuer",
  "iat": 1683000000,
  "exp": 1883000000,
  "vct": "https://credentials.example.com/identity_credential",
  "_sd_alg": "sha-256",
  "cnf": {
    "jwk": {
      "kty": "EC",
      "crv": "P-256",
      "x": "TCAER19Zvu3OHF4j4W4vfSVoHIP1ILilDls7vCeGemc",
      "y": "ZxjiWWbZMQGHVWKVQ4hbSIirsVfuecCE6t4jT9F2HZQ"
    }
  }
}
```

The following are disclosures belonging to the claims from the example above.
Claim given_name:

SHA-256 Hash: jsu9yVulwQQlhFlM_3JlzMaSFzglhQG0DpfayQwLUK4

            Disclosure:
              WyIyR0xDNDJzS1F2ZUNmR2ZyeU5STjl3IiwgImdpdmVuX25hbWUiLCAiSm9o
              biJd

            Contents:
["2GLC42sKQveCfGfryNRN9w", "given_name", "John"]

          
Claim family_name:

SHA-256 Hash: TGf4oLbgwd5JQaHyKVQZU9UdGE0w5rtDsrZzfUaomLo

            Disclosure:
              WyJlbHVWNU9nM2dTTklJOEVZbnN4QV9BIiwgImZhbWlseV9uYW1lIiwgIkRv
              ZSJd

            Contents:
["eluV5Og3gSNII8EYnsxA_A", "family_name", "Doe"]

          
Claim birthdate:

SHA-256 Hash: tiTngp9_jhC389UP8_k67MXqoSfiHq3iK6o9un4we_Y

            Disclosure:
              WyI2SWo3dE0tYTVpVlBHYm9TNXRtdlZBIiwgImJpcnRoZGF0ZSIsICIxOTQw
              LTAxLTAxIl0

            Contents:
["6Ij7tM-a5iVPGboS5tmvVA", "birthdate", "1940-01-01"]

          


#### B.3.3. Transaction Data
It is RECOMMENDED that each transaction data type defines a top-level claim parameter to be used in the Key Binding JWT to return the processed transaction data. Additionally, it is RECOMMENDED that it specifies the processing rules, potentially including any hash function to be applied, and the expected resulting structure.
The transaction data mechanism requires the use of an SD-JWT VC with Cryptographic Holder Binding. Wallets MUST reject requests with transaction data types that have the require_cryptographic_holder_binding parameter set to false.


##### B.3.3.1. A Profile of Transaction Data in SD-JWT VC
The following is one profile that can be included in a transaction data type specification:


                The transaction_data request parameter includes the following parameter, in addition to type and credential_ids from [Section 5.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#new_parameters):


                    transaction_data_hashes_alg: OPTIONAL. Non-empty array of strings each representing a hash algorithm identifier, one of which MUST be used to calculate hashes in transaction_data_hashes response parameter. The value of the identifier MUST be a hash algorithm value from the "Hash Name String" column in the IANA "Named Information Hash Algorithm" registry [[IANA.Hash.Algorithms](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#IANA.Hash.Algorithms)] or a value defined in another specification and/or profile of this specification. If this parameter is not present, a default value of sha-256 MUST be used. To promote interoperability, implementations MUST support the sha-256 hash algorithm.

                

              
                The Key Binding JWT in the response includes the following top-level parameters:


                    transaction_data_hashes: A non-empty array of strings where each element is a base64url-encoded hash. Each of these hashes is calculated using a hash function over the string received in the transaction_data request parameter (base64url decoding is not performed before hashing). Each hash value ensures the integrity of, and maps to, the respective transaction data object. If transaction_data_hashes_alg was specified in the request, the hash function MUST be one of its values. If transaction_data_hashes_alg was not specified in the request, the hash function MUST be sha-256.

                  
                    transaction_data_hashes_alg: REQUIRED when this parameter was present in the transaction_data request parameter. String representing the hash algorithm identifier used to calculate hashes in transaction_data_hashes response parameter.

                

            


#### B.3.4. Metadata
The vp_formats_supported parameter of the Verifier metadata or Wallet metadata MUST have the Credential Format Identifier as a key, and the value MUST be an object consisting of the following name/value pairs:


              sd-jwt_alg_values: OPTIONAL. A non-empty array containing fully-specified identifiers of cryptographic algorithms (as defined in [[I-D.ietf-jose-fully-specified-algorithms](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-jose-fully-specified-algorithms)]) supported for an Issuer-signed JWT of an SD-JWT.

            
              kb-jwt_alg_values: OPTIONAL. A non-empty array containing fully-specified identifiers of cryptographic algorithms (as defined in [[I-D.ietf-jose-fully-specified-algorithms](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-jose-fully-specified-algorithms)]) supported for a Key Binding JWT (KB-JWT).

          
The following is a non-normative example of client_metadata request parameter value in a request to present an IETF SD-JWT VC.

```
{
  "vp_formats_supported": {
    "dc+sd-jwt": {
      "sd-jwt_alg_values": ["ES256", "ES384"],
      "kb-jwt_alg_values": ["ES256", "ES384"]
    }
  }
}
```


#### B.3.5. Parameter in the meta parameter in Credential Query
The following is an SD-JWT VC specific parameter in the meta parameter in a Credential Query as defined in [Section 6.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#credential_query).

            
vct_values:
            REQUIRED. A non-empty array of strings that specifies allowed values for
the type of the requested Verifiable Credential. All elements in the array MUST
be valid type identifiers as defined in [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)]. The Wallet
MAY return Credentials that inherit from any of the specified types, following
the inheritance logic defined in [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)].

          


#### B.3.6. Presentation Response
A non-normative example DCQL query using the SD-JWT VC format is shown in [Section 7.4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dcql_query_example).
The respective response is shown in [Section 8.1.1](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#response_dcql_query).
Additional examples are shown in [Appendix D](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#more_dcql_query_examples).
The following requirements apply to the nonce and aud claims in the Key Binding JWT:

the nonce claim MUST be the value of nonce from the Authorization Request;

            the aud claim MUST be the value of the Client Identifier, except for requests over the DC API where it MUST be the Origin prefixed with origin:, as described in [Appendix A.4](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#dc_api_response).

          
The following is a non-normative example of the unsecured payload of the Key Binding JWT of a Verifiable Presentation.

```
{
  "nonce": "n-0S6_WzA2Mj",
  "aud": "x509_san_dns:client.example.org",
  "iat": 1709838604,
  "sd_hash": "Dy-RYwZfaaoC3inJbLslgPvMp09bH-clYP_3qbRqtW4",
  "transaction_data_hashes": [ "fOBUSQvo46yQO-wRwXBcGqvnbKIueISEL961_Sjd4do" ]
}
```


#### B.3.7. SD-JWT VCLD
SD-JWT VCLD (SD-JWT Verifiable Credentials with JSON-LD) extends the IETF SD-JWT VC [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)] Credential format and allows to incorporate existing data models that use Linked Data, e.g., W3C VCDM [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)], while enabling a consistent and uncomplicated approach to selective disclosure.
Information contained in SD-JWT VCLD Credentials can be processed using a JSON-LD [[JSON-LD](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#JSON-LD)] processor after the SD-JWT VC processing.
When IETF SD-JWT VC is mentioned in this specification, SD-JWT VCLD defined in this section MAY be used.


##### B.3.7.1. Format
SD-JWT VCLD Credentials are valid SD-JWT VCs and all requirements from [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)] apply. Additionally, the requirements listed in this section apply.
For compatibility with JWT processors, the following registered Claims from [[RFC7519](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#RFC7519)] and [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)] MUST be used instead of any respective counterpart properties from W3C VCDM or elsewhere:


                vct to represent the type of the Credential.

              
                exp and nbf to represent the validity period of SD-JWT VCLD (i.e., cryptographic signature).

              
                iss to represent the Credential Issuer.

              
                status to represent the information to obtain the status of the Credential.

            
IETF SD-JWT VC is extended with the following claim:


                ld: OPTIONAL. Contains a JSON-LD [[JSON-LD](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#JSON-LD)] object in compact form, e.g., [[VC_DATA](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#VC_DATA)].

            


##### B.3.7.2. Processing
The following outlines a suggested non-normative set of processing steps for SD-JWT VCLD:


###### B.3.7.2.1. Step 1: SD-JWT VC Processing

A receiver (holder or verifier) of an SD-JWT VCLD applies the processing rules outlined in Section 4 of [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-sd-jwt-vc)], including verifying signatures, validity periods, status information, etc.

                If the vct value is associated with any SD-JWT VC Type Metadata, schema validation of the entire SD-JWT VCLD is performed, including the nested ld claim.

                Additionally, trust framework rules are applied, such as ensuring the Credential Issuer is authorized to issue SD-JWT VCLDs for the specified vct value.

              


###### B.3.7.2.2. Step 2: Business Logic Processing

Once the SD-JWT VC is verified and trusted by the SD-JWT VC processor, and if the ld claim is present, the receiver extracts the JSON-LD object from the ld claim and uses this for the business logic object. If the ld claim is not present, the entire SD-JWT VC is considered to represent the business logic object.

                The business logic object is then passed on for further use case-specific processing and validation. The business logic assumes that all security-critical functions (e.g., signature verification, trusted issuer) have already been performed during the previous step. Additional schema validation is applied if provided in the ld claim, e.g., to support SHACL schemas. Note that while a vct claim is required, SD-JWT VC type metadata resolution and related schema validation is optional in certain cases.

              


##### B.3.7.3. Examples
The following is a non-normative example of an unsecured payload of an SD-JWT VCLD (i.e., before applying the modifications to enable selective disclosure and before adding validity claims).

```
{
  "vct": "https://credentials.example.com/example_credential",
  "ld": {
    "@context": [
      "https://www.w3.org/ns/credentials/v2",
      "https://w3id.org/citizenship/v3"
    ],
    "credentialSubject": {
      "givenName": "John",
      "familyName": "Doe",
      "birthDate": "1978-07-17"
    }
  }
}
```

The following payload would be used in the SD-JWT after encoding the payload above and enabling selective disclosure on the End-User specific claims within credentialSubject:

```
{
  "iss": "https://issuer.example.com",
  "iat": 1683000000,
  "exp": 1883000000,
  "vct": "https://credentials.example.com/example_credential",
  "ld": {
    "@context": [
      "https://www.w3.org/ns/credentials/v2",
      "https://w3id.org/citizenship/v3"
    ],
    "credentialSubject": {
      "_sd": [
        "6BJdQrO24ejTTMsFI-wGiJJmGrbseWc5IwCCp4NAJ0k",
        "NTDVsbVAwS9AnUVq-_YG_wv0yGD0bv2JstX-AmvN65I",
        "ts0pyPntLjD0_NcgNOI3hd_2WjbZw21p2LfqhOC0b-U"
      ]
    }
  },
  "_sd_alg": "sha-256",
  "cnf": {
    "jwk": {
      "kty": "EC",
      "crv": "P-256",
      "x": "TCAER19Zvu3OHF4j4W4vfSVoHIP1ILilDls7vCeGemc",
      "y": "ZxjiWWbZMQGHVWKVQ4hbSIirsVfuecCE6t4jT9F2HZQ"
    }
  }
}
```

Note: The decision which claims to make selectively disclosable is up to the Issuer of the Credential. Considerations can be found in Section 6 and Section 9.7 of [[I-D.ietf-oauth-selective-disclosure-jwt](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#I-D.ietf-oauth-selective-disclosure-jwt)].
