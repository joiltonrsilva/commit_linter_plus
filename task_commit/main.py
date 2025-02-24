from .core import git_commit
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    """
    Main function that calls the git_commit function to perform the commit.
    """

    git_commit()
