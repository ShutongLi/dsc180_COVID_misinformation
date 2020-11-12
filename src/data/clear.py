#CLEAR ANY DATA THAT HAS DOWNLOADED SO FAR BANGBANGBAGN

import os
import shutil

# helper function
def obliviate(path):
    for fname in os.listdir(path):
        file_path = os.path.join(path, fname)
        try:
            if os.path.isfile(file_path):
                # ELDRITCH BLAST!!!!
                os.remove(file_path)
            elif os.path.isdir(file_path):
                # ELDRITCH BLAST!!!!
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# clear script
def clean(paths):
    for path in paths:
        obliviate(path)
    