import sys
from extractor import run

if __name__ == "__main__":
    if "--analyze" in sys.argv and "--repo" in sys.argv:
        repo_index = sys.argv.index("--repo") + 1
        repo_path = sys.argv[repo_index]
        run(repo_path)