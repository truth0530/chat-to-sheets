# gcloud CLI authentication (browser)

This is the step beginners fear. **A browser window is normal.**

## Install gcloud

https://cloud.google.com/sdk/docs/install  
Then open a new terminal:

```bash
gcloud --version
```

## Login (copy-paste)

```bash
gcloud config set project YOUR_PROJECT_ID

# User login + Google Drive scopes (needed to create/share sheets)
gcloud auth login --enable-gdrive-access

# Optional but useful for some libraries
gcloud auth application-default login
```

### What you should see

1. Browser opens Google account chooser  
2. You approve access  
3. Terminal returns success  

### Verify

```bash
gcloud auth list
gcloud auth print-access-token
```

## Insufficient scopes

```text
Request had insufficient authentication scopes
```

Fix:

```bash
gcloud auth login --enable-gdrive-access --force
```

## Why not “service account only”?

Service accounts often have **Drive storage quota 0** and cannot create files.  
Pattern:

```text
Human account creates spreadsheet
  → share Editor to service account email
  → scripts write with SA JSON
```
