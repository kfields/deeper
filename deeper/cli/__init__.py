import os
import click

import cProfile
import pstats

from ..app import main


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand is None:
        main()


@cli.command()
@click.pass_context
def run(ctx):
    main()

@cli.command()
@click.pass_context
def profile(ctx):
    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('time').print_stats(10)

    profiler.dump_stats('deeper.prof')
