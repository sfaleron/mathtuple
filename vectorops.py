
from  __future__ import division

from collections import Iterable, Sized
from   six.moves import zip as izip
from   itertools import islice
from     numbers import Number
from        math import sqrt

from    newbinds import NewBinds


def validate(otherIn, mathTuple):
    if isinstance(otherIn, Sized):
        otherOut = otherIn
    else:
        if isinstance(otherIn, Iterable):
            otherOut = islice(otherIn, mathTuple.length+1)
        else:
            return NotImplemented

    return type(mathTuple)(*otherOut)


def make_ops():
    binder = NewBinds(locals())

    def __sub__(self, otherIn):
        otherOut = validate(otherIn, self)

        return ( NotImplemented if otherOut is NotImplemented
            else type(self)(*[i-j for i,j in izip(self, otherOut)]) )

    def __rsub__(self, otherIn):
        otherOut = validate(otherIn, self)

        return ( NotImplemented if otherOut is NotImplemented
            else type(self)(*[j-i for i,j in izip(self, otherOut)]) )

    def __add__(self, otherIn):
        otherOut = validate(otherIn, self)

        return ( NotImplemented if otherOut is NotImplemented
            else type(self)(*[i+j for i,j in izip(self, otherOut)]) )

    __radd__ = __add__

    def dist(self, otherIn):
        otherOut = validate(otherIn, self)

        return ( NotImplemented if otherOut is NotImplemented
            else sqrt(sum([(i-j)**2 for i,j in izip(self, otherOut)])) )

    def dot(self, otherIn):
        otherOut = validate(otherIn, self)

        return ( NotImplemented if otherOut is NotImplemented
            else sum([i*j for i,j in izip(self, otherOut)]) )

    def cross(self, otherIn):
        otherOut = validate(otherIn, self)

        return ( NotImplemented if otherOut is NotImplemented
            else type(self)(
                self.y*otherOut.z - self.z*otherOut.y,
                self.z*otherOut.x - self.x*otherOut.z,
                self.x*otherOut.y - self.y*otherOut.x) )

    return binder(locals())
