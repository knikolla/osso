# osso

Simple SAML 2.0 proxy written in Flask.

Creates a SAML assertion with the attributes for `eppn`, `givenName`, `sn`
and `mail`. The value of the asserted attributes is read from the respective
environment variables. 
