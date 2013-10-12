from sklearn.linear_model import lasso_path

from util.quadraticProgram import QuadraticObjectiveProgram

def solveLSQ(b, A, B, bxl, bxu, bcl, bcu):
    """
    Solves a constrained linear least squares problem

    minimize   2-norm (A*x-b)^2
    subject to  bcl <= B*x <= bcu
                bxl <=  x  <= bxu
    """
    (n, m) = A.shape

    q = numpy.zeros(m + n)
    q[m:m + n] = 1

    C1 = numpy.hstack((A, -numpy.eye(n, n)))               # A*x - I*u = [A, -I]*[x;u]
    C2 = numpy.hstack((B, numpy.zeros((B.shape[0], n))))

    qp = QuadraticObjectiveProgram(Q=numpy.diag(v=q, k=0),
                                   p=numpy.zeros(n + m),
                                   A=numpy.vstack((C1, C2)))

    qp.lp.bc.lower = numpy.concatenate((b, bcl))
    qp.lp.bc.upper = numpy.concatenate((b, bcu))

    qp.lp.bx.lower = numpy.concatenate((bxl, -numpy.inf * numpy.ones(n)))
    qp.lp.bx.upper = numpy.concatenate((bxu, +numpy.inf * numpy.ones(n)))

    return qp.solve()[0][0:m]


def solveLASSO(b, A, B, bxl, bxu, bcl, bcu, tau):
    """
    Solves a constrained linear least squares problem

    minimize   2-norm (A*x-b)^2 + tau 1-norm(x)
    subject to  bcl <= B*x <= bcu
                bxl <=  x  <= bxu
    """
    (n, m) = A.shape

    q = numpy.zeros(2 * m + n)   #[x,z,t]
    q[m:m + n] = 1

    C1 = numpy.hstack((A, -numpy.eye(n, n), numpy.zeros((n, m))))               # A*x - I*u = [A, -I]*[x;u]
    C2 = numpy.hstack((B, numpy.zeros((B.shape[0], n + m))))
    E = numpy.eye(m, m)
    C3 = numpy.hstack((E, numpy.zeros((m, n)), -E))
    C4 = numpy.hstack((-E, numpy.zeros((m, n)), -E))

    qp = QuadraticObjectiveProgram(Q=numpy.diag(v=q, k=0),
                                   p=numpy.concatenate((numpy.zeros(n + m), tau * numpy.ones(m))),
                                   A=numpy.vstack((C1, C2, C3, C4)))

    qp.lp.bc.lower = numpy.concatenate((b, bcl, -numpy.inf * numpy.ones(2 * m)))
    qp.lp.bc.upper = numpy.concatenate((b, bcu, numpy.zeros(2 * m)))

    qp.lp.bx.lower = numpy.concatenate((bxl, -numpy.inf * numpy.ones(n + m)))
    qp.lp.bx.upper = numpy.concatenate((bxu, +numpy.inf * numpy.ones(n + m)))

    return qp.solve()[0][0:m]


def solvePenalizedLSQ(A, b, eps, B, c):
    """
    Solves an  unconstrained linear least squares problem

    minimize   2-norm (A*x-b)^2 + eps * 2-norm (Bx-c)^2 + tau 1-norm(x)
    """
    X = numpy.vstack((A, eps * B))
    y = numpy.concatenate((b, c))

    print "Computing regularization path using the lasso..."
    models = lasso_path(X, y)
    alphas_lasso = numpy.array([model.alpha for model in models])
    coefs_lasso = numpy.array([model.coef_ for model in models])

    print alphas_lasso
    print coefs_lasso


if __name__ == '__main__':
    import numpy

    A = numpy.random.randn(10, 3)
    b = numpy.random.randn(10)

    print solveLASSO(b, A, numpy.eye(3, 3), bxl=-10 * numpy.ones(3), bxu=10 * numpy.ones(3), bcl=-20 * numpy.ones(3),
                     bcu=20 * numpy.ones(3), tau=0.0)

    print numpy.linalg.lstsq(A, b)[0]



