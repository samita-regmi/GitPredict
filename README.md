# GitPredict

GitPredict is a command-line repository analytics tool that mines Git history, extracts software-engineering metrics, ranks contributor performance, and recommends salary adjustments.

The project analyzes a Git repository to collect different contributor metrics such as commits, code changes, and maintenance activity. It then uses these metrics to predict a contributor's performance tier using a Decision Tree model and recommends a salary adjustment based on the prediction.

## Setup
1. Clone the repository
2. Make sure Python 3 is installed
3. No additional packages need to be installed; GitPredict uses only Python's built-in libraries.

## Usage

### Analyze a Repository
```bash
python gitpredict.py --analyze --repo path/to/repo
```
### Predict a Contributor
```bash
python gitpredict.py --predict --commits 3 --added 45 --deleted 8 --files 5 --exp 1 --bugfixes 0
```
## How It works?

### Module 1:
GitPredict first analyzes the repository and creates a structured dataset (dataset.csv). Each row represents a committer or a committer during a specific time period along with different repository metrics. This dataset gives the user a clear view of how much each contributor changed, how consistently they contributed, how much review or maintenance activity they generated, and how experienced they were in the project.

### Module 2:
GitPredict evaluates each committer and assigns them to one of six performance tiers using a Decision Tree classifier. Instead of looking at just the number of commits, it uses multiple repository metrics to compare contributors based on productivity, consistency, code changes, and maintenance activity.

### Module 3:
GitPredict estimates the recommended salary adjustment for a committer based on the predicted performance tier. The result is shown as a salary increase, no change, or salary decrease. The first three tiers indicate a salary increase, the fourth tier indicates no change, and the fifth and sixth tiers indicate a salary decrease.

### Module 4:
The user interacts with GitPredict through the command line. One command analyzes a repository and generates the dataset, while another command predicts the performance tier and recommended salary adjustment for a committer profile.

## Assumptions
- Salary adjustment percentages were manually defined: 
-Tier 1 → +15%
-Tier 2 → +12%
-Tier 3 → +8%
-Tier 4 → 0%
-Tier 5 → -8%
-Tier 6 → -10%
- Author experience is approximated as total commits minus 1
- Bugfix commits are identified by keywords: "fix", "bug", "patch" in commit messages
- Weekend commit rate is set to 0 for the --predict command since commit timing is unknown
- Performance tiers are generated using a weighted scoring formula since Git history does not contain real performance labels

## Limitations
### Multicollinearity:
I had used experience = commits - 1. So they're basically the same number. When two features are almost identical, the regression model gets confused about which one is actually causing the effect. That's why experience sometimes has a negative coefficient even though more experience should mean higher salary.

### Overfitting
The first question the decision tree asked was Is weekend_rate >= 1.0? This is technically correct for the training data but not meaningful in real life. The tree found a pattern that works on the data it saw but might not generalize well to new data. That's overfitting—the model learns the training data too well, including patterns that may not generalize to new repositories.

### Weekend rate issue:
When using --predict, the user doesn't provide weekend commit information. So we default it to 0. But since weekend_rate is an important feature in the decision tree, this might affect prediction accuracy.



