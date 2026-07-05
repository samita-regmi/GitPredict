import subprocess
import csv
import os
from datetime import datetime
from tier_engine import calculate_minmax, calculate_score, assign_tier,calculate_percentile_boundaries, calculate_salary_adjustment

def extract(repo_path):
    result = subprocess.run(
    ["git","log","--stat"],
    capture_output=True,
    text=True,
    cwd=repo_path,
    encoding='utf-8',
    errors='replace')

    print(result.returncode)
    print(result.stderr)

    commits = result.stdout.split("commit ")
    contributors = {}

    for block in commits:
        if not block.strip():
            continue

        lines = block.split("\n")

        author = ""
        date = ""
        message = ""
        added = 0
        deleted = 0
        files = 0

        for line in lines:
            if line.startswith("Author:"):
                author = line.split("Author:")[1].split(" <")[0]
            elif line.startswith("Date:"):
                date = line.split("Date:")[1].strip()
            elif line.startswith("    "):
                message = line.strip()
            elif "files changed" in line:
                parts = line.split(",")
                try:
                    for part in parts:
                        if "insertion" in part:
                            added = int(part.strip().split(" ")[0])
                        if "deletion" in part:
                            deleted = int(part.strip().split(" ")[0])
                except:
                    pass

        if author:
            if author not in contributors:
                contributors[author] = {
                    "commits": 0,
                    "added": 0,
                    "deleted": 0,
                    "files": 0,
                    "bugfix_commits": 0,
                    "weekend_commits": 0,
                    "dates": []
                }

            contributors[author]["commits"] += 1
            contributors[author]["added"] += added
            contributors[author]["deleted"] += deleted
            contributors[author]["files"] += files

            
            if "fix" in message.lower() or "bug" in message.lower() or "patch" in message.lower():
                contributors[author]["bugfix_commits"] += 1

            try:
                date_obj = datetime.strptime(date, "%a %b %d %H:%M:%S %Y %z")
                if date_obj.weekday() >= 5:
                    contributors[author]["weekend_commits"] += 1
            except:
                pass

    return contributors


def calculate_features(contributors):
    for author, data in contributors.items():
        commits = data["commits"]

        data["avg_files_per_commit"] = round(data["files"]/commits, 2) if commits > 0 else 0
        data["weekend_rate"] = round(data["weekend_commits"]/commits,2) if commits > 0 else 0
        data["experience"] = commits -1
        data["avg_lines_per_commit"] = round((data["added"] + data["deleted"])/commits, 2) if commits > 0 else 0

    return contributors


def save_csv(contributors):
    with open("dataset.csv", "w", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["author","commits","added","deleted","files","bugfix_commits","avg_files_per_commit","avg_lines_per_commit","weekend_rate","experience","score","tier","salary_adjustment"])
        for author, data in contributors.items():
            writer.writerow([author,
                            data["commits"],
                            data["added"],
                            data["deleted"],
                            data["files"],
                            data["bugfix_commits"],
                            data["avg_files_per_commit"],
                            data["avg_lines_per_commit"],
                            data["weekend_rate"],
                            data["experience"],
                            data["score"],
                            data["tier"],
                            data["salary_adjustment"]
                            ])
            

def run(repo_path):
    contributors = extract(repo_path)
    contributors = calculate_features(contributors)
    minmax = calculate_minmax(contributors)
    for contributor, data in contributors.items():
        score = calculate_score(data, minmax)
        contributors[contributor]["score"] = score

    scores = [data["score"] for data in contributors.values()]
    boundaries = calculate_percentile_boundaries(scores)

    for contributor, data in contributors.items():
        tier = assign_tier(data["score"], boundaries)
        contributors[contributor]["tier"] = tier

    for contributor, data in contributors.items():
        salary = calculate_salary_adjustment(data["tier"])
        contributors[contributor]["salary_adjustment"] = salary
    save_csv(contributors)
    print("dataset.csv generated successfully!")