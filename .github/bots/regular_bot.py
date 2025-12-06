"""
Regular Bot - Orchestrator PoC
Bronze-level automation bot for managing CI/CD tasks and repository health.

This is a proof-of-concept for a bot that can:
- Monitor PR health checks
- Trigger additional workflows
- Provide automated feedback on common issues
- Orchestrate Bronze-level CI tasks

Usage:
    python .github/bots/regular_bot.py [options]
"""

import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BotConfig:
    """Configuration for the Regular Bot."""

    github_token: str | None = None
    repo_owner: str = "alcatrazarmy"
    repo_name: str = "bauliver-backend"
    dry_run: bool = False

    @classmethod
    def from_env(cls) -> "BotConfig":
        """Load configuration from environment variables."""
        github_repo = os.getenv("GITHUB_REPOSITORY", "alcatrazarmy/bauliver-backend")
        repo_parts = github_repo.split("/")
        # Use last part if split resulted in multiple parts and last part is non-empty
        repo_name = (
            repo_parts[-1]
            if len(repo_parts) > 1 and repo_parts[-1]
            else "bauliver-backend"
        )

        return cls(
            github_token=os.getenv("GITHUB_TOKEN"),
            repo_owner=os.getenv("GITHUB_REPOSITORY_OWNER", "alcatrazarmy"),
            repo_name=repo_name,
            dry_run=os.getenv("BOT_DRY_RUN", "false").lower() == "true",
        )


class RegularBot:
    """
    Regular Bot orchestrator for Bronze-level CI/CD automation.

    This PoC demonstrates basic bot functionality for:
    - Health monitoring
    - Check orchestration
    - Automated PR feedback
    """

    def __init__(self, config: BotConfig):
        self.config = config
        self.checks_passed: list[str] = []
        self.checks_failed: list[str] = []

    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp."""
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] [{level}] {message}", file=sys.stderr)

    def run_health_check(self) -> bool:
        """
        Run basic health checks on the repository.

        Returns:
            bool: True if all checks pass, False otherwise.
        """
        self.log("Starting Bronze-level health checks...")

        checks = {
            "workflow_file_exists": self._check_workflow_exists(),
            "precommit_config_exists": self._check_precommit_config(),
            "python_files_exist": self._check_python_files(),
        }

        for check_name, passed in checks.items():
            if passed:
                self.checks_passed.append(check_name)
                self.log(f"✓ {check_name}", "PASS")
            else:
                self.checks_failed.append(check_name)
                self.log(f"✗ {check_name}", "FAIL")

        return len(self.checks_failed) == 0

    def _check_workflow_exists(self) -> bool:
        """Check if Bronze CI workflow exists."""
        workflow_path = ".github/workflows/bronze-ci.yml"
        return os.path.exists(workflow_path)

    def _check_precommit_config(self) -> bool:
        """Check if pre-commit configuration exists."""
        return os.path.exists(".pre-commit-config.yaml")

    def _check_python_files(self) -> bool:
        """Check if Python files exist in the repository."""
        for root, dirs, files in os.walk("."):
            # Skip hidden directories and common exclusions
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".") and d not in ["venv", "node_modules"]
            ]
            for file in files:
                if file.endswith(".py"):
                    return True
        return False

    def generate_report(self) -> dict:
        """
        Generate a JSON report of the bot's findings.

        Returns:
            Dict: Report containing check results and metadata.
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "bot_version": "0.1.0-poc",
            "config": {
                "repo": f"{self.config.repo_owner}/{self.config.repo_name}",
                "dry_run": self.config.dry_run,
            },
            "results": {
                "total_checks": len(self.checks_passed) + len(self.checks_failed),
                "passed": len(self.checks_passed),
                "failed": len(self.checks_failed),
                "checks_passed": self.checks_passed,
                "checks_failed": self.checks_failed,
            },
            "status": "success" if len(self.checks_failed) == 0 else "failure",
        }

    def run(self) -> int:
        """
        Main entry point for the bot.

        Returns:
            int: Exit code (0 for success, 1 for failure).
        """
        self.log(f"Regular Bot starting (dry_run={self.config.dry_run})...")

        # Run health checks
        health_ok = self.run_health_check()

        # Generate and print report
        report = self.generate_report()
        print(json.dumps(report, indent=2))

        # Summary
        passed = report["results"]["passed"]
        total = report["results"]["total_checks"]
        self.log(f"Checks completed: {passed}/{total} passed")

        if not health_ok and not self.config.dry_run:
            self.log("Health checks failed!", "ERROR")
            return 1

        self.log("Regular Bot completed successfully!", "SUCCESS")
        return 0


def main():
    """Main function to run the Regular Bot."""
    config = BotConfig.from_env()
    bot = RegularBot(config)
    sys.exit(bot.run())


if __name__ == "__main__":
    main()
