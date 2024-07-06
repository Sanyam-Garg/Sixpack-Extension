from .models import Experiment, Alternative, Client
from .config import CONFIG as cfg

def create(experiment, alternatives, segmentation_rules,
    traffic_fraction=None,
    redis=None):

    try:
        existing_exp = Experiment.find(experiment, redis=redis)
    except ValueError:
        exp = Experiment.create(experiment, alternatives, segmentation_rules, traffic_fraction, redis=redis)
        return exp
    if existing_exp is not None:
        raise ValueError(f"experiment with name {experiment} already exists.")

def participate(experiment, alternatives, client_id,
    force=None,
    record_force=False,
    prefetch=False,
    datetime=None,
    redis=None,
    request=None):

    # exp = Experiment.find_or_create(experiment, alternatives, traffic_fraction=traffic_fraction, redis=redis)
    exp = Experiment.find(experiment, redis=redis)

    alt = None
    # if force and force in alternatives:
    #     alt = Alternative(force, exp, redis=redis)

    #     if record_force:
    #         client = Client(client_id, redis=redis)
    #         alt.record_participation(client, datetime)

    if not cfg.get('enabled', True):
        alt = exp.control
    elif exp.winner is not None:
        alt = exp.winner
    else:
        client = Client(client_id, redis=redis)
        alt = exp.get_alternative(client, dt=datetime, prefetch=prefetch, request=request)

    return alt


def convert(experiment, client_id,
    kpi=None,
    datetime=None,
    redis=None):

    exp = Experiment.find(experiment, redis=redis)

    if cfg.get('enabled', True):
        client = Client(client_id, redis=redis)
        alt = exp.convert(client, dt=datetime, kpi=kpi)
    else:
        alt = exp.control

    return alt
