
from  __future__ import division

def unexpression_adder(appendable=None):
    if appendable is None:
        appendable = []
    def dec(unexpression):
        appendable.append(unexpression.__name__)
        return unexpression

    return appendable, dec

__all__, adder = unexpression_adder()


from collections import namedtuple, Sized
from     numbers import Number, Integral
from      string import ascii_lowercase
from   six.moves import zip as izip
from   itertools import islice

from    newbinds import NewBinds

@adder
def mathtuple(className, size, positionNames=True):

    if not (size > 0 and isinstance(size, Integral)):
        raise ValueError('"size" must be an integer greater than or equal to one')

    fmtStr = '_{{:0{:d}}}'.format(len(str(size-1)))

    if   positionNames is True:
        if   size <=  3:
            reifiedSyms = 'xyz'[:size]
        else:
            #  if size >= 26, slice is the whole
            reifiedSyms = ascii_lowercase[-size:]

        reifiedNames = tuple(reifiedSyms)

    elif positionNames is False:
        reifiedNames = ()

    else:
        reifiedNames = tuple(islice(positionNames, size))

    reifiedSize  = len(reifiedNames)

    if reifiedSize < size:
        padIds = []
        for i in range(reifiedSize, size):
            padId = fmtStr.format(i)
            while padId in reifiedNames:
                padId += '_'

            padIds.append(padId)

        reifiedNames = reifiedNames + tuple(padIds)

    baseClass = namedtuple('_' + className, reifiedNames)

    binder = NewBinds(locals())

    _size  = size

    def __new__(cls, *seq):
        if len(seq) != size:
            raise TypeError('Size mismatch')
        for i,j in izip(seq, cls._fields):
            if not isinstance(i, Number):
                raise TypeError(j+' is not a Number')

        return baseClass.__new__(cls, *seq)

    def copy(self):
        return type(self)(*self)

    __pos__ = copy

    def __neg__(self):
        return -1*self

    def __mul__(self, other):
        cls = type(self)

        if isinstance(other, Number):
            return cls(*[i*other for i in self])
        else:
            return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other):
        cls = type(self)

        if isinstance(other, Number):
            return cls(*[i/other for i in self])
        else:
            return NotImplemented

    __div__ = __truediv__

    @staticmethod
    def _validate(otherIn):
        if isinstance(otherIn, Sized):
            otherOut = otherIn
        else:
            if isinstance(otherIn, Iterable):
                otherOut = tuple(islice(otherIn, size+1))
            else:
                return NotImplemented

        if len(otherOut) != size:
            raise TypeError('Sizes do not match')

        return otherOut

    def __sub__(self, otherIn):
        cls      = type(self)
        otherOut = self._validate(otherIn)

        if otherOut is NotImplemented:
            return NotImplemented
        else:
            return cls(*[i-j for i,j in izip(self, otherOut)])

    def __add__(self, otherIn):
        cls = type(self)

        otherOut = self._validate(otherIn)

        return ( NotImplemented if otherOut is NotImplemented else
            cls(*[i+j for i,j in izip(self, otherOut)]) )

    def dist(self, otherIn):
        otherOut = self._validate(otherIn)

        return ( NotImplemented if otherOut is NotImplemented else
            (sum([(i-j)**2 for i,j in izip(self, otherOut)]))**.5 )

    hypot = dist

    def dot(self, other):
        otherOut = self._validate(otherIn)

        return ( NotImplemented if otherOut is NotImplemented else
            sum([i*j for i,j in izip(self, otherOut)]) )

    def cross(self, other):
        cls = type(self)

        otherOut = self._validate(otherIn)
        if otherOut is NotImplemented:
            return NotImplemented
        else:
            ox, oy, oz = otherOut
            return cls(
                self.y*oz - self.z*oy,
                self.z*ox - self.x*oz,
                self.x*oy - self.y*ox)

    @classmethod
    def from_any(cls, *seq):
        """Pass any number of sequences or iterators, of the
        correct length; returns an iterator that returns
        instances of the type."""

        return cls.from_iter(seq)

    @classmethod
    def from_iter(cls, it):
        """Pass an iterable of sequences or iterators, of the
        correct length; returns an iterator that returns
        instances of the type."""

        return (e if isinstance(e, cls) else cls(*e) for e in it)

    classBinds = binder(locals())
    classBinds.update(size=property(lambda s: s._size))

    return type(className, (baseClass,), classBinds)

# First arguments must be mathtuples

@adder
def dot(tup1, tup2):
    return tup1.dot(tup2)

@adder
def cross(tup1, tup2):
    if tup1.size != 3:
        raise TypeError('Cross products are only supported for mathtuple types of length three')

    return tup1.cross(tup2)

@adder
def dist(tup1, tup2):
    return tup1.dist(tup2)

hypot = dist

__all__.append('hypot')
