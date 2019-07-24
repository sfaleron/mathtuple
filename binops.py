
# First arguments must be mathtuples

def dot(tup1, tup2):
    return tup1.dot(tup2)

def cross(tup1, tup2):
    if tup1.length != 3:
        raise TypeError('Cross products are only supported for mathtuple types of length three')

    return tup1.cross(tup2)

def dist(tup1, tup2):
    return tup1.dist(tup2)
