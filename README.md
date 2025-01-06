# GoogleDriveFolderMerger
A python tool to merge files in two folders, even if intermediate folders are owned by others

## Technology used:
- Python3
- Google Drive API (Python)
- Default python libraries (json, os, re)

## Description

<p>
  This tool was written to fix a problem caused by the shutdown of organisational Google Drive accounts.
  Over time, there can be files and folders owned by multiple of your accounts, nested within each other. 
</p>
<p>
  However, on account shutdown / use of Takeout, I encountered a situation where the files from each account
  were separated into two folders within my personal account. For example: 
</p>

```
Archives
├── orgfile1
└── folder
    ├── orgfile2
    └── personalfile2
```
Becomes two folders, both owned by the personal account:
```
Archives (this contains files owned by org account)
├── orgfile1
└── folder
    └── orgfile2
Archives (this contains files owned by personal account)
└── folder
    └── personalfile2

```

## Solution
<p>
  This tool designates a source & target folder. 
  It then finds all the files in the <b>source folder</b> owned by your personal account,
  and moves them to the exact corresponding position in the <b>target folder</b>. 
  (Sidenote: these files are also aggregated into folders where all the children are owned
  by your personal account, which is the while loop you will see)
</p>
<p>
  The choice of which folder to be source & target does not significantly matter,
  only that a target folder with less clutter is preferable
</p>

## How To
<p> Pull this repo. </p>

This tool is split into 2 steps, `1queryAllFiles.py` and `2mergeFiles.py`

<p>
  Read the sections below. 
</p>
<p>
  Update the constants at the top of each script, then run one after the other
</p>

### Authentication

This tool requires Google authentication. You can either:
1. Follow the steps at [Configure OAuth Consent](https://developers.google.com/workspace/guides/configure-oauth-consent)
   and [Create AccessCredentials](https://developers.google.com/workspace/guides/create-credentials)
   to obtain OAuth credentials in the form of a json. Rename this json `credentials.json`
2. Ask me (if you know me) for the credentials to my Google Cloud project. It will work,
   but I do not put it here for fear someone exhausts my quota

### Other Important Notes
- On first run, a webpage will appear requesting Google Account approval. It will say that 
  the project cannot be trusted (This is because the API access is done through a non-verified 
  Google Cloud project owned by me). If you feel like you can trust me 🤡 you can click the 
  `Continue` button regardless.
- The `token.json` generated on first run is a key to your account. Be **VERY CAREFUL** with this file. 

