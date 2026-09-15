from pathlib import Path

import yaml


PIPELINE_PATH = Path(__file__).resolve().parent.parent / "pipelines" / "copy-clair-scan-results.yaml"


def test_clair_copy_pipeline_uses_the_reusable_git_resolved_task():
    pipeline = yaml.safe_load(PIPELINE_PATH.read_text())
    task = pipeline["spec"]["tasks"][0]

    assert task["name"] == "copy-clair-scan-results-task"
    assert "taskSpec" not in task
    assert task["taskRef"] == {
        "resolver": "git",
        "params": [
            {"name": "url", "value": "https://github.com/red-hat-data-services/aipcc-konflux-data"},
            {"name": "revision", "value": "main"},
            {"name": "pathInRepo", "value": "tasks/copy-clair-scan-results.yaml"},
        ],
    }
    assert task["params"] == [
        {"name": "snapshot", "value": "$(params.snapshot)"},
        {"name": "target-repo", "value": "$(params.target-repo)"},
    ]
    assert [param["name"] for param in pipeline["spec"]["params"]] == [
        "release",
        "releasePlan",
        "snapshot",
        "target-repo",
    ]
