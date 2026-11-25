# Privacy policy (package)

Must **not** appear in the published repo:

- Real person names, emails, phones  
- Student / patient identifiers  
- Real school, hospital, company names  
- Service account private keys, `.env`  
- OAuth / Gmail access tokens (`GOOGLE_GMAIL_TOKEN`, gws export dumps)

Allowed: fictional roles, placeholder emails (`you@example.com`), generic Google product names.

## Demo email

- Real addresses may exist **only** in local `.env` (gitignored), for **self-test** or an explicit allow-list.  
- Do not commit `GMAIL_TO` / `GMAIL_FROM` with real values.  
- Do not BCC a class, mailing list, or third parties from workshop scripts.  
- Scripts default to **dry-run**; `--send` is opt-in and whitelist-enforced.  
- Placeholder domains (`example.com`, etc.) are rejected for real send.
