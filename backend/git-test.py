import git
import sys

def run_git_blame(file_path, lineno):
    try:
        repo = git.Repo(search_parent_directories=True)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            total_lines = len(lines)

        if lineno > total_lines:
            print(f"Error: Line number {lineno} exceeds the total number of lines in the file ({total_lines}).")
            return

        blame_result = repo.blame('HEAD', file_path, L=lineno)
        
        for commit, lines in blame_result:
            print(f"Commit: {commit.hexsha}")
            print(f"Author: {commit.author.name} <{commit.author.email}>")
            print(f"Date: {commit.authored_datetime}")
            print("Lines:")
            for line in lines:
                print(line.strip())
            print()
            
    except git.exc.InvalidGitRepositoryError:
        print("Error: This directory is not a valid Git repository.")
        sys.exit(1)


def analyze_code_with_git(file_path, issues):
    for lineno, message in issues:
        print(f"- Line {lineno}: {message}")
        print("Running git blame to check for recent changes...")
        blame_output = run_git_blame(file_path, lineno)
        print(blame_output)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python git_code_analyzer.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Example issues detected in the code analysis (replace with actual detected issues)
    issues = [(5, "Method is too long"), (10, "Excessive nesting")]

    analyze_code_with_git(file_path, issues)
