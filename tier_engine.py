def calculate_score(data):
    bugfix_ratio = data["bugfix_commits"]/data["commits"] if data["commits"] > 0 else 0
    score = (
    (data["commits"]*0.25)
    +(data["added"]*0.25)
    +(data["files"]*0.15)
    +(data["experience"]*0.15)
    +(data["avg_files_per_commit"]*0.15)
    +(data["weekend_rate"]*0.05) - (bugfix_ratio*0.10)
    )

    return score