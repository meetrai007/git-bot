import os
import subprocess
from datetime import datetime, timedelta
import random

# Parameters
REPO_PATH = r"C:\Users\deepr\OneDrive\Desktop\git-bot\git-bot"
START_DATE = datetime.now() - timedelta(days=400)
END_DATE = datetime.now()
MIN_COMMITS_PER_DAY = 1
MAX_COMMITS_PER_DAY = 4

def set_git_date(date):
    """Sets the GIT_AUTHOR_DATE and GIT_COMMITTER_DATE environment variables."""
    formatted_date = date.strftime("%Y-%m-%dT%H:%M:%S")
    os.environ["GIT_AUTHOR_DATE"] = formatted_date
    os.environ["GIT_COMMITTER_DATE"] = formatted_date

def run_git_command(command, repo_path):
    """Runs a Git command and checks for errors."""
    result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command {command}: {result.stderr}")

def commit_changes(repo_path, message="Automated commit"):
    """Creates a commit with a specific message."""
    dummy_file_path = os.path.join(repo_path, "dummy.txt")
    
    directory = os.path.dirname(dummy_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if not os.path.exists(dummy_file_path):
        with open(dummy_file_path, "w") as file:
            file.write("Commit Log Start\n")

    with open(dummy_file_path, "a") as file:
        file.write(f"Commit on {datetime.now()}\n")
        
    run_git_command(["git", "add", "."], repo_path)
    run_git_command(["git", "commit", "-m", message], repo_path)

def random_time_on_day(day):
    """Generates a random time for a given day."""
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return day.replace(hour=hour, minute=minute, second=second)

def main():
    current_date = START_DATE

    while current_date <= END_DATE:
        if random.random() < 0.2:
            days_to_skip = random.randint(1, 2)
            print(f"Skipping {days_to_skip} days...")
            current_date += timedelta(days=days_to_skip)
            continue

        commits_today = random.randint(MIN_COMMITS_PER_DAY, 2) if current_date.weekday() == 6 else random.randint(MIN_COMMITS_PER_DAY, MAX_COMMITS_PER_DAY)

        print(f"Making {commits_today} commits on {current_date.date()}...")

        for _ in range(commits_today):
            random_time = random_time_on_day(current_date)
            set_git_date(random_time)
            message = f"Automated commit on {random_time.strftime('%Y-%m-%d %H:%M:%S')}"
            commit_changes(REPO_PATH, message)

        current_date += timedelta(days=1)

    print("All commits are done!")

if __name__ == "__main__":
    main()
