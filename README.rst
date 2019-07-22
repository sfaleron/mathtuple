
Supported arithmetic:

- add and subtract by iterables of equal length (or reversed)
- p by types registered as a subclass of Number
- unary negation
- unary plus (returns a copy)

Additionally:

- dot product
- cross product (if size equals three)
- distance to another point

Works very much like numpy for these operations, without the bulk. Distinctions (may not be exhaustive):

- Length mismatches are a ValueError in numpy, but a TypeError here.
- Some reverse operations are handled that numpy doesn't support.

----


----

Depends on NewBinds
