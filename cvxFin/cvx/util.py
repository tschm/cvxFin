import cvxpy as cvx
import numpy as np

def cvx2np(x):
    return np.array([x[i].value for i in range(x.size[0])])


def minimize(objective, constraints):
    cvx.Problem(cvx.Minimize(objective), constraints).solve()


def maximize(objective, constraints):
    cvx.Problem(cvx.Maximize(objective), constraints).solve()