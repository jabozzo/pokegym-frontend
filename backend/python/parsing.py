#! /usr/bin/env python

import parsec as psc


class Parser(object):
    """
    A collection of methods to parse arrival time files.
    """

    @staticmethod
    def int_number():
        return psc.regex('-?(0|[1-9][0-9]*)').parsecmap(int)

    @staticmethod
    def time_parser():
        return Parser.int_number()

    @staticmethod
    def id_parser():
        return Parser.int_number()

    @staticmethod
    def range_parser():
        return (Parser.id_parser() << psc.string('-')) + Parser.id_parser()

    @staticmethod
    def tokenize(p):
        return p << psc.many1(psc.string(' '))

    @staticmethod
    def row_element():
        return Parser.range_parser() ^ Parser.id_parser()

    @staticmethod
    def row():
        return (  Parser.tokenize(Parser.time_parser())
                + psc.sepBy(Parser.row_element(), psc.many1(psc.string(' '))) )

    @staticmethod
    def file():
        return psc.sepEndBy(Parser.row(), psc.string('\n'))

    @staticmethod
    def parse(filename):
        """
        Opens a file an returns a list of arrival times. Each arrival time is a
        time-ids tuple, with ids being a list.
        """
        with open(filename, 'r') as f:
            data = f.read()

        data = Parser.file().parse(data)

        def to_list(tail):
            result = [[t] if isinstance(t, int) else list(range(*t)) for t in tail]
            result = [r for res in result for r in res]
            return result

        data = [(head, to_list(tail),) for head, tail in data]
        data = sorted(data, key=lambda x: x[0])

        return data
