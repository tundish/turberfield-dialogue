#!/usr/bin/env python3
# encoding: utf-8

import bisect
from collections.abc import Mapping
import numbers


class Matcher:

    @staticmethod
    def flatten_mapping(obj, path=[]):
        leaves = {k: v for k, v in obj.items() if not isinstance(v, Mapping)}
        children = {k: v for k, v in obj.items() if k not in leaves}
        for k, v in children.items():
            yield from Matcher.flatten_mapping(v, path=path[:] + [k])

        yield from (
            (tuple(path + [k]), Matcher.simplify(getattr(v, "value", v)))
            for k, v in leaves.items()
        )

    @staticmethod
    def mapping_key(obj):
        return sorted(list(Matcher.flatten_mapping(obj)))

    @staticmethod
    def simplify(val):
        if val is None:
            return ""
        elif isinstance(val, numbers.Complex):
            return str(abs(val))
        elif isinstance(val, numbers.Number):
            return str(val)
        else:
            return val

    def __init__(self, folders=None):
        self.folders = sorted(folders or [], key=lambda x: self.mapping_key(x.metadata))
        self.keys = sorted([self.mapping_key(i.metadata) for i in self.folders] ) 
    def options(self, data):
        if self.mapping_key(data) in self.keys:
            yield next(i for i in self.folders if i.metadata == data)
        else:
            index = bisect.bisect_left(self.keys, self.mapping_key(data))
            posns = sorted(set([max(0, index - 1), index]))
            yield from (self.folders[i] for i in posns)
