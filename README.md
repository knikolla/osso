# sso

<samlp:AuthnRequest
     xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
     xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
     ID="identifier_1"
     Version="2.0"
     IssueInstant="2004-12-05T09:21:59Z"
     AssertionConsumerServiceIndex="1">
     <saml:Issuer>https://sp.example.com/SAML2</saml:Issuer>
     <samlp:NameIDPolicy
       AllowCreate="true"
       Format="urn:oasis:names:tc:SAML:2.0:nameid-format:transient"/>
</samlp:AuthnRequest>
