import numpy
from cvxFin.util.cone import conelp, coneqp

from cvxFin.util.linearProgram import LinearProgram


class QuadraticConstraintProgram:
    class __QuadraticBound:
        def __init__(self, Q):
            self.__Q = Q
            self.upper = numpy.infty

        def get_cvx(self):
            n = numpy.shape(self.__Q)[0]
            assert self.upper < numpy.infty, "Non-valid bound for quadratic term"
            assert self.upper >= 0, "Non-valid bound for quadratic term"

            L = numpy.transpose(numpy.linalg.cholesky(self.__Q))
            A = numpy.vstack([numpy.zeros((1, n)), L])
            h = numpy.concatenate([[self.upper], numpy.zeros(n)])

            return {'mat': A, 'vec': h}

        def eval(self, x):
            return numpy.sqrt(numpy.sum(x * numpy.dot(self.__Q, x)))

    def __init__(self, c, A, Q):
        self.lp = LinearProgram(c, A)
        self.qc = QuadraticConstraintProgram.__QuadraticBound(Q)

    def solve(self):
        bx = self.lp.bx.get_cvx()
        bc = self.lp.bc.get_cvx()
        qc = self.qc.get_cvx()

        X = conelp(self.lp.c)
        X.aux.pushLinConstraint(bx['mat'], bx['vec'])
        X.aux.pushLinConstraint(bc['mat'], bc['vec'])
        X.aux.pushQuadConstraint(qc['mat'], qc['vec'])

        return X.solve()


class QuadraticObjectiveProgram:
    def __init__(self, Q, p, A):
        self.lp = LinearProgram(c=p, matrix=A)
        self.Q = Q

    def solve(self):
        bx = self.lp.bx.get_cvx()
        bc = self.lp.bc.get_cvx()

        X = coneqp(P=self.Q, q=self.lp.c)

        X.aux.pushLinConstraint(bx['mat'], bx['vec'])
        X.aux.pushLinConstraint(bc['mat'], bc['vec'])

        return X.solve()