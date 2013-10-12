import numpy
from cone import conelp


class LinearProgram:
    class __LinearBound:
        def __init__(self, A):
            n = numpy.shape(A)[0]
            self.lower = numpy.empty(n)
            self.upper = numpy.empty(n)
            self.lower.fill(-numpy.inf)
            self.upper.fill(+numpy.inf)
            self.__mat = A

        def getCVX(self):
            assert len(self.upper) == self.__mat.shape[0], "Inconsistent length for upper bound here"
            assert len(self.lower) == self.__mat.shape[0], "Inconsistent length for lower bound here"

            for (l, u) in zip(self.lower, self.upper):
                assert l <= u, "Lower bound larger than upper bound"

            h = numpy.concatenate([self.upper, -self.lower])
            A = numpy.vstack([self.__mat, -self.__mat])

            A = A[~numpy.isinf(h)]
            h = h[~numpy.isinf(h)]
            return {'mat': A, 'vec': h}

        def eval(self, x):
            return numpy.dot(self.__mat, x)

    def __init__(self, c, A):
        self.c = c
        self.bx = self.__LinearBound(numpy.eye(len(c), len(c)))
        self.bc = self.__LinearBound(A)

    def solve(self):
        bx = self.bx.getCVX()
        bc = self.bc.getCVX()

        X = conelp(self.c)
        X.aux.pushLinConstraint(bx['mat'], bx['vec'])
        X.aux.pushLinConstraint(bc['mat'], bc['vec'])
        return X.solve()