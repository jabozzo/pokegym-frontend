#! /usr/bin/env python

import argparse

import flask
import flask_restful as rest

import config
import backendlib as lib


DESCRIPTION = """
Start the PokeGym backend.
"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("files", nargs='*', default=[],
        help= "Path to an arrival FILE.",  metavar="FILE")
    args = parser.parse_args()

    queue = lib.PokemonQueue()
    app = flask.Flask(__name__)

    if len(args.files) > 0:
        from parsing import Parser
        arrivals = []
        for file_ in args.files:
            arrivals.append(lib.AsyncEnqueue(queue, Parser.parse(file_)))

        for thread in arrivals:
            thread.start()

    else:
        queue.recieve_batch()

    api = rest.Api(app)
    api.add_resource(lib.LastQueue, '/last', resource_class_args=(queue,))
    app.run(host=config.HOST, port=str(config.PORT))

    exit()
