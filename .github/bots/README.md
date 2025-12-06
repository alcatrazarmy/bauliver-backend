# Regular Bot - Bronze-level Orchestrator PoC

This directory contains the Regular Bot, a proof-of-concept orchestrator for Bronze-level CI/CD automation.

## Overview

The Regular Bot is designed to:
- Monitor repository health
- Orchestrate Bronze-level CI checks
- Provide automated feedback on common issues
- Serve as a foundation for more advanced automation

## Components

### `regular_bot.py`
The main bot implementation. This PoC demonstrates:
- Health check orchestration
- Configuration management via environment variables
- JSON report generation
- Extensible architecture for future enhancements

## Usage

### Local Testing
```bash
# Run health checks
python .github/bots/regular_bot.py

# Run in dry-run mode (doesn't fail on errors)
BOT_DRY_RUN=true python .github/bots/regular_bot.py
```

### CI Integration
The bot can be integrated into GitHub Actions workflows:

```yaml
- name: Run Regular Bot health check
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    BOT_DRY_RUN: "false"
  run: |
    python .github/bots/regular_bot.py
```

## Configuration

The bot reads configuration from environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `GITHUB_TOKEN` | GitHub API token for authenticated requests | None |
| `GITHUB_REPOSITORY_OWNER` | Repository owner | `alcatrazarmy` |
| `GITHUB_REPOSITORY` | Repository name | `bauliver-backend` |
| `BOT_DRY_RUN` | Run in dry-run mode (true/false) | `false` |

## Health Checks

The bot currently performs the following Bronze-level checks:

1. **Workflow existence**: Verifies that `.github/workflows/bronze-ci.yml` exists
2. **Pre-commit config**: Checks for `.pre-commit-config.yaml`
3. **Python files**: Confirms Python source files are present

## Output

The bot generates a JSON report with the following structure:

```json
{
  "timestamp": "2025-12-06T23:41:18.573Z",
  "bot_version": "0.1.0-poc",
  "config": {
    "repo": "alcatrazarmy/bauliver-backend",
    "dry_run": false
  },
  "results": {
    "total_checks": 3,
    "passed": 3,
    "failed": 0,
    "checks_passed": ["workflow_file_exists", "precommit_config_exists", "python_files_exist"],
    "checks_failed": []
  },
  "status": "success"
}
```

## Future Enhancements

This PoC can be extended to include:
- PR comment automation
- Automated labeling based on check results
- Integration with additional CI/CD tools
- Custom check definitions via configuration files
- Slack/Discord notifications
- Performance metrics tracking

## Development

To extend the bot with new checks:

1. Add a new check method to the `RegularBot` class (e.g., `_check_new_feature()`)
2. Register the check in the `run_health_check()` method
3. Update this README with the new check documentation

## License

This bot is part of the Bauliver Backend project.
