#!/usr/bin/env python3
# encoding: utf-8

import bisect
from collections.abc import Mapping
import numbers


class Matcher:

    @staticmethod
    def flatten_mapping(obj, path=[]):
        leaves = {k: v for k, v in obj.items() if not isinstance(v, Mapping)}
        children = (k for k in obj if k not in leaves)
        for key in children:
            yield from Matcher.flatten_mapping(obj[key], path=path[:] + [key])

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
        if data in self.keys:
            yield next(i for i in self.folders if i.metadata == data)
        else:
            pos = bisect.bisect_left(self.keys, self.mapping_key(data))
            yield self.folders[pos]
