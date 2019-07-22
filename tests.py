from mathtuple import mathtuple

def test_construction():
    Point = mathtuple('Point', 2)
    assert(Point._fields == ('x', 'y'))

    Point = mathtuple('Point', 3)
    assert(Point._fields == ('x', 'y', 'z'))

    Point = mathtuple('Point', 4)
    assert(Point._fields == ('w', 'x', 'y', 'z'))

def make_iter(start=0, step=1):
    return (start+i*step for i in range(3))

def test_numpy():
    from numpy import array
    Triple = mathtuple('Triple', 3)

    a = array([2,4,6])
    b = Triple(2,4,6)
    c = Triple(*range(3))
    d = (-1,-2,-3)

    # intended to be done interactively in the interpreter.
    # some translation is pending.

    print(a)
    print(b)

    print(a*5)
    print(b*5)
    print(5*a)
    print(5*b)

    print(a/2)
    print(b/2)

    print(d-a)
    print(d-b)
    #print(make_iter()-a)
    print(make_iter()-b)

    print(5*b+a)
    print(5*a+b)

    print(+a is a)
    print(+b is b)

    print(a/2+range(3))
    print(b/2+range(3))

    #print(a/2+range(2))
    #print(b/2+range(2))

    #print(a/2+range(4))
    #print(b/2+range(4))

if __name__ == '__main__':
    test_construction()
    test_numpy()
