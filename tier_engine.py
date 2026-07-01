def calculate_score(data, minmax):
    bugfix_ratio = data["bugfix_commits"]/data["commits"] if data["commits"] > 0 else 0
    normalized_commits = (data["commits"] - minmax["commits"]["min"]) / (minmax["commits"]["max"] - minmax["commits"]["min"]) if minmax["commits"]["max"] != minmax["commits"]["min"] else 0
    normalized_added = (data["added"] - minmax["added"]["min"]) / (minmax["added"]["max"] - minmax["added"]["min"]) if minmax["added"]["max"] != minmax["added"]["min"] else 0
    normalized_files = (data["files"] - minmax["files"]["min"]) / (minmax["files"]["max"] - minmax["files"]["min"]) if minmax["files"]["max"] != minmax["files"]["min"] else 0
    normalized_experience = (data["experience"] - minmax["experience"]["min"]) / (minmax["experience"]["max"] - minmax["experience"]["min"]) if minmax["experience"]["max"] != minmax["experience"]["min"] else 0
    normalized_avg_files_per_commit = (data["avg_files_per_commit"] - minmax["avg_files_per_commit"]["min"]) / (minmax["avg_files_per_commit"]["max"] - minmax["avg_files_per_commit"]["min"]) if minmax["avg_files_per_commit"]["max"] != minmax["avg_files_per_commit"]["min"] else 0
    normalized_weekend_rate = (data["weekend_rate"] - minmax["weekend_rate"]["min"]) / (minmax["weekend_rate"]["max"] - minmax["weekend_rate"]["min"]) if minmax["weekend_rate"]["max"] != minmax["weekend_rate"]["min"] else 0
    normalized_avg_lines_per_commit = (data["avg_lines_per_commit"] - minmax["avg_lines_per_commit"]["min"]) / (minmax["avg_lines_per_commit"]["max"] - minmax["avg_lines_per_commit"]["min"]) if minmax["avg_lines_per_commit"]["max"] != minmax["avg_lines_per_commit"]["min"] else 0
    normalized_bugfix_commits = (data["bugfix_commits"] - minmax["bugfix_commits"]["min"]) / (minmax["bugfix_commits"]["max"] - minmax["bugfix_commits"]["min"]) if minmax["bugfix_commits"]["max"] != minmax["bugfix_commits"]["min"] else 0


    score = (
    (normalized_commits*0.15)
    +(normalized_added*0.05)
    +(normalized_files*0.15)
    +(normalized_experience*0.15)
    +(normalized_avg_files_per_commit*0.15)
    +(normalized_weekend_rate*0.05) - (normalized_bugfix_commits*0.10)
    +(normalized_avg_lines_per_commit*0.15)
    )

    return score

def calculate_minmax(contributors):
    minmax = {
        "commits": {"min": float("inf"), "max": float("-inf")},
        "added": {"min": float("inf"), "max": float("-inf")},
        "deleted": {"min": float("inf"), "max": float("-inf")},
        "files": {"min": float("inf"), "max": float("-inf")},
        "bugfix_commits": {"min": float("inf"), "max": float("-inf")},
        "avg_files_per_commit": {"min": float("inf"), "max": float("-inf")},
        "avg_lines_per_commit": {"min": float("inf"), "max": float("-inf")},
        "weekend_rate": {"min": float("inf"), "max": float("-inf")},
        "experience": {"min": float("inf"), "max": float("-inf")}
    }

    for author, data in contributors.items():
        for key in minmax.keys():
            minmax[key]["min"] = min(minmax[key]["min"], data[key])
            minmax[key]["max"] = max(minmax[key]["max"], data[key])

    return minmax