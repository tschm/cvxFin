from cvxFin.util.markowitzProgram import MarkowitzConstraintProgram, MarkowitzObjectiveProgram
from cvxFin.util.quadraticProgram import QuadraticConstraintProgram, QuadraticObjectiveProgram
from cvxFin.util.linearProgram import LinearProgram


def solveLP(c, A, bxl, bxu, bcl, bcu):
    """
    Solves a linear program

    maximize    c'*x
    subject to  bcl <= A*x <= bcu
                bxl <=  x  <= bxu
    """
    lp = LinearProgram(c=-c, A=A)
    lp.bc.lower = bcl
    lp.bc.upper = bcu
    lp.bx.lower = bxl
    lp.bx.upper = bxu
    return lp.solve()[0]


def solveQPcon(c, A, Q, qc, bxl, bxu, bcl, bcu):
    """
    Solves a convex program with a quadratic constraint

    maximize      c'*x
    subject to    bcl <= A*x <= bcu
                  bxl <=  x  <= bxu
                sqrt(x'*Q*x) <= qc
    """
    qp = QuadraticConstraintProgram(-c, A, Q)
    qp.qc.upper = qc
    qp.lp.bc.lower = bcl
    qp.lp.bc.upper = bcu
    qp.lp.bx.lower = bxl
    qp.lp.bx.upper = bxu
    return qp.solve()[0]


def solveQPobj(c, A, Q, bxl, bxu, bcl, bcu):
    """
    Solves a convex program with a quadratic objective

    maximize    c'*x - (1/2) x'*Q*x
    subject to    bcl <= A*x <= bcu
                  bxl <=  x  <= bxu
    """
    qp = QuadraticObjectiveProgram(Q=Q, p=-c, A=A)
    qp.lp.bc.lower = bcl
    qp.lp.bc.upper = bcu
    qp.lp.bx.lower = bxl
    qp.lp.bx.upper = bxu
    return qp.solve()[0]


def solveMarkowitzConstraint(c, A, Q, qc, v, x0, bxl, bxu, bcl, bcu):
    """
    Solves a convex program with a quadratic constraint and linear abs penalty

    maximize     c'*x - v'*abs{x - x0}
    subject to    bcl <= A*x <= bcu
                  bxl <=  x  <= bxu
                sqrt(x'*Q*x) <= qc
    """
    mp = MarkowitzConstraintProgram(-c, A, Q)
    mp.qp.qc.upper = qc
    mp.qp.lp.bc.lower = bcl
    mp.qp.lp.bc.upper = bcu
    mp.qp.lp.bx.lower = bxl
    mp.qp.lp.bx.upper = bxu
    mp.penalty.v = v
    mp.penalty.x0 = x0
    return mp.solve()[0]


def solveMarkowitzObjective(c, A, Q, v, x0, bxl, bxu, bcl, bcu):
    """
    Solves a convex program with a quadratic constraint and linear abs penalty

    maximize     c'*x - (1/2) x'*Q*x - v'*abs{x - x0}
    subject to    bcl <= A*x <= bcu
                  bxl <=  x  <= bxu
    """
    mp = MarkowitzObjectiveProgram(Q=Q, c=-c, A=A)
    mp.qp.lp.bc.lower = bcl
    mp.qp.lp.bc.upper = bcu
    mp.qp.lp.bx.lower = bxl
    mp.qp.lp.bx.upper = bxu
    mp.penalty.v = v
    mp.penalty.x0 = x0
    return mp.solve()[0]