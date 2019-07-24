
A pure-python point/vector type factory. Classes inherit from a namedtuple
type. Any non-negative length is allowed, although the cross product is only
defined for two length-3 instances. Supports Python2 and Python3.

Aims to be lightweight and light-duty (plus a bit). If more features or
performance are desired, consider numpy or scipy.

Supported arithmetic (reverse operations are also defined):

- Addition and subtraction by iterables of equal length
- Multiplication, division, modulus, and powers by scalars

  + Division, true and floor, is supported

- Unary negative
- Unary positive

- An element-wise representation is provided for multiplication, division,
  modulus, and powers.

Explicit methods for binary operations are provided, named in the manner of
the operator module. mul(),

Additionally:

- Dot product
- Cross product (if size equals three)
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
    take the modulus of a scalar by a vector? It's there if you want it!

----

Depends on NewBinds and six
