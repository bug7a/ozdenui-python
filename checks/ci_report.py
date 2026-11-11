# Bismillah
"""ci_report.py - ozdenui v0.1 (OzdenUI: basic.js for Python)
The last runs of the CI of the repository (.github/workflows/tests.yml) in one report: the jobs that failed, the window
checks and the tests that failed in them with their problem, how often each one failed, and the times of the window
checks on each system. WHY: a check that failed in one job and passed in the others is a slow machine (flaky), one that
fails in every job is broken; the logs of all the jobs tell the two apart.
Usage: .venv/bin/python checks/ci_report.py [--runs 10] [--repo bug7a/ozdenui-python]
It needs the GitHub CLI (gh), logged in. The log of a finished job does not change: it is downloaded once, into the
temporary folder of the system.

Started Date: November 2026
Webpage: https://bug7a.github.io/ozdenui-python/

Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
Licensed under the Apache License, Version 2.0
SPDX-License-Identifier: Apache-2.0
"""

import argparse
import ast
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

REPOSITORY = "bug7a/ozdenui-python"
WORKFLOW_FILE = "tests.yml"
RUN_COUNT = 10
PAGE_SIZE = 100  # the most the API gives in one answer (runs, the jobs of a run)
DOWNLOADS_AT_ONCE = 8
TITLE_LENGTH = 60
LINES_BEFORE_ERROR = 5
LOG_FOLDER = os.path.join(tempfile.gettempdir(), "ozdenui-ci-logs")
TIME_STAMP = re.compile(r"^\d{4}-\d\d-\d\dT[\d:.]+Z ?")
COLOR_CODE = re.compile(r"\x1b\[[0-9;]*m")
CHECK_LINE = re.compile(r"^(PASS|FAIL)  (.+?) +(\d+(?:\.\d+)?) s$")  # run_all.py: "FAIL  chat         17.8 s"
PROBLEM_LINE = re.compile(r"^      - (.+)$")  # under it: '      - "play_chat line 453: ..."'
FAILED_TEST_LINE = re.compile(r"^(?:FAILED|ERROR) (\S+)(?: - (.*))?$")  # the short summary of pytest
TESTS_RAN_LINE = re.compile(r"^=+ .*\b(?:passed|failed)\b.* in [\d.]+s")  # "=== 448 passed, 1 skipped in 11.30s ==="
SYSTEM_OF_JOB = re.compile(r"\((\w+)[^,]*, ([^)]+)\)")  # "tests (macos-latest, 3.9)": macos, 3.9
ERROR_LINE = "##[error]"


def gh(path):
    """The answer of the GitHub API for a path ("repos/.../actions/runs"), as a text."""
    finished = subprocess.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if finished.returncode != 0:
        raise RuntimeError(finished.stderr.strip() or finished.stdout.strip())
    return finished.stdout


def log_lines(repository, job):
    """The lines of the log of a finished job, without their time stamps and colors ([]: GitHub has no log)."""
    path = os.path.join(LOG_FOLDER, f"{job['id']}.log")
    if not os.path.exists(path):
        try:
            text = gh(f"repos/{repository}/actions/jobs/{job['id']}/logs")
        except RuntimeError:
            return []  # WHY: GitHub keeps the logs for a time only (90 days)
        os.makedirs(LOG_FOLDER, exist_ok=True)
        with open(path + ".part", "w", encoding="utf-8") as file:
            file.write(text)
        os.replace(path + ".part", path)  # WHY: a download that was stopped must not be read as a whole log
    with open(path, encoding="utf-8", errors="replace") as file:
        return [COLOR_CODE.sub("", TIME_STAMP.sub("", line.rstrip("\r\n"))) for line in file]


def unquoted(text):
    """A problem as run_all.py printed it (the ascii() of the text), as it was written."""
    try:
        return str(ast.literal_eval(text))
    except (ValueError, SyntaxError):
        return text


def read_log(lines):
    """What a log says: the window checks of run_all.py, the failed tests of pytest, whether pytest ran, and the lines
    before the first error (a step that is not a check: the install, the download of WebView2)."""
    log = {"checks": [], "failed_tests": [], "tests_ran": False, "before_error": []}
    is_under_check = False
    for index, line in enumerate(lines):
        check = CHECK_LINE.match(line)
        problem = PROBLEM_LINE.match(line)
        failed_test = FAILED_TEST_LINE.match(line)
        if check:
            log["checks"].append({"name": check.group(2), "passed": check.group(1) == "PASS",
                                  "seconds": float(check.group(3)), "problems": []})
        elif problem and is_under_check:
            log["checks"][-1]["problems"].append(unquoted(problem.group(1)))
        elif failed_test:
            log["failed_tests"].append((failed_test.group(1), failed_test.group(2) or ""))
        elif TESTS_RAN_LINE.match(line):
            log["tests_ran"] = True
        elif line.startswith(ERROR_LINE) and not log["before_error"]:
            log["before_error"] = [text for text in lines[:index] if text.strip()][-LINES_BEFORE_ERROR:]
        is_under_check = bool(check) or (bool(problem) and is_under_check)
    return log


def system_of(job):
    """("macos", "3.9") from the name of a job of the matrix."""
    found = SYSTEM_OF_JOB.search(job["name"])
    return (found.group(1), found.group(2)) if found else (job["name"], "")


def jobs_of(repository, run):
    return json.loads(gh(f"repos/{repository}/actions/runs/{run['id']}/jobs?per_page={PAGE_SIZE}"))["jobs"]


def read_runs(repository, count):
    """The last runs, the newest first, with their jobs; a finished job with what its log says."""
    runs = json.loads(gh(f"repos/{repository}/actions/workflows/{WORKFLOW_FILE}/runs?per_page={count}"))["workflow_runs"]
    with ThreadPoolExecutor(DOWNLOADS_AT_ONCE) as pool:
        for run, jobs in zip(runs, pool.map(lambda run: jobs_of(repository, run), runs)):
            run["jobs"] = jobs
        finished = [job for run in runs for job in run["jobs"] if job["status"] == "completed"]
        for job, lines in zip(finished, pool.map(lambda job: log_lines(repository, job), finished)):
            job["log"] = read_log(lines)
    return runs


def jobs_with_logs(runs):
    return [job for run in runs for job in run["jobs"] if "log" in job]


def shortened(text):
    return text if len(text) <= TITLE_LENGTH else text[:TITLE_LENGTH - 3] + "..."


def print_failed_job(job):
    system, python = system_of(job)
    steps = ", ".join(step["name"] for step in job.get("steps", []) if step["conclusion"] == "failure")
    print(f"      {system} {python} failed in: {steps or '?'}")
    log = job.get("log")
    if log is None:
        return
    failed_checks = [check for check in log["checks"] if not check["passed"]]
    for check in failed_checks:
        print(f"          FAIL {check['name']} {check['seconds']} s: {'; '.join(check['problems'])}")
    for name, message in log["failed_tests"]:
        print(f"          FAILED {name}: {message}")
    if failed_checks or log["failed_tests"]:
        return
    for line in log["before_error"] or ["(no log)"]:
        print(f"          {line}")


def print_runs(runs, repository):
    print(f"The last {len(runs)} runs of {WORKFLOW_FILE} ({repository}), the newest first:")
    for run in runs:
        result = run["conclusion"] or run["status"]
        print(f"  {run['id']}  {run['head_sha'][:7]}  {run['head_branch']:<8} {result:<11} {shortened(run['display_title'])}")
        failed_jobs = [job for job in run["jobs"] if job["conclusion"] == "failure"]
        if failed_jobs:
            print(f"      {run['html_url']}")
        for job in failed_jobs:
            print_failed_job(job)


def version_key(python):
    return tuple(int(part) if part.isdigit() else 0 for part in python.split("."))


def where_text(by_commit):
    """ "b51740f macos 3.9; 3b7c91e windows 3.9/3.13/3.15": the commits of the runs, the newest first."""
    parts = []
    for commit, by_system in by_commit.items():
        systems = ", ".join(f"{system} {'/'.join(sorted(pythons, key=version_key))}" for system, pythons in by_system.items())
        parts.append(f"{commit} {systems}")
    return "; ".join(parts)


def print_failures(runs):
    """Every check and test that failed: in how many of the jobs that ran it, and where (the newest run first)."""
    jobs = jobs_with_logs(runs)
    tests_ran = sum(1 for job in jobs if job["log"]["tests_ran"])
    ran = {}
    places = {}  # name -> {the commit of a run: {system: [python, ...]}}
    for run in runs:
        for job in run["jobs"]:
            if "log" not in job:
                continue
            system, python = system_of(job)
            failed = [test for test, _ in job["log"]["failed_tests"]]
            for check in job["log"]["checks"]:
                name = f"{check['name']} (window check)"
                ran[name] = ran.get(name, 0) + 1
                if not check["passed"]:
                    failed.append(name)
            for name in failed:
                places.setdefault(name, {}).setdefault(run["head_sha"][:7], {}).setdefault(system, []).append(python)
    if not places:
        print(f"Nothing failed in the checks and the tests of these {len(jobs)} jobs.")
        return
    print("What failed (only some jobs of a run: flaky, a slow machine; every job of a system: broken in that commit):")
    width = max(len(name) for name in places) + 2
    for name, by_commit in places.items():
        count = sum(len(pythons) for by_system in by_commit.values() for pythons in by_system.values())
        # WHY tests_ran: pytest names only the tests that failed; the others ran wherever pytest ran
        print(f"  {name:<{width}} {count} of {ran.get(name, tests_ran)} jobs: {where_text(by_commit)}")


def print_times(runs):
    """The median and the slowest time of each window check on each system, in the order run_all.py runs them."""
    jobs = jobs_with_logs(runs)
    times = {}
    for job in jobs:
        system = system_of(job)[0]
        for check in job["log"]["checks"]:
            times.setdefault(check["name"], {}).setdefault(system, []).append(check["seconds"])
    if not times:
        return
    systems = sorted({system for by_system in times.values() for system in by_system})
    is_pair = len(systems) == 2
    width = max(len(name) for name in times) + 2
    print(f"The times of the window checks in s, from {len(jobs)} jobs (the median, the slowest in brackets):")
    print(f"  {'check':<{width}}" + "".join(f"{system:<16}" for system in systems) + (" / ".join(systems) if is_pair else ""))
    for name, by_system in times.items():
        cells = [by_system.get(system, []) for system in systems]
        line = f"  {name:<{width}}" + "".join(f"{f'{statistics.median(cell):.1f} ({max(cell):.1f})' if cell else '-':<16}" for cell in cells)
        if is_pair and all(cells):
            line += f"{statistics.median(cells[0]) / statistics.median(cells[1]):.2f}"
        print(line)


def main():
    parser = argparse.ArgumentParser(description="The last runs of the CI: what failed where, and the times of the window checks.")
    parser.add_argument("--runs", type=int, default=RUN_COUNT, help=f"how many runs, the newest first (default {RUN_COUNT})")
    parser.add_argument("--repo", default=REPOSITORY, help=f"the repository on GitHub (default {REPOSITORY})")
    arguments = parser.parse_args()
    if shutil.which("gh") is None:
        sys.exit("ci_report.py needs the GitHub CLI (gh): https://cli.github.com, then: gh auth login")
    sys.stdout.reconfigure(errors="replace")  # WHY: the console of Windows has an old code page
    try:
        runs = read_runs(arguments.repo, max(1, min(arguments.runs, PAGE_SIZE)))
    except RuntimeError as error:
        sys.exit(f"gh api: {error}")
    print_runs(runs, arguments.repo)
    print()
    print_failures(runs)
    print()
    print_times(runs)


if __name__ == "__main__":
    main()
