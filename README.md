# Vlogue Legal

Official privacy policy and support pages for the Vlogue iOS app.

- Privacy Policy: https://koachan-dev.github.io/vlogue-legal/privacy/
- Support: https://koachan-dev.github.io/vlogue-legal/support/

Terms of use follow Apple's standard End User License Agreement (linked from the app).

The pages are static HTML and CSS. They intentionally use no cookies, analytics,
advertising, external fonts, or client-side scripts.

## Validate locally

```bash
python3 -m unittest discover -s tests -v
```

Policy changes must remain consistent with the behavior of the released Vlogue app,
with `docs/privacy-policy.md` in the app repository, and with the data-handling
disclosures published in App Store Connect.

## Legal copy source and publication

- Service & Purchase Terms: https://koachan-dev.github.io/vlogue-legal/terms/
- Commercial Disclosure (Japan): https://koachan-dev.github.io/vlogue-legal/commerce/
- Public operator: Independent developer koakutsu (個人開発者 koakutsu).
- The seller's legal name, address and phone number are disclosed on request by email without delay, in sufficient time before a purchase decision. The operator must actually maintain that process; do not add personal details to this public repository.

The three legal pages are generated from the app repository's
`Vlogue/Resources/LegalDocuments.json`. To update, run from the app repository:

```bash
python3 scripts/sync_legal_documents.py --site /path/to/vlogue-legal
python3 scripts/sync_legal_documents.py --site /path/to/vlogue-legal --check
```

Review and test the generated pages before publishing. A push to this repository's
`main` branch deploys GitHub Pages. App Store metadata and the iOS binary require
separate updates; publishing this site does not update them.
