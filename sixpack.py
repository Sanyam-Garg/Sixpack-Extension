#!/usr/bin/env python

import os, random
import sys

from werkzeug.serving import run_simple
from sixpack.server import create_app

sys.path.append("..")

port = int(os.environ.get('SIXPACK_PORT', 5000))
debug = 'SIXPACK_DEBUG' in os.environ
RANDOM_SEED = int.from_bytes(os.urandom(32))
random.seed(RANDOM_SEED)

app = create_app()
run_simple('0.0.0.0', port, app, use_debugger=debug, use_reloader=debug)
