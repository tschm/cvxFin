import cvxpy as cvx
import numpy as np

def __cvx2np(x):
    return np.array([x[i].value for i in range(x.size[0])])


def __minimize(objective, constraints):
    cvx.Problem(cvx.Minimize(objective), constraints).solve()


def __maximize(objective, constraints):
    cvx.Problem(cvx.Maximize(objective), constraints).solve()



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
    __maximize(objective=objective, constraints=constraints)
    return __cvx2np(x)

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
    __maximize(objective=objective, constraints=constraints)
    return __cvx2np(x)

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
    __maximize(objective=objective, constraints=constraints)
    return __cvx2np(x)

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
    __maximize(objective=objective, constraints=constraints)
    return __cvx2np(x)


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
    __maximize(objective=objective, constraints=constraints)
    return __cvx2np(x)