#
#   This script runs through files in the source dir (defined below)
#   and searches for files owned by a specific account (defined below)
#
#   These are aggregated into folders that might all be owned by this
#   account, and all of these are then moved to the target directory (defined also).
#   This process preserves folder structures present in both directories
#

import json
import re

from googledriver import init_service

SOURCE_DIR="Hwa Chong (shared)"
TARGET_DIR="Hwa Chong"
ACC_EMAIL="t.xuyuan@gmail.com"

def fileInSource(file):
    return file["path"].strip(" /").split("/")[0] == SOURCE_DIR and \
            file["mimeType"] != "application/vnd.google-apps.folder" and \
            ACC_EMAIL in [owner["emailAddress"] for owner in file["owners"]]

def moveFile(source, target_parent, index):
    print(f"{index} ===\t{source['path']} -> {target_parent['path']}")
    
    # Query & logging
    service, creds = init_service()
    source_file = service.files().get(fileId=source["id"], fields="name, parents").execute()
    print(f"\tQueried source:   \t{source_file}")
    target_file = service.files().get(fileId=target_parent["id"], fields="name").execute()
    print(f"\tQueried target: \t{target_file}")
    
    # Execute API calls
    previous_parents = ",".join(source_file["parents"])
    file = (
        service.files()
        .update(
            fileId=source["id"],
            addParents=target_parent["id"],
            removeParents=previous_parents,
            fields="id, parents"
        )
        .execute()
    )
    print()
    return file

def main():
    with open("filetree.json", "r") as file:
        files = json.load(file)
    
    # Setup lookup indexes for the original file objects
    target_dir_index = {}
    for i, file in enumerate(files):
        if file["mimeType"] == "application/vnd.google-apps.folder" and file["path"].strip(" /").split("/")[0] == TARGET_DIR:
            target_dir_index[file["path"]] = i
    
    source_index = {}
    for i, file in enumerate(files):
        if file["path"].strip(" /").split("/")[0] == SOURCE_DIR:
            source_index[file["path"]] = i

    # Find files to transfer
    transfer_files = list(filter(fileInSource, files))
    already_transferred = []
   
    # Statistics
    total_moved = 0
    files_moved, folders_moved = 0, 0
    files_skipped = 0

    # MAIN FILE PROCESSING LOOP
    for file in transfer_files:

        # Checks
        path = file["path"]
        path_components = re.split(r'(?<!\\)/', path.strip().strip("/"))
        if len(path_components) < 2:
            continue
        
        skip_file = False
        for old_filepath in already_transferred:
            if path.startswith(old_filepath):
                #print(f"ALREADY {path} - {old_filepath}")
                skip_file = True
                files_skipped += 1
                break
        if skip_file:
            continue
      
        # Iteratively look for the largest file/folder that can be transferred
        source_path, parent_path = path_components, path_components[:-1]
        searching, iterlen = True, 0
        
        target_path = parent_path # The TARGET is the PARENT to be transferred to
        target_path[0] = TARGET_DIR
        target_dirname = "/" + "/".join(target_path) + "/"

        while target_dirname not in target_dir_index.keys() and len(parent_path) > 1:
            # Advance frame
            source_path = source_path[:-1]
            parent_path = parent_path[:-1]
            
            target_path = parent_path
            target_path[0] = TARGET_DIR
            target_dirname = "/" + "/".join(target_path) + "/"

            # Depth limits
            iterlen += 1
            if len(source_path) <= 1 or iterlen > 50:
                print("ERROR: recursion depth limit reached.")
                print(f"Filepath: {path}")
                print(f"Sourcepath: {source_path}, targetpath: {target_path}")
                print(f"Target Dirname: {target_dirname}")
                exit(1)

        target_dir = files[target_dir_index[target_dirname]]
        source_dirname = "/" + "/".join(source_path) + "/"
        source_dir = files[source_index[source_dirname]]
        
        # Execute MOVE API call
        moveFile(source_dir, target_dir, total_moved)
        
        # Prevent re-transfer of source directory children
        already_transferred += [source_dirname]
       
        # Statistics
        total_moved += 1
        if source_dir["mimeType"] == "application/vnd.google-apps.folder":
            folders_moved += 1
        else:
            files_moved += 1

    print()
    print(f"Total in source dir: {len(transfer_files)}")
    print(f"Total moved: {total_moved}")
    print(f"├── Folders: {folders_moved}")
    print(f"└── Files  : {files_moved}")
    print(f"Total files skipped: {files_skipped}")

if __name__ == "__main__":
    main()
