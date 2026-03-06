import os
import datetime
import random

# --- Configuration ---
# In GitHub Actions, GITHUB_WORKSPACE is the root of your repo
REPO_PATH = os.environ.get("GITHUB_WORKSPACE", ".") 
PROBLEMS_FILE = os.path.join(REPO_PATH, "problems.txt")

# A curated list of beginner-friendly LeetCode problems
BEGINNER_PROBLEMS = [
    ("Contains Duplicate", "https://leetcode.com/problems/contains-duplicate/", "Arrays & Hashing"),
    ("Valid Anagram", "https://leetcode.com/problems/valid-anagram/", "Arrays & Hashing"),
    ("Two Sum", "https://leetcode.com/problems/two-sum/", "Arrays & Hashing"),
    ("Group Anagrams", "https://leetcode.com/problems/group-anagrams/", "Arrays & Hashing"),
    ("Valid Palindrome", "https://leetcode.com/problems/valid-palindrome/", "Two Pointers"),
    ("Two Sum II - Input Array Is Sorted", "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/", "Two Pointers"),
    ("3Sum", "https://leetcode.com/problems/3sum/", "Two Pointers"),
]

def get_solved_problems():
    if not os.path.exists(PROBLEMS_FILE):
        # If the file doesn't exist, create an empty one
        with open(PROBLEMS_FILE, "w") as f:
            pass
        return set()
    with open(PROBLEMS_FILE, "r") as f:
        return {line.strip() for line in f if line.strip()}

def add_solved_problem(problem_name):
    with open(PROBLEMS_FILE, "a") as f:
        f.write(f"{problem_name}\\n")

def select_problem(solved_problems):
    available_problems = [p for p in BEGINNER_PROBLEMS if p[0] not in solved_problems]
    if not available_problems:
        print("All beginner problems solved!")
        return None
    return random.choice(available_problems)

def generate_python_solution(problem_name, problem_url, topic):
    return f"""# LeetCode Problem: {problem_name}
# Link: {problem_url}
# Topic: {topic}

class Solution:
    def solve(self, *args) -> any:
        # Write your solution here
        pass
"""

def generate_markdown_description(problem_name, problem_url, topic):
    return f"""# {problem_name}
**Link:** [{problem_name}]({problem_url})
**Topic:** {topic}

## Solution Approach
[Describe your thought process here.]

## Complexity
- **Time:** O(N)
- **Space:** O(1)
"""

def main():
    # Ensure we are in the right directory
    print(f"Working directory: {os.getcwd()}")
    print(f"Repo path: {REPO_PATH}")
    
    solved_problems = get_solved_problems()
    problem = select_problem(solved_problems)

    if problem is None:
        return

    problem_name, problem_url, topic = problem
    sanitized_name = problem_name.replace(" ", "_").replace("-", "_")
    today = datetime.date.today().strftime("%Y-%m-%d")

    # Create folder: Topic/YYYY-MM-DD_ProblemName
    topic_dir = os.path.join(REPO_PATH, topic.replace(" ", "_"))
    problem_dir = os.path.join(topic_dir, f"{today}_{sanitized_name}")
    os.makedirs(problem_dir, exist_ok=True)

    # Create files
    with open(os.path.join(problem_dir, f"{sanitized_name}.py"), "w") as f:
        f.write(generate_python_solution(problem_name, problem_url, topic))
    
    with open(os.path.join(problem_dir, "README.md"), "w") as f:
        f.write(generate_markdown_description(problem_name, problem_url, topic))

    add_solved_problem(problem_name)
    print(f"Successfully processed: {problem_name}")

if __name__ == "__main__":
    main()
    
