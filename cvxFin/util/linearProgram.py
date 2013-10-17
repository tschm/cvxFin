import numpy
from cvxFin.util.cone import conelp


class LinearProgram:
    class __LinearBound:
        def __init__(self, matrix):
            n = numpy.shape(matrix)[0]
            self.lower = -numpy.inf*numpy.ones(n)
            self.upper = +numpy.inf*numpy.ones(n)
            self.__mat = matrix

        def get_cvx(self):
            """
            Constraint brought into G*x <= h standard form
            """
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

    def __init__(self, c, matrix):
        self.c = c
        self.bx = self.__LinearBound(numpy.eye(len(c), len(c)))
        self.bc = self.__LinearBound(matrix)

    def solve(self):
        bx = self.bx.get_cvx()
        bc = self.bc.get_cvx()

        X = conelp(self.c)
        X.aux.pushLinConstraint(bx['mat'], bx['vec'])
        X.aux.pushLinConstraint(bc['mat'], bc['vec'])
        return X.solve()