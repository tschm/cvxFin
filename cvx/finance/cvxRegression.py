from sklearn.linear_model import lasso_path

import cvx.finance.util as ccu
import cvxpy as cvx


def solveLASSO(b, A, B, bxl, bxu, bcl, bcu, tau=0):
    """
    Solves a constrained linear least squares problem

    minimize   2-norm (A*x-b) + tau 1-norm(x)
    subject to  bcl <= B*x <= bcu
                bxl <=  x  <= bxu
    """
    (n, m) = A.shape
    x = cvx.Variable(m)
    constraints = [B*x <= bcu, bcl <= B*x, bxl <= x, x <= bxu]
    objective = cvx.norm(A*x-b,2) + tau*cvx.norm(x,1)
    ccu.minimize(objective=objective, constraints=constraints)
    return x.value


def solvePenalizedLSQ(A, b, eps, B, c):
    """
    Solves an  unconstrained linear least squares problem

    minimize   2-norm (A*x-b)^2 + eps * 2-norm (Bx-c)^2 + tau 1-norm(x)
    """
    X = numpy.vstack((A, eps * B))
    y = numpy.concatenate((b, c))

    models = lasso_path(X, y)
    alphas_lasso = numpy.array([model.alpha for model in models])
    coefs_lasso = numpy.array([model.coef_ for model in models])

    print(alphas_lasso)
    print(coefs_lasso)

