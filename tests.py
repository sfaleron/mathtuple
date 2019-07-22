from mathtuple import mathtuple

def test_construction():
    Point = mathtuple('Point', 2)
    assert(Point._fields == ('x','y'))

    Point = mathtuple('Point', 3)
    assert(Point._fields == ('x','y','z'))

    Point = mathtuple('Point', 4)
    assert(Point._fields == ('w','x','y','z'))

def test_numpy():
    from numpy import array
    a=array([2,4,6])
    Triple = mathtuple('Triple',3)
    b=Triple(2,4,6)

    # intended to be done interactively in interpreter.
    # some translation is pending.

    a
    b

    a*5
    b*5
    5*a
    5*b

    a/2
    b/2

    5*b+a
    5*a+b

    +a is a
    +b is b

    a/2+range(3)
    b/2+range(3)

    a/2+range(2)
    b/2+range(2)

    a/2+range(4)
    b/2+range(4)
