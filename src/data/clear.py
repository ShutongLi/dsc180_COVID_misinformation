# Clear any data that has been downloaded

import os
import shutil

# Delete all files and directories in a path
def obliviate(path):
    for fname in os.listdir(path):
        print(f'deleting{fname} under {path}')
        file_path = os.path.join(path, fname)
        try:
            # Delete file in path
            if os.path.isfile(file_path):
                os.remove(file_path)
            
            # Delete directory in path
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            # Failsafe: potential error for deleting paths
            print(f'Failed to delete {file_path}. Reason: {e}')

# Delete files for all paths
def clean(paths):
    for path in paths:
        obliviate(path)
    