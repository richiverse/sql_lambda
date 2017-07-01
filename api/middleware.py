#! /usr/bin/env python2
import urllib

from flask import url_for

def list_routes(app):
    output = []
    for rule in app.url_map.iter_rules():

        if rule.endpoint == 'static':
            continue

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule for rule in rule.methods if rule not in ('OPTIONS','HEAD'))
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:7s}{:40s}{}".format(methods, url, rule.endpoint))
        output.append(line)

    return [line for line in sorted(output)]



