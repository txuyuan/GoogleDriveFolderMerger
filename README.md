# GoogleDriveFolderMerger
A python tool to merge self-owned files in two folders, even if intermediate folders are owned by others

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
  were seperated into two folders within my personal account. Forr example: 
</p>

```
Archives
├── orgfile1
└── folder
    ├── orgfile2
    └── personalfile2
```
Becomes two folders:
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
<p>
  This tool is split into 2 steps:
</p>

1. `1queryAllFiles.py`:  A record of all your Google Drive files are pulled from online into `filetree.json`
2. `2mergeFiles.py`:     The files from `filetree.json` are filtered & the API calls to move them are executed

<p>
  Execute one script after the other, and ensure the constants at the top of each script are updated. 
</p>

