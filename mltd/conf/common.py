from pathlib import Path

from oslo_config import cfg


home = str(Path.home())
DEFAULT_CONFIG_DIR = f"{home}/.config/mltd/"
APRSD_DEFAULT_MAGIC_WORD = "CHANGEME!!!"

tune_group = cfg.OptGroup(
    name="tune",
    title="Settings specific to the tune command",
)

mltd_opts = [
    cfg.StrOpt(
        "callsign",
        required=True,
        help="Callsign to use for messages sent by APRSD",
    ),
    cfg.BoolOpt(
        "enable_save",
        default=True,
        help="Enable saving of watch list, packet tracker between restarts.",
    ),
    cfg.StrOpt(
        "save_location",
        default=DEFAULT_CONFIG_DIR,
        help="Save location for packet tracking files.",
    ),
    cfg.BoolOpt(
        "trace_enabled",
        default=False,
        help="Enable code tracing",
    ),
    cfg.StrOpt(
        "units",
        default="imperial",
        help="Units for display, imperial or metric",
    ),
]

tune_opts = [
    cfg.StrOpt(
        "web_ip",
        default="0.0.0.0",
        help="The ip address to listen on",
    ),
    cfg.PortOpt(
        "web_port",
        default=8001,
        help="The port to listen on",
    ),
    cfg.BoolOpt(
        "disable_url_request_logging",
        default=False,
        help="Disable the logging of url requests in the webchat command.",
    ),
]


def register_opts(config):
    config.register_opts(mltd_opts)
    config.register_group(tune_group)
    config.register_opts(tune_opts, group=tune_group)


def list_opts():
    return {
        "DEFAULT": (mltd_opts),
        tune_group.name: tune_opts,
    }
