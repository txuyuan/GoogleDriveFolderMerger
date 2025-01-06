#
#   This recursively queries files from the root of your Google Drive,
#   regardless of file owner.
#
#   Doing it this way also allows for the full paths of files "/folder1/folder2/..."
#   to be ascertained, since Google Drive files only store the ID of their direct
#   parent.
#
#   Results will be saved to filetree.json, which is used by part 2
#

import os
import copy
import json
from concurrent.futures import ThreadPoolExecutor, wait

from googledriver import init_service

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

FOLDER_MIMETYPE = "application/vnd.google-apps.folder"

def search_folder(executor, folder_id, folder_path, depth=0):
    # Recursive depth limit
    if depth > 30:
        return []
    
    # Init service
    service, creds = init_service()

    # Main Query
    results = (
        service.files()
        .list(
            pageSize=100,
            orderBy="name, recency",
            fields="files(id, name, mimeType, owners)",
            q=f"""
            '{folder_id}' in parents
            and trashed = false
            """
        )
        .execute()
    )

    # Display
    print(f"Queried: \t{folder_path}")
    ##for i, file in enumerate(results["files"]):
    ##    print(i, file)

    # Process files & folders
    files = []
    futures = []
    for file in results["files"]:
        file_name = file["name"].replace("/", "\/")
        file_path = folder_path + file_name + "/"

        if file["mimeType"] == FOLDER_MIMETYPE:
            # FOLDER
            try:
                # Queue further recursion on folders
                future = executor.submit(search_folder, executor, file["id"], file_path)
                futures += [future]
            except Exception as e:
                # Special error handling
                print(e)
                with open("logs/errors.log", "a+") as file:
                    file.write(str(e))
        
        # FILE OR FOLDER
        # Add files to registry of this folder
        fileRecord = copy.copy(file)
        fileRecord["path"] = file_path
        del fileRecord["name"]
        files += [fileRecord]

    # Return this folder's results
    return files, futures

def main():
    service, creds = init_service()

    # Recursive root call
    with ThreadPoolExecutor(max_workers=12) as executor:
        files, futures = search_folder(executor, "root", "/")
        wait(futures)

        while len(futures) > 0:
            for future in futures:
                sub_files, sub_futures = future.result()
                futures.remove(future)

                files += sub_files
                futures += sub_futures

    # Display flat file registry with paths
    for i, file in enumerate(files):
        print(file)
    print(f"Total files found: {len(files)}")

    # Dump into JSON
    with open("filetree.json", "w+") as out_file:
        json.dump(files, out_file, indent=4)

    print("Complete!")

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occured: {e}")
