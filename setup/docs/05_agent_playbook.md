# Agent playbook — zero-config setup from a GitHub URL

User says something like:

> Here is the GitHub repo. Use this kit so I can control Google Sheets. Nothing is set up yet.

## Playbook

1. **Clone / open** repo root  
2. Run `python setup/scripts/check_environment.py`  
3. For each **required NO**:
   - Explain in one sentence  
   - Propose install command  
   - Wait for user OK before running invasive installs  
4. **Chrome**
   - If missing: ask user to install Chrome  
   - If present: OK  
5. **Playwright**
   - Ask: “Optional browser automation — install Playwright? (y/N)”  
   - Default **No** for short demos  
6. **gcloud**
   - If missing: install SDK guide  
   - Run login command; tell user **complete browser login**  
   - Re-check token  
7. **Cloud project + APIs**
   - User picks/creates project  
   - Enable Sheets + Drive  
8. **Service account JSON**
   - Guide console key download into `credentials/`  
9. **bootstrap.py**  
10. **smoke_test.py**  
11. Announce URL + “Tool 1 done → Tool 2 `control/`”  

## Phrases to use with the user

- “A browser window will open — please sign in and click Allow.”  
- “I will not ask for your password in this chat.”  
- “We can skip Tool 1 live demo if time is short; Tool 2 needs a ready `.env`.”  
