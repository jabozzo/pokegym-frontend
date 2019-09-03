#! /usr/bin/env python

import time
import sched
import threading

import requests
import flask
import flask_cors as cors
import flask_restful as rest

import config


class LastQueue(rest.Resource):
    """
    Get the limited queue
    """

    def __init__(self, queue):
        self.queue = queue

    @cors.cross_origin()
    def get(self):
        data = self.queue.get_last(config.MAX_POKEMON_DISPLAY)
        data = tuple({"id": id_, "name": name} for id_, name in data)
        return flask.jsonify(data)


class PokemonQueue(object):
    """
    This class tracks down the which pokemons are in queue for display.
    """

    def __init__(self):
        self._queue = []
        self._pokedex = None
        self._lock_queue = threading.Lock()
        self._lock_pokedex = threading.Lock()

    def get_last(self, length=None):
        """
        Gets a number of pokemon to display.
        """
        self._lock_queue.acquire()
        result = self._queue[slice(None, length)]
        self._lock_queue.release()
        self.second_elapsed()
        return result

    def get_pokedex(self):
        """
        Gets either the cached or the onine pokedex from the pokeapi.
        """
        if not config.CACHE_POKEDEX or self._pokedex is None:
            self._lock_pokedex.acquire()
            r = requests.get(config.POKEDEX_URL)
            if r.status_code == 200:
                pokedex = r.json()["pokemon_entries"]
                self._pokedex = tuple(
                    (poke["entry_number"], poke["pokemon_species"]["name"])
                    for poke in pokedex)
            self._lock_pokedex.release()

        return self._pokedex

    def clear_cache(self):
        """
        Forces the queue to update the pokedex the next time it is needed.
        """
        self._lock_pokedex.acquire()
        self._pokedex = None
        self._lock_pokedex.release()

    def second_elapsed(self):
        """
        Removes an element from the queue
        """
        self._lock_queue.acquire()
        try:
            if len(self._queue) > config.MIN_POKEMON_DISPLAY:
                self._queue.pop(0)
        except IndexError:
            pass
        self._lock_queue.release()

    def recieve_batch(self, ids=None):
        """
        Adds newely-arrived pokemon to the queue
        """
        pokedex = self.get_pokedex()
        if pokedex is not None:
            if ids is None:
                batch = pokedex
            else:
                ids = set(ids)
                batch = tuple(poke for poke in pokedex if poke[0] in ids)

            self._lock_queue.acquire()
            self._queue.extend(sorted(batch, key=lambda x: x[1]))
            self._lock_queue.release()


class AsyncEnqueue(threading.Thread):
    def __init__(self, queue, data, **kwargs):
        super().__init__(**kwargs)
        self._queue = queue
        self._data = data

    def run(self):
        scheduler = sched.scheduler(time.time, time.sleep)

        for delay, values in self._data:
            scheduler.enter(delay, 0, self._queue.recieve_batch,
                argument=(values,))

        scheduler.run()
