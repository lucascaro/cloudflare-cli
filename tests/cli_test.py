from cfcli import cli

import click
from click.testing import CliRunner

def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    assert result.output.startswith('Usage: cli')