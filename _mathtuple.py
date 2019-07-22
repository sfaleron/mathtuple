
from  __future__ import division

import six

def unexpression_adder(appendable=None):
    if appendable is None:
        appendable = []
    def dec(unexpression):
        appendable.append(unexpression.__name__)
        return unexpression

    return appendable, dec

__all__, adder = unexpression_adder()


from collections import namedtuple, Iterable, Sized
from     numbers import Number, Integral
from      string import ascii_lowercase
from   six.moves import zip as izip
from   itertools import islice

from    newbinds import NewBinds

def _make_elementwise(inst):
    binder = NewBinds(locals())

    __slots__ = ()

    def __mul__(self, otherIn):
        otherOut = self._validate(otherIn)

        if otherOut is NotImplemented:
            return NotImplemented
        else:
            return cls(*[i*j for i,j in izip(self, otherOut)])

    __rmul__ = __mul__

    def __div__(self, otherIn):
        otherOut = self._validate(otherIn)

        if otherOut is NotImplemented:
            return NotImplemented
        else:
            return cls(*[i/j for i,j in izip(self, otherOut)])

    def __rdiv__(self, otherIn):
        otherOut = self._validate(otherIn)

        if otherOut is NotImplemented:
            return NotImplemented
        else:
            return cls(*[j/i for i,j in izip(self, otherOut)])

    __div__ = __truediv__

    def __mod__(self, otherIn):
        otherOut = self._validate(otherIn)

        if otherOut is NotImplemented:
            return NotImplemented
        else:
            return cls(*[i%j for i,j in izip(self, otherOut)])

    def __rmod__(self, otherIn):
        otherOut = self._validate(otherIn)

        if otherOut is NotImplemented:
            return NotImplemented
        else:
            return cls(*[j%i for i,j in izip(self, otherOut)])

    def __pow__(self, otherIn, modulus=None):
        otherOut = self._validate(otherIn)

        if otherOut is NotImplemented:
            return NotImplemented
        else:
            return cls(*[pow(i, j, modulus) for i,j in izip(self, otherOut)])

    def __rpow__(self, otherIn):
        otherOut = self._validate(otherIn)

        if otherOut is NotImplemented:
            return NotImplemented
        else:
            return cls(*[pow(j, i) for i,j in izip(self, otherOut)])

    return type(className, (type(inst),), binder(locals()))(*inst)

@adder
def mathtuple(className, length, positionNames=True):
    """The constraints on `className` are the same as those on the first arguments
    of `namedtuple()` and `type()`.
    `length` is a non-negative integer.
    The position names are guaranteed to be sensibly set, if `positionNames` is
    either a boolean or an iterator that yields valid identifiers. Possible
    values:

    - If an iterator:

      + Short iterators are padded with generic identifiers
      + Long iterators are truncated to fit

    - If True (default):

      + If 1 <= length <=  3, then the identifiers are: `x`, `x,y`, or `x,y,z`.
      + If 4 <= length <= 26, then the trailing part of the lowercase alphabet is
        used.
      + If length > 26, the full alphabet is padded in the same manner as an
        explicit short iterator.

    - If False:

      + All positions are given generic identifiers

    Generic identifiers are an underscore followed with the index, zero-padded
    to the width of the highest index.

    If a short iterator is passed and it contains collisions with the generic
    identifiers, the generic identifier is extended by an underscore until a
    unique identifier is obtained."""

    if not (length >= 0 and isinstance(length, Integral)):
        raise ValueError('"length" must be a non-negative integer')

    fmtStr = '_{{:0{:d}}}'.format(len(str(length-1)))

    if   positionNames is True:
        if   length <=  3:
            reifiedSyms = 'xyz'[:length]
        else:
            #  if length >= 26, slice is the whole
            reifiedSyms = ascii_lowercase[-length:]

        reifiedNames = tuple(reifiedSyms)

    elif positionNames is False:
        reifiedNames = ()

    else:
        reifiedNames = tuple(islice(positionNames, length))

    reifiedLength  = len(reifiedNames)

    if reifiedLength < length:
        padIds = []
        for i in range(reifiedLength, length):
            padId = fmtStr.format(i)
            while padId in reifiedNames:
                padId += '_'

            padIds.append(padId)

        reifiedNames = reifiedNames + tuple(padIds)

    baseClass = namedtuple('_' + className, reifiedNames)

    binder = NewBinds(locals())

    _ew       = None
    _length   = length
    __slots__ = ()

    if six.PY2:
        def __repr__(self):
            return baseClass.__repr__(self)[1:]

    @property
    def ew(self):
        if self._ew is None:
            self._ew = _make_elementwise(self)

        return self._ew

    def __new__(cls, *seq):
        if len(seq) != length:
            raise TypeError('Length mismatch')

        for i,j in izip(seq, cls._fields):
            if not isinstance( i, Number):
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

    def __mod__(self, other):
        cls = type(self)

        if isinstance(other, Number):
            return cls(*[i%other for i in self])
        else:
            return NotImplemented

    def __pow__(self, other, modulus=None):
        cls = type(self)

        if isinstance(other, Number):
            return cls(*[pow(i, other, modulus) for i in self])
        else:
            return NotImplemented


    @staticmethod
    def _validate(otherIn):
        if isinstance(otherIn, Sized):
            otherOut = otherIn
        else:
            if isinstance(otherIn, Iterable):
                otherOut = tuple(islice(otherIn, length+1))
            else:
                return NotImplemented

        if len(otherOut) != length:
            raise TypeError('Lengths do not match')

        for i in otherOut:
            if not isinstance(i, Number):
                return NotImplemented

        return otherOut

    def __sub__(self, otherIn):
        cls      = type(self)
        otherOut = self._validate(otherIn)

        if otherOut is NotImplemented:
            return NotImplemented
        else:
            return cls(*[i-j for i,j in izip(self, otherOut)])

    def __rsub__(self, otherIn):
        cls      = type(self)
        otherOut = self._validate(otherIn)

        if otherOut is NotImplemented:
            return NotImplemented
        else:
            return cls(*[j-i for i,j in izip(self, otherOut)])

    def __add__(self, otherIn):
        cls = type(self)

        otherOut = self._validate(otherIn)

        return ( NotImplemented if otherOut is NotImplemented else
            cls(*[i+j for i,j in izip(self, otherOut)]) )

    __radd__ = __add__

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
    classBinds.update(length=property(lambda s: s._length))

    return type(className, (baseClass,), classBinds)

# First arguments must be mathtuples

@adder
def dot(tup1, tup2):
    return tup1.dot(tup2)

@adder
def cross(tup1, tup2):
    if tup1.length != 3:
        raise TypeError('Cross products are only supported for mathtuple types of length three')

    return tup1.cross(tup2)

@adder
def dist(tup1, tup2):
    return tup1.dist(tup2)

hypot = dist

__all__.append('hypot')
