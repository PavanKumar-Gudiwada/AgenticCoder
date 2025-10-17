import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from app.app_helper import cleanup_workspace

if __name__ == "__main__":
    cleanup_workspace()
    print("Workspace cleaned up.")
