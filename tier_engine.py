import csv

header = ["commits", "added", "deleted", "files", "bugfix_commits", "avg_files_per_commit", "avg_lines_per_commit", "weekend_rate", "experience"]

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

def calculate_percentile_boundaries(score):
    sorted_score = sorted(score)
    n= len(sorted_score)
    boundaries = []
    for i in range(1,6):
        index = int((i/6) * n)
        boundaries.append(sorted_score[index])
    return boundaries

def assign_tier(score, boundaries):
    if score >= boundaries[4]:
        return 1
    elif score >= boundaries[3]:
        return 2
    elif score >= boundaries[2]:
        return 3
    elif score >= boundaries[1]:
        return 4
    elif score >= boundaries[0]:
        return 5
    else:
        return 6


def load_data():
    with open("dataset.csv", "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        data=[]
        next(reader)
        for row in reader:
            numeric_row = [float(val) for val in row[1:-2]]  + [int(row[-1])]
            data.append(numeric_row)
    return data

def  unique_vals(data, col):
    return set([row[col] for row in data])


def class_counts(data):
    counts = {}
    for row in data:
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

def is_numeric(value):
    return isinstance(value, int) or isinstance(value, float)


class Question:
    def __init__(self, column, value):
        self.column = column
        self.value = value
        
    def match(self, example):
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value
        
    def __repr__(self):
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))
    
def partition(rows, question):
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows
    
def gini(rows):
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity

def info_gain(true_rows, false_rows, current_uncertainty):
    p = float(len(true_rows)) / float(len(true_rows) + len(false_rows))
    return current_uncertainty - p * gini(true_rows) - (1 - p) * gini(false_rows)

def find_best_split(rows):
    best_gain = 0
    best_question = None
    current_uncertainty = gini(rows)
    no_of_features = len(rows[0]) - 1
    
    for col in range(no_of_features):
        values = set([row[col] for row in rows])

        for val in values:
            question = Question(col,val)
            true_rows, false_rows = partition(rows, question)
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            gain = info_gain(true_rows, false_rows, current_uncertainty)

            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question


class Leaf:
    def __init__(self, rows):
        self.predictions = class_counts(rows)

class Decision_Node:
    def __init__(self, question, true_branch, false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


def build_tree(rows):
    gain, question = find_best_split(rows)

    if gain == 0:
        return Leaf(rows)
    
    true_rows, false_rows = partition(rows, question)

    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)

    return Decision_Node(question, true_branch, false_branch)


def classify(row, node):
    if isinstance(node, Leaf):
        return node.predictions
    
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


def print_tree(node, spacing =""):

    if isinstance(node, Leaf):
        print(spacing + "Predict", node.predictions)
        return
    
    print(spacing + str(node.question))

    print(spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    print(spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")

if __name__ == "__main__":
    data = load_data()
    tree = build_tree(data)
    print_tree(tree)