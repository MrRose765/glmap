"""Test the ghmap CLI with a sample input file and expected output."""

import subprocess
import filecmp
import tempfile
import os


def test_ghmap_cli_on_sample():
    """Run the ghmap CLI on sample data and compare outputs to expected results."""
    sample_dir = os.path.join(os.path.dirname(__file__), "data")

    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run([
            "python", "-m", "ghmap.cli",
            "--raw-events", os.path.join(sample_dir, "sample-events.json"),
            "--output-actions", os.path.join(tmpdir, "actions.jsonl"),
            "--output-activities", os.path.join(tmpdir, "activities.jsonl")
        ], check=True)

        assert filecmp.cmp(
            os.path.join(tmpdir, "actions.jsonl"),
            os.path.join(sample_dir, "expected-actions.jsonl"),
            shallow=False
        ), "Actions output does not match expected"

        assert filecmp.cmp(
            os.path.join(tmpdir, "activities.jsonl"),
            os.path.join(sample_dir, "expected-activities.jsonl"),
            shallow=False
        ), "Activities output does not match expected"
