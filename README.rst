
A pure-python point/vector type factory. Classes inherit from a `namedtuple`_
type. Any non-negative length is allowed, although the cross product is only
defined for two length-3 instances. Supports Python2 and Python3.

Aims to be lightweight and light-duty (plus a bit). If more features or
performance are desired, consider `numpy`_ or `scipy`_.

Supported arithmetic (reverse operations are also defined):

- Addition and subtraction by iterables of equal length
- Multiplication, division ("true" and floor), modulus, and powers by scalars
- Unary negative
- Unary positive

- An element-wise representation is provided for operations that normally
  have a scalar other-operand: multiplication, division, modulus, and powers.

Additionally:

- Dot product
- Cross product (if length equals three)
- Distance to another point
- Magnitude/norm
- Normalization to unit length

All binary operations and arithmetical methods are available as functions,
in the manner of the operations module.

Works very much like numpy for these operations, without the bulk.
Distinctions (may not be exhaustive):

- Length mismatches are a ValueError in numpy, but a TypeError here.
- Some reverse operations are handled that numpy doesn't support.

  + Of course, these can be somewhat dubious in utility. Anybody want to
    take the modulus of a scalar by a vector? It's here if you want it!

Tests are not thorough at this time. Use with caution!

----

Depends on `NewBinds`_ and `six`_

.. _NewBinds: https://github.com/sfaleron/NewBinds
.. _six: https://pypi.org/project/six/

.. _namedtuple: https://docs.python.org/library/collections.html#collections.namedtuple

.. _numpy: https://numpy.org/
.. _scipy: https://scipy.org/
