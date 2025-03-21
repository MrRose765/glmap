import subprocess
import filecmp
import tempfile
import os


def test_ghmap_cli_on_sample():
    sample_dir = os.path.dirname(__file__) + "/data"

    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run([
            "python", "-m", "ghmap.cli",
            "--raw-events", f"{sample_dir}/sample-events.json",
            "--output-actions", f"{tmpdir}/actions.jsonl",
            "--output-activities", f"{tmpdir}/activities.jsonl"
        ], check=True)

        assert filecmp.cmp(
            f"{tmpdir}/actions.jsonl",
            f"{sample_dir}/expected-actions.jsonl",
            shallow=False
        ), "Actions output does not match expected"

        assert filecmp.cmp(
            f"{tmpdir}/activities.jsonl",
            f"{sample_dir}/expected-activities.jsonl",
            shallow=False
        ), "Activities output does not match expected"