
from __future__ import absolute_import
from __future__ import division

from  six.moves import zip as izip

from   newbinds import NewBinds

from .vectorops import validate


def make_elementwise(inst):
    cls    = type(inst)

    binder = NewBinds(locals())

    __slots__ = ()

    def unew(self):
        return cls(*self)

    def __mul__(self, otherIn):
        otherOut = validate(otherIn, self)

        return ( NotImplemented if otherOut is NotImplemented
            else cls(*[i*j for i,j in izip(self, otherOut)]) )

    __rmul__ = __mul__

    def __truediv__(self, otherIn):
        otherOut = validate(otherIn, self)

        return ( NotImplemented if otherOut is NotImplemented
            else cls(*[i/j for i,j in izip(self, otherOut)]) )

    def __rtruediv__(self, otherIn):
        otherOut = validate(otherIn, self)

        return ( NotImplemented if otherOut is NotImplemented
            else cls(*[j/i for i,j in izip(self, otherOut)]) )

    __div__  =  __truediv__
    __rdiv__ = __rtruediv__

    def __floordiv__(self, otherIn):
        otherOut = validate(otherIn, self)

        return ( NotImplemented if otherOut is NotImplemented
            else cls(*[i//j for i,j in izip(self, otherOut)]) )

    def __rfloordiv__(self, otherIn):
        otherOut = validate(otherIn, self)

        return ( NotImplemented if otherOut is NotImplemented
            else cls(*[j//i for i,j in izip(self, otherOut)]) )

    def __mod__(self, otherIn):
        otherOut = validate(otherIn, self)

        return ( NotImplemented if otherOut is NotImplemented
            else cls(*[i%j for i,j in izip(self, otherOut)]) )

    def __rmod__(self, otherIn):
        otherOut = validate(otherIn, self)

        return ( NotImplemented if otherOut is NotImplemented
            else cls(*[j%i for i,j in izip(self, otherOut)]) )

    def __pow__(self, otherIn, modulus=None):
        otherOut = validate(otherIn, self)

        return ( NotImplemented if otherOut is NotImplemented
            else cls(*[pow(i, j, modulus) for i,j in izip(self, otherOut)]) )

    def __rpow__(self, otherIn):
        otherOut = validate(otherIn, self)

        return ( NotImplemented if otherOut is NotImplemented
            else cls(*[pow(j, i) for i,j in izip(self, otherOut)]) )

    return type('ew'+cls.__name__, (cls,), binder(locals()))(*inst)
