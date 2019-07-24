
from __future__ import division

from  numbers import Number

from newbinds import NewBinds

ifNumber = lambda f, other: f() if isinstance(other, Number) else NotImplemented

def make_ops():
    binder = NewBinds(locals())

    def __mul__(self, other):
        return ifNumber(lambda: type(self)(*[i*other for i in self]), other)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return ifNumber(lambda: type(self)(*[i/other for i in self]), other)

    __div__ = __truediv__

    def __mod__(self, other):
        return ifNumber(lambda: type(self)(*[i%other for i in self]), other)

    def __rmod__(self, other):
        return ifNumber(lambda: type(self)(*[other%i for i in self]), other)

    def __pow__(self, other, modulus=None):
        return ifNumber(lambda: type(self)(*[pow(i, other, modulus) for i in self]), other)

    def __rpow__(self, other):
        return ifNumber(lambda: type(self)(*[pow(other, i) for i in self]), other)

    return binder(locals())
