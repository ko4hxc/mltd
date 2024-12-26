import datetime
import json
import logging
import math
import signal
import sys
import threading
import time

import click
import flask
from flask import request
from flask_httpauth import HTTPBasicAuth
from flask_socketio import Namespace, SocketIO
from geopy.distance import geodesic
from oslo_config import cfg
from werkzeug.security import check_password_hash, generate_password_hash
import wrapt

import mltd
from mltd import (
#    cli_helper, threads, utils,
    cli_helper, utils,
)
#from aprsd.client import client_factory, kiss
from mltd.main import cli
#from aprsd.threads import aprsd as aprsd_threads
#from aprsd.threads import keep_alive, rx, tx
from mltd.utils import trace

import subprocess
import yaml
 
def ticcmd(*args):
  return subprocess.check_output(['ticcmd'] + list(args))

CONF = cfg.CONF
LOG = logging.getLogger()
auth = HTTPBasicAuth()
users = {}
socketio = None



flask_app = flask.Flask(
    "mltd",
    static_url_path="/static",
    static_folder="web/tune/static",
    template_folder="web/tune/templates",
)


def signal_handler(sig, frame):

    click.echo("signal_handler: called")
    LOG.info(
        f"Ctrl+C, Sending all threads({len(threads.MLTDThreadList())}) exit! "
        f"Can take up to 10 seconds {datetime.datetime.now()}",
    )
    threads.MLTDThreadList().stop_all()
    if "subprocess" not in str(frame):
        time.sleep(1.5)
        stats.stats_collector.collect()
        LOG.info("Telling flask to bail.")
        signal.signal(signal.SIGTERM, sys.exit(0))



# HTTPBasicAuth doesn't work on a class method.
# This has to be out here.  Rely on the APRSDFlask
# class to initialize the users from the config
@auth.verify_password
def verify_password(username, password):
    global users

    if username in users and check_password_hash(users[username], password):
        return username




def set_config():
    global users


def _get_transport(stats):
    if CONF.aprs_network.enabled:
        transport = "aprs-is"
        aprs_connection = (
            "APRS-IS Server: <a href='http://status.aprs2.net' >"
            "{}</a>".format(stats["APRSClientStats"]["server_string"])
        )
    elif kiss.KISSClient.is_enabled():
        transport = kiss.KISSClient.transport()
        if transport == client.TRANSPORT_TCPKISS:
            aprs_connection = (
                "TCPKISS://{}:{}".format(
                    CONF.kiss_tcp.host,
                    CONF.kiss_tcp.port,
                )
            )
        elif transport == client.TRANSPORT_SERIALKISS:
            # for pep8 violation
            aprs_connection = (
                "SerialKISS://{}@{} baud".format(
                    CONF.kiss_serial.device,
                    CONF.kiss_serial.baudrate,
                ),
            )
    elif CONF.fake_client.enabled:
        transport = client.TRANSPORT_FAKE
        aprs_connection = "Fake Client"

    return transport, aprs_connection

class CtlStepNamespace(Namespace):
    """Class to handle the socketio interactions."""
    got_ack = False
    reply_sent = False
    msg = None
    request = None

    def __init__(self, namespace=None, config=None):
        super().__init__(namespace)

    def on_connect(self):
        global socketio
        LOG.info("Web socket connected")
        socketio.emit(
            "connected", {"data": "/ctlstep Connected"},
            namespace="/ctlstep",
        )

    def on_disconnect(self):
        LOG.debug("WS Disconnected")

    def on_send(self, data):
        global socketio
        LOG.info(f"WS: on_send {data}")
        self.request = data
        
        new_target = int(data['steps']) if data['cmd']=='UP' else -int(data['steps'])
        LOG.info("Setting target position to {}.".format(new_target))
        #ticcmd('--resume', '--position-relative', str(new_target))

    def on_deeng(self, data):
        global socketio
        LOG.info(f"WS: on_deeng {data}")
        self.request = data
        #ticcmd('--deenergize')

    def handle_message(self, data):
        LOG.debug(f"WS Data {data}")

    def handle_json(self, data):
        LOG.debug(f"WS json {data}")


@auth.login_required
@flask_app.route("/")
def index():
#    stats = _stats()

    # For development
    html_template = "index.html"
    LOG.debug(f"Template {html_template}")

#    transport, aprs_connection = _get_transport(stats["stats"])
#    LOG.debug(f"transport {transport} aprs_connection {aprs_connection}")

#    stats["transport"] = transport
#    stats["aprs_connection"] = aprs_connection
#    LOG.debug(f"initial stats = {stats}")

    return flask.render_template(
        html_template,
        callsign=CONF.callsign,
        version=mltd.__version__,
    )


@trace.trace
def init_flask(loglevel, quiet):
    global socketio, flask_app

    socketio = SocketIO(
        flask_app, logger=False, engineio_logger=False,
        async_mode="threading",
    )
    socketio.on_namespace(
        CtlStepNamespace(
            "/ctlstep",
        ),
   )
    return socketio


# main() ###
@cli.command()
@cli_helper.add_options(cli_helper.common_options)
@click.option(
    "-f",
    "--flush",
    "flush",
    is_flag=True,
    show_default=True,
    default=False,
    help="Flush out all old aged messages on disk.",
)
@click.option(
    "-p",
    "--port",
    "port",
    show_default=True,
    default=None,
    help="Port to listen to web requests.  This overrides the config.webchat.web_port setting.",
)
@click.pass_context
@cli_helper.process_standard_options
def tune(ctx, flush, port):
    """Web based HAM Radio tuninnng program!"""
    loglevel = ctx.obj["loglevel"]
    quiet = ctx.obj["quiet"]

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    level, msg = utils._check_version()
    if level:
        LOG.warning(msg)
    else:
        LOG.info(msg)
    LOG.info(f"mltd Started version: {mltd.__version__}")

    CONF.log_opt_values(logging.getLogger(), logging.DEBUG)
    if not port:
        port = CONF.tune.web_port


#    keepalive = keep_alive.KeepAliveThread()
#    LOG.info("Start KeepAliveThread")
#    keepalive.start()

    socketio = init_flask(loglevel, quiet)
    #rx_thread = rx.APRSDPluginRXThread(
    #    packet_queue=threads.packet_queue,
    #)
    #rx_thread.start()
    #process_thread = WebChatProcessPacketThread(
    #   packet_queue=threads.packet_queue,
    #    socketio=socketio,
    #)
    #process_thread.start()

    LOG.info("Start socketio.run()")
    socketio.run(
        flask_app,
        # This is broken for now after removing cryptography
        # and pyopenssl
        # ssl_context="adhoc",
        host=CONF.tune.web_ip,
        port=port,
        allow_unsafe_werkzeug=True,
    )

    LOG.info("SaT exiting!!!!  Bye.")
