#
#
#
# (C)2024 F Basti KO4HXC
#
# License GPLv2
#

# python included libs
import datetime
import importlib.metadata as imp
from importlib.metadata import version as metadata_version
import logging
import signal
import sys
import time

import click
from oslo_config import cfg, generator

# local imports here
import mltd
# from mltd import cli_helper, packets, threads, utils
# from aprsd.stats import collector
# from mltd import cli_helper, threads, utils
from mltd import cli_helper, utils, threads

# setup the global logger
# log.basicConfig(level=log.DEBUG) # level=10
CONF = cfg.CONF
LOG = logging.getLogger("MLTD")
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
flask_enabled = False


@click.group(cls=cli_helper.AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.version_option()
@click.pass_context
def cli(ctx):
    pass


def load_commands():
    from .cmds import (  # noqa
       tune, 
    )


def main():
    # First import all the possible commands for the CLI
    # The commands themselves live in the cmds directory
    load_commands()
    # utils.load_entry_points("aprsd.extension")
    cli(auto_envvar_prefix="MLTD")


def signal_handler(sig, frame):
    global flask_enabled

    click.echo("signal_handler: called")
    threads.MLTDThreadList().stop_all()
    if "subprocess" not in str(frame):
        LOG.info(
            "Ctrl+C, Sending all threads exit! Can take up to 10 seconds {}".format(
                datetime.datetime.now(),
            ),
        )
        time.sleep(1.5)
        # packets.PacketTrack().save()
        #  packets.WatchList().save()
        # packets.SeenList().save()
        # packets.PacketList().save()
        # collector.Collector().collect()
        # signal.signal(signal.SIGTERM, sys.exit(0))
        # sys.exit(0)

    if flask_enabled:
        signal.signal(signal.SIGTERM, sys.exit(0))


@cli.command()
@cli_helper.add_options(cli_helper.common_options)
@click.pass_context
@cli_helper.process_standard_options_no_config
def check_version(ctx):
    """Check this version against the latest in pypi.org."""
    level, msg = utils._check_version()
    if level:
        click.secho(msg, fg="yellow")
    else:
        click.secho(msg, fg="green")


@cli.command()
@click.pass_context
def sample_config(ctx):
    """Generate a sample Config file from aprsd and all installed plugins."""

    def _get_selected_entry_points():
        import sys
        if sys.version_info < (3, 10):
            all = imp.entry_points()
            selected = []
            if "oslo.config.opts" in all:
                for x in all["oslo.config.opts"]:
                    if x.group == "oslo.config.opts":
                        selected.append(x)
        else:
            selected = imp.entry_points(group="oslo.config.opts")

        return selected

    def get_namespaces():
        args = []

        # selected = imp.entry_points(group="oslo.config.opts")
        selected = _get_selected_entry_points()
        for entry in selected:
            if "mltd" in entry.name:
                args.append("--namespace")
                args.append(entry.name)

        return args

    args = get_namespaces()
    config_version = metadata_version("oslo.config")
    logging.basicConfig(level=logging.WARN)
    conf = cfg.ConfigOpts()
    generator.register_cli_opts(conf)
    try:
        conf(args, version=config_version)
    except cfg.RequiredOptError:
        conf.print_help()
        if not sys.argv[1:]:
            raise SystemExit
        raise
    generator.generate(conf)
    return


@cli.command()
@click.pass_context
def version(ctx):
    """Show the MLTD version."""
    click.echo(click.style("MLTD Version : ", fg="white"), nl=False)
    click.secho(f"{mltd.__version__}", fg="yellow", bold=True)


if __name__ == "__main__":
    main()
