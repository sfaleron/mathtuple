
depends on NewBinds

# Supported arithmetic:
#   add/subtract by iterables of equal length
#   divide/multiply by types registered as a subclass of Number
#   unary negation is identical to multiplying by -1
#   unary plus returns a copy

# Works very much like numpy for these operations, without the bulk,
# although a size mismatch is a ValueError in numpy, but a TypeError here.

# The position names are guaranteed to be sensibly set, if passed either a
# boolean or an iterator that yields valid identifiers.

# If such an iterator is passed:
#   Long iterators are truncated
#   Short ones are padded with generic identifiers
# If True (default):
#   If 1 <= size <=  3, then the identifiers are: "x", "x,y", or "x,y,z".
#   If 4 <= size <= 26, then the trailing part of the lowercase alphabet is used.
#   if size > 26, the full alphabet is padded in the same manner as an explicit
#     short iterator.
# If False:
#   All positions are given generic identifiers

# Generic identifiers are an underscore followed with the index, zero-padded
# to the width of the highest index.

# If a short iterator is passed and it contains collisions with the generic
# identifiers, the generic identifier is extended by an underscore until a
# unique identifier is obtained.
