import numpy
from cvxFin.util.cone import conelp, coneqp

from cvxFin.util.quadraticProgram import QuadraticConstraintProgram, QuadraticObjectiveProgram


class AbsPenalty:
    def __init__(self, n):
        self.v = numpy.zeros(n)
        self.x0 = numpy.zeros(n)

    def getCVX(self):
        h = numpy.concatenate([self.x0, -self.x0])
        E = numpy.eye(len(self.x0), len(self.x0))
        G = numpy.vstack([numpy.hstack([E, -E]), numpy.hstack([-E, -E])])
        return {'mat': G, 'vec': h}

    def eval(self, x):
        return numpy.sum(self.v * numpy.abs(x - self.x0))


class MarkowitzObjectiveProgram:
    def __init__(self, Q, c, A):
        self.qp = QuadraticObjectiveProgram(Q=Q, p=c, A=A)
        self.penalty = AbsPenalty(len(c))

    def solve(self):
        c = numpy.concatenate([self.qp.lp.c, self.penalty.v])
        Q = numpy.zeros((len(c), len(c)))
        Q[0:len(self.qp.lp.c), 0:len(self.qp.lp.c)] = self.qp.Q

        X = coneqp(P=Q, q=c)

        bx = self.qp.lp.bx.get_cvx()
        bc = self.qp.lp.bc.get_cvx()
        p = self.penalty.getCVX()

        X.aux.pushLinConstraint(numpy.hstack([bx['mat'], numpy.zeros(bx['mat'].shape)]), bx['vec'])
        X.aux.pushLinConstraint(numpy.hstack([bc['mat'], numpy.zeros(bc['mat'].shape)]), bc['vec'])
        X.aux.pushLinConstraint(p['mat'], p['vec'])

        x = X.solve()
        return x[0][0:len(self.qp.lp.c)], x[1]


class MarkowitzConstraintProgram:
    def __init__(self, c, A, Q):
        self.qp = QuadraticConstraintProgram(c, A, Q)
        self.penalty = AbsPenalty(len(c))

    def solve(self):
        c = numpy.concatenate([self.qp.lp.c, self.penalty.v])

        X = conelp(c)

        bx = self.qp.lp.bx.get_cvx()
        bc = self.qp.lp.bc.get_cvx()
        qc = self.qp.qc.get_cvx()
        p = self.penalty.getCVX()

        X.aux.pushLinConstraint(numpy.hstack([bx['mat'], numpy.zeros(bx['mat'].shape)]), bx['vec'])
        X.aux.pushLinConstraint(numpy.hstack([bc['mat'], numpy.zeros(bc['mat'].shape)]), bc['vec'])
        X.aux.pushLinConstraint(p['mat'], p['vec'])
        X.aux.pushQuadConstraint(numpy.hstack([qc['mat'], numpy.zeros(qc['mat'].shape)]), qc['vec'])

        x = X.solve()
        return x[0][0:len(self.qp.lp.c)], x[1]