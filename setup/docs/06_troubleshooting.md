# Tool 1 troubleshooting

| Symptom | Fix |
|---------|-----|
| API disabled | enable Sheets + Drive |
| insufficient scopes | `gcloud auth login --enable-gdrive-access --force` |
| storageQuotaExceeded on SA create | use bootstrap (user-owned sheet) |
| 403 on write | share SA as Editor |
| gcloud not found | install Cloud SDK |
| Chrome not found | install Chrome (login UX) |
| import googleapiclient fails | `pip install -r requirements.txt` |
| path with spaces breaks `source .env` | use `lib_env.py` (scripts already do) |
