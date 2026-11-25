# APIs and service account key

## Enable APIs

In Cloud Console (project selected) enable:

- Google Sheets API  
- Google Drive API  
- Google Gmail API *(optional — demo email only; see [07_gmail_api.md](07_gmail_api.md))*  

CLI:

```bash
gcloud services enable sheets.googleapis.com drive.googleapis.com
# optional demo mail:
# gcloud services enable gmail.googleapis.com
```

Wait 1–2 minutes if calls fail immediately after enable.

**Gmail + service account:** bare SA keys usually cannot send as a personal user. Beginners should use **user OAuth** or `gws auth login` for mail — details in [07_gmail_api.md](07_gmail_api.md).

## Create service account

1. IAM → Service accounts → Create  
2. Name e.g. `sheet-writer`  
3. Keys → Add key → JSON  
4. Save as:

```text
credentials/google-service-account.json
```

(gitignored)

Note `client_email` — you will share the sheet with this address.

## Security

- Never commit the JSON  
- Never paste `private_key` into chat/issues  
- Lab/demo keys can be rotated after the workshop  
