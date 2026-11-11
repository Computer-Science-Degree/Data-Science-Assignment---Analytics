"""Autograder: runs each part's tests, awards partial credit, writes a summary.

Points per part are split evenly across that part's tests. Results are printed,
written to the GitHub Actions job summary, and saved to grading_results.json.
Exit code is 0 only when every test passes.
"""
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PARTS = [
    ("Part 1 - Python Foundations", "tests/test_part1_python_foundations.py", 10),
    ("Part 2 - NumPy", "tests/test_part2_numpy.py", 10),
    ("Part 3 - Pandas Analysis", "tests/test_part3_pandas_analysis.py", 15),
    ("Part 4 - Data Cleaning", "tests/test_part4_data_cleaning.py", 20),
    ("Part 5 - EDA & Visualisation", "tests/test_part5_eda_visualization.py", 15),
    ("Part 6 - Machine Learning", "tests/test_part6_machine_learning.py", 20),
    ("Part 7 - Report", "tests/test_part7_report.py", 10),
]


def run_part(test_file, report_path):
    subprocess.run(
        [sys.executable, "-m", "pytest", test_file, "-q", "--no-header", "-p", "no:cacheprovider",
         f"--junitxml={report_path}"],
        check=False,
    )
    if not report_path.exists():
        return 0, 1
    root = ET.parse(report_path).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    total = int(suite.get("tests", 0))
    failed = sum(int(suite.get(k, 0)) for k in ("failures", "errors", "skipped"))
    return max(total - failed, 0), max(total, 1)


def main():
    out_dir = Path("grading")
    out_dir.mkdir(exist_ok=True)
    rows, earned_total, max_total = [], 0.0, 0
    for name, test_file, points in PARTS:
        passed, total = run_part(test_file, out_dir / (Path(test_file).stem + ".xml"))
        earned = round(points * passed / total, 2)
        rows.append({"part": name, "passed": passed, "tests": total, "points": earned, "max_points": points})
        earned_total += earned
        max_total += points

    earned_total = round(earned_total, 2)
    lines = [
        "## Autograder Results",
        "",
        "| Part | Tests passed | Points |",
        "|---|---|---|",
        *[f"| {r['part']} | {r['passed']}/{r['tests']} | {r['points']}/{r['max_points']} |" for r in rows],
        f"| **Total** | | **{earned_total}/{max_total}** |",
        "",
        "_Part 7 is checked for completeness only; your instructor grades the writing quality._",
    ]
    summary = "\n".join(lines)
    print("\n" + summary)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(summary + "\n")
    Path("grading_results.json").write_text(
        json.dumps({"score": earned_total, "max_score": max_total, "parts": rows}, indent=2)
    )
    sys.exit(0 if earned_total == max_total else 1)


if __name__ == "__main__":
    main()
