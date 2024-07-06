Sixpack-Extension
=======

**Note: This is an extension to the already existing sixpack server available [here](https://github.com/sixpack/sixpack).**

Sixpack is a framework to enable A/B testing across multiple programming languages. It does this by exposing a simple API for client libraries.  Client libraries can be written in virtually any language.

Sixpack has two main parts. The first, **Sixpack-server**, is responsible for responding to web requests.  The second, **Sixpack-web**, is a web dashboard for tracking and acting on your A/B tests.  Sixpack-web is optional.

Requirements
============

* Redis >= 2.6
* Python >= 3 (Tested in 3.12.6)

Getting Started
===============

To get going, create (or don't, but you really should) a new virtualenv for your Sixpack installation. Follow that up with ``pip install``:

    $ pip install -r requirements.txt


### Optional
    Next, create a Sixpack configuration . A configuration must be created for Sixpack to run. Here's the default::

        redis_port: 6379                            # Redis port
        redis_host: localhost                       # Redis host
        redis_prefix: sixpack                       # all Redis keys will be prefixed with this
        redis_db: 15                                # DB number in redis

        metrics: false                              # send metrics to StatsD (response times, # of calls, etc)?
        statsd_url: 'udp://localhost:8125/sixpack'  # StatsD url to connect to (used only when metrics: true)

        # The regex to match for robots
        robot_regex: $^|trivial|facebook|MetaURI|butterfly|google|amazon|goldfire|sleuth|xenu|msnbot|SiteUptime|Slurp|WordPress|ZIBB|ZyBorg|pingdom|bot|yahoo|slurp|java|fetch|spider|url|crawl|oneriot|abby|commentreader|twiceler
        ignored_ip_addresses: []                    # List of IP

        asset_path: gen                             # Path for compressed assets to live. This path is RELATIVE to sixpack/static
        secret_key: '<your secret key here>'        # Random key (any string is valid, required for sixpack-web to run)

    You can store this file anywhere (we recommend ``/etc/sixpack/config.yml``). As long as Redis is running, you can now start the Sixpack server like this::

        $ SIXPACK_CONFIG=<path to config.yml> sixpack

    Sixpack-server will be listening on port 5000 by default but can be changed with the ``SIXPACK_PORT`` environment variable. For use in a production environment, please see the "Production Notes" section below.

Alternatively, as of version 1.1, all Sixpack configuration can be set by environment variables. The following environment variables are available:

* ``SIXPACK_CONFIG_ENABLED``
* ``SIXPACK_CONFIG_REDIS_PORT``
* ``SIXPACK_CONFIG_REDIS_HOST``
* ``SIXPACK_CONFIG_REDIS_PASSWORD``
* ``SIXPACK_CONFIG_REDIS_PREFIX``
* ``SIXPACK_CONFIG_REDIS_DB``
* ``SIXPACK_CONFIG_ROBOT_REGEX``
* ``SIXPACK_CONFIG_IGNORE_IPS`` - comma separated
* ``SIXPACK_CONFIG_ASSET_PATH``
* ``SIXPACK_CONFIG_SECRET``
* ``SIXPACK_CORS_ORIGIN``
* ``SIXPACK_CORS_HEADERS``
* ``SIXPACK_CORS_CREDENTIALS``
* ``SIXPACK_CORS_METHODS``
* ``SIXPACK_CORS_EXPOSE_HEADERS``
* ``SIXPACK_METRICS``
* ``STATSD_URL``

Using the API
=============

All interaction with Sixpack is done via ``HTTP GET`` requests. Sixpack allows for cross-language testing by accepting a unique ``client_id`` (which the client is responsible for generating) that links a participation to a conversion. All requests to Sixpack require a ``client_id``.

The Sixpack API can be used from front-end Javascript via CORS-enabled requests. The Sixpack API server will accept CORS requests from any domain.


Creating an Experiment
------------------------------
You can create an experiment with a `POST` request to the `create-experiment` endpoint:

    $ curl http://localhost:5000/create-experiment

with a json request body something like this:
```json
{
    "name": "test",
    "alternatives": {
        "variantA": [
            ["/html/body/h1", "innerHTML", "Heading A"],
            ["/html/body/img", "src", "https://img.freepik.com/free-vector/letter-brush-stroke-typography-vector_53876-175299.jpg"]
        ],
        "variantB": [
            ["/html/body/h1", "innerHTML", "Heading B"],
            ["/html/body/img", "src", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLs6Mavwc2pTrEqhYNqPg561fO4kGTsPgbzQ&s"]
        ]
    },
    "segmentation_rules": [
        ["user-agent", ["safari"], ["chrome"]]
    ]
}
```

``traffic_fraction`` (optional) Sixpack allows for limiting experiments to a subset of traffic. You can pass the percentage of traffic you'd like to expose the test to as a decimal number here. (``?traffic_fraction=0.10`` for 10%)

Here you can specify the 2 alternatives for your A/B test. The keys `variantA` and `variantB` can have any names of your choice, and the values associated with them contain the rules for changing the HTML elements via a client side script. <br>
Each variant has a 2D array, where each 1D array has 3 elements:

* `[0] xpath` --> This denotes the xpath of the HTML element.
* `[1] property` --> This denotes the property of the above element to be modified. If `property == innerHTML`, then the content of the element is changed. Else, the property is treated as an attribute like `src`, etc.   
* `[2] value` --> The desired value of the property for the selected element.


In addition to this, you can also optionally specify the audience segmentation rules for splitting the variants across your audience. <br> 
> Note: If you do not specify any segmentation rules, the audience will be split randomly in a ratio of 50:50.

If you do want to specify the rules, you can do so in the following format: <br>
```json
"segmentation_rules": [
        ["user-agent", ["safari", "firefox"], ["chrome"]],
        ["location", ["india"], ["europe", "japan"]],
        ["random", 30, 70]
    ]
```
The format is very similar to that of alternatives.<br>
* `[0]` --> This denotes the **class** of the audience segmenter. Currently supported segmenter classes can be found in [segmenters.py](https://github.com/Sanyam-Garg/Sixpack-Extension/blob/master/sixpack/segmenters.py)
* `[1]` --> These correspond to the audiences who will be shown the first variant. This can be a list in case of for example `user-agent`, and can be an integer in case of `random`.
* `[2]` --> These correspond to the audiences who will be shown the second variant.

When you specify multiple segmentation rules, the first rule in the list is assigned the topmost priority, while the last rule in the list has the least priority. When segmenting the audience, the lower priority rules are then used as fallbacks in case the outcome is indecisive for a higher priority rule.

**Note: The `random` class rule is the last fallback rule. So make sure to define it at the end of your rule list. If you do not define it, a 50:50 random rule will be applied as the last fallback**

### Response
```json
{
    "name": "test",
    "alternatives": {
        "variantA": [
            [
                "/html/body/h1",
                "innerHTML",
                "Heading A"
            ],
            [
                "/html/body/img",
                "src",
                "https://img.freepik.com/free-vector/letter-brush-stroke-typography-vector_53876-175299.jpg"
            ]
        ],
        "variantB": [
            [
                "/html/body/h1",
                "innerHTML",
                "Heading B"
            ],
            [
                "/html/body/img",
                "src",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLs6Mavwc2pTrEqhYNqPg561fO4kGTsPgbzQ&s"
            ]
        ]
    },
    "segmentation_rules": [
        [
            "user-agent",
            [
                "safari"
            ],
            [
                "chrome"
            ]
        ]
    ],
    "created_at": "2024-07-06 17:45",
    "traffic_fraction": 1.0,
    "excluded_clients": 0,
    "total_participants": 0,
    "total_conversions": 0,
    "description": null,
    "winner": "",
    "is_archived": false,
    "is_paused": false,
    "status": "ok"
}
```

Participating in an Experiment
------------------------------

You can participate in an experiment with a ``GET`` request to the ``participate`` endpoint::

    $ curl http://localhost:5000/participate?experiment=test&client_id=12345678-1234-5678-1234-567812345678


``experiment`` (required) is the name of the test.

``client_id`` (required) is the unique id for the user participating in the test.


Response
--------

A typical Sixpack participation response will look something like this:
```json
{
    "alternative": {
        "variantA": [
            [
                "/html/body/h1",
                "innerHTML",
                "Heading A"
            ],
            [
                "/html/body/img",
                "src",
                "https://img.freepik.com/free-vector/letter-brush-stroke-typography-vector_53876-175299.jpg"
            ]
        ]
    },
    "experiment": {
        "name": "test"
    },
    "client_id": "abcd",
    "status": "ok"
}
```

The most interesting part of this is ``alternative``. This is a representation of the alternative that was chosen for the test and assigned to a ``client_id``. All subsequent requests to this experiment/client_id combination will be returned the same alternative.

> You can check out the files in the `example` folder in the root of the repository to see how this might be used to modify the elements at the frontend.

<!-- Converting a user
-----------------

You can convert a user with a ``GET`` request to the ``convert`` endpoint::

    $ curl http://localhost:5000/convert?experiment=button_color&client_id=12345678-1234-5678-1234-567812345678

Conversion Arguments
--------------------

- ``experiment`` (required) the name of the experiment you would like to convert on.
- ``client_id`` (required) the client you would like to convert.
- ``kpi`` (optional) sixpack supports recording multiple KPIs. If you would like to track conversion against a specfic KPI, you can do that here. If the KPI does not exist, it will be created automatically. -->

Notes
-----

We've included a 'health-check' endpoint, available at ``/_status``. This is helpful for monitoring and alerting if the Sixpack service becomes unavailable. The health check will respond with either 200 (success) or 500 (failure) headers.

CORS
====

Cross-origin resource sharing can be adjusted with the following config attributes::

    cors_origin: *
    cors_headers: ...
    cors_credentials: true
    cors_methods: GET
    cors_expose_headers: ...

License
=======

Sixpack-Extension is released under the
`BSD 2-Clause License`: http://opensource.org/licenses/BSD-2-Clause

Disclaimer
========
Some of the features of `sixpack` have not been updated in this repository. You can checkout the original repository for more information on those features.