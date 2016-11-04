import cvxpy as cvx
import numpy as np
import cvxFin.cvx.util as ccu

def solveLP(c, A, bxl, bxu, bcl, bcu):
    """
    Solves a linear program

    maximize    c'*x
    subject to  bcl <= A*x <= bcu
                bxl <=  x  <= bxu
    """
    x = cvx.Variable(len(c))
    constraints = [A*x <= bcu, bcl <= A*x, bxl <= x, x <= bxu]
    objective = x.T*c
    ccu.maximize(objective=objective, constraints=constraints)
    return ccu.cvx2np(x)

def solveQPcon(c, A, Q, qc, bxl, bxu, bcl, bcu):
    """
    Solves a convex program with a quadratic constraint

    maximize      c'*x
    subject to    bcl <= A*x <= bcu
                  bxl <=  x  <= bxu
                sqrt(x'*Q*x) <= qc
    """
    x = cvx.Variable(len(c))
    constraints = [A*x <= bcu, bcl <= A*x, bxl <= x, x <= bxu, cvx.quad_form(x, Q) <= qc*qc]
    objective = x.T*c
    ccu.maximize(objective=objective, constraints=constraints)
    return ccu.cvx2np(x)

def solveQPobj(c, A, Q, bxl, bxu, bcl, bcu):
    """
    Solves a convex program with a quadratic objective

    maximize    c'*x - (1/2) x'*Q*x
    subject to    bcl <= A*x <= bcu
                  bxl <=  x  <= bxu
    """
    x = cvx.Variable(len(c))
    constraints = [A*x <= bcu, bcl <= A*x, bxl <= x, x <= bxu]
    objective = x.T*c - 0.5 * cvx.quad_form(x, Q)
    ccu.maximize(objective=objective, constraints=constraints)
    return ccu.cvx2np(x)

def solveMarkowitzConstraint(c, A, Q, qc, v, x0, bxl, bxu, bcl, bcu):
    """
    Solves a convex program with a quadratic constraint and linear abs penalty

    maximize     c'*x - v'*abs{x - x0}
    subject to    bcl <= A*x <= bcu
                  bxl <=  x  <= bxu
                sqrt(x'*Q*x) <= qc
    """
    x = cvx.Variable(len(c))
    constraints = [A*x <= bcu, bcl <= A*x, bxl <= x, x <= bxu, cvx.quad_form(x, Q) <= qc*qc]
    objective = x.T*c - cvx.abs(x - x0).T*v
    ccu.maximize(objective=objective, constraints=constraints)
    return ccu.cvx2np(x)


def solveMarkowitzObjective(c, A, Q, v, x0, bxl, bxu, bcl, bcu):
    """
    Solves a convex program with a quadratic constraint and linear abs penalty

    maximize     c'*x - (1/2) x'*Q*x - v'*abs{x - x0}
    subject to    bcl <= A*x <= bcu
                  bxl <=  x  <= bxu
    """
    x = cvx.Variable(len(c))
    constraints = [A*x <= bcu, bcl <= A*x, bxl <= x, x <= bxu, cvx.quad_form(x, Q)]
    objective = x.T*c -0.5 * cvx.quad_form(x, Q) - cvx.abs(x - x0).T*v
    ccu.maximize(objective=objective, constraints=constraints)
    return ccu.cvx2np(x)