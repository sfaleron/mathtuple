
from  __future__ import absolute_import
from  __future__ import division

from collections import namedtuple, Iterable, Sized
from     numbers import Number, Integral
from      string import ascii_lowercase
from   six.moves import zip as izip
from   itertools import islice
from        math import sqrt
import       six

from    newbinds import NewBinds

from           . import scalarops, vectorops
from           . import elementwise as _ew


_mathtuple_signature = object()

_aliases = dict(
    dist = ['hypot'],
    norm = ['magnitude'],
    dot  = ['scalarprod'],
    cross= ['vectorprod'] )


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
            # if length >= 26, slice is the whole
            reifiedSyms  = ascii_lowercase[-length:]

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

    _ew        = []
    __slots__  = ()
    _length    = length

    _signature = _mathtuple_signature

    if six.PY2:
        def __repr__(self):
            return baseClass.__repr__(self)[1:]

    @property
    def ew(self):
        if not self._ew:
            self._ew.append(_ew.make_elementwise(self))

        return self._ew[0]

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

    def norm(self):
        return sqrt(sum([i*i for i in self]))

    __abs__ = norm

    def normalize(self):
        return self/self.norm()

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

    classBinds.update(scalarops.make_ops())
    classBinds.update(vectorops.make_ops(length))

    classBinds.update(length=property(lambda s: s._length))

    return type(className, (baseClass,), classBinds)
