import cvxpy as cvx


def minimize(objective, constraints, verbose=False, solver=cvx.ECOS):
    cvx.Problem(cvx.Minimize(objective), constraints).solve(verbose=verbose, solver=solver)


def maximize(objective, constraints, verbose=False, solver=cvx.ECOS):
    cvx.Problem(cvx.Maximize(objective), constraints).solve(verbose=verbose, solver=solver)

def installed_solvers():
    return cvx.installed_solvers()
