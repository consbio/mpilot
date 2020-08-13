from __future__ import absolute_import

import os
import sys

import click

from ..commands import Command
from ..exceptions import MPilotError, ProgramError
from ..program import Program

LINE_CONTEX_LENGTH = 3


@click.command()
@click.argument("path")
def main(path):
    if not os.path.exists(path):
        sys.stderr.write(
            "\n".join(
                (
                    "Problem: The specified command file does not exist: {}".format(path),
                    "Solution: Check the path to the command file and try again.",
                )
            )
        )
        sys.stderr.write("\n")
        sys.exit(-1)

    with open(path) as f:
        lines = [line.strip("\n\r") for line in f.readlines()]
    source = "\n".join(lines)

    Command.load_commands('mpilot.libraries')

    try:
        program = Program.from_source(source)
    except MPilotError as ex:
        sys.stderr.write("\n".join(("ERROR: There was a problem running the MPilot command file.", str(ex))))
        sys.stderr.write("\n")

        if isinstance(ex, ProgramError) and ex.lineno is not None:
            idx = ex.lineno - 1
            start = max(idx - LINE_CONTEX_LENGTH, 0)
            end = min(idx + LINE_CONTEX_LENGTH, len(lines))

            sys.stderr.write("\n".join((" " * 4 + line for line in lines[start:idx])))
            sys.stderr.write("\n")
            sys.stderr.write("--> {}".format(lines[idx]))
            sys.stderr.write("\n")
            sys.stderr.write("\n".join((" " * 4 + line for line in lines[idx + 1 : end])))
            sys.stderr.write("\n")

        sys.exit(-1)
