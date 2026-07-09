import sys
import json
from extractor import run
from tier_engine import assign_tier, calculate_score, calculate_salary_adjustment, get_tier_label, get_decision_reason, get_salary_recommendation, load_data, build_tree, print_tree, run_regression

if __name__ == "__main__":
    if "--analyze" in sys.argv and "--repo" in sys.argv:
        repo_index = sys.argv.index("--repo") + 1
        repo_path = sys.argv[repo_index]
        run(repo_path)
        run_regression()
        print_tree(build_tree(load_data()))
    if "--predict" in sys.argv:
        commit_index = sys.argv.index("--commits") + 1
        commits = int(sys.argv[commit_index])
        added_index = sys.argv.index("--added") + 1
        added = int(sys.argv[added_index])
        deleted_index = sys.argv.index("--deleted") + 1
        deleted= int(sys.argv[deleted_index])
        files_index = sys.argv.index("--files") + 1
        files = int(sys.argv[files_index])
        exp_index = sys.argv.index("--exp") + 1
        exp = int(sys.argv[exp_index])
        bugfixes_index = sys.argv.index("--bugfixes") + 1
        bugfixes = int(sys.argv[bugfixes_index])
    
        with open("minmax.json","r") as f:
            minmax = json.load(f)
        with open("boundaries.json","r") as f:
            boundaries = json.load(f)

        new_contributor = {
        "commits": commits,
        "added": added,
        "deleted": deleted,
        "files": files,
        "bugfix_commits": bugfixes,
        "weekend_commits": 0,
        "avg_files_per_commit": round(files/commits, 2) if commits > 0 else 0,
        "avg_lines_per_commit": round((added + deleted)/commits, 2) if commits > 0 else 0,
        "experience": commits - 1,
        "weekend_rate": 0
        }

        score = calculate_score(new_contributor, minmax)
        tier = assign_tier(score, boundaries)
        salary_adjustment = calculate_salary_adjustment(tier)
        print("=============================")
        print("GIT PREDICT RADAR FORECAST")
        print("============================")
        print("Committer Performance Tier : ",get_tier_label(tier))
        print(f"Salary Adjustment Forecast: {salary_adjustment * 100:+.1f}%")
        print("Recommendation : ",get_salary_recommendation(tier))
        print("Decision Reason :",get_decision_reason(tier))
        print("=============================")
