from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_site.py"


class SiteValidationTests(unittest.TestCase):
    def run_validator(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_site_contract_is_satisfied(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Legal site validation passed", result.stdout)

    def test_long_legal_copy_cannot_overflow_mobile_width(self) -> None:
        css = (ROOT / "assets/site.css").read_text(encoding="utf-8")
        self.assertIn("overflow-wrap: anywhere", css)


if __name__ == "__main__":
    unittest.main()
