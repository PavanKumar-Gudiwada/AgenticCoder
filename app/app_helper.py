import os
import shutil


def make_workspace(directory):
    test_dir = os.path.join(directory, "tests")

    # Ensure the workspace exists before zipping
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)
        os.makedirs(test_dir, exist_ok=True)

    if not os.path.isdir(test_dir):
        os.makedirs(test_dir, exist_ok=True)


def delete_workspace(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
