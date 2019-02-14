import numpy as np
import numpy.testing as npTest

import cvxFin.cvx.cvxFinance as Fin


def __get_c():
    return np.array([3.0, 1.0, 5.0, 1.0])


def __get_A():
    return np.array([[3.0, 1.0, 2.0, 0.0],
                     [2.0, 1.0, 3.0, 1.0],
                     [0.0, 2.0, 0.0, 3.0]])


def __get_Q():
    return np.array([[1.0, 0.3, 0.2, 0.2],
                     [0.3, 1.0, 0.25, 0.5],
                     [0.2, 0.25, 1.0, 0.4],
                     [0.2, 0.5, 0.4, 1.0]])


def __get_bxl():
    return np.zeros(4)


def __get_bxu():
    return np.array([1e6, 10.0, 1e6, 1e6])


def __get_bcl():
    return np.array([30.0, 15.0, -1e6])


def __get_bcu():
    return np.array([30.0, 1e6, 25.0])

def testLinear():
    # see the example at
    # http://docs.mosek.com/6.0/capi/node007.html#250240248
    y = Fin.solveLP(c=__get_c(), A=__get_A(), bxl=__get_bxl(), bxu=__get_bxu(), bcl=__get_bcl(), bcu=__get_bcu())
    npTest.assert_array_almost_equal(y, np.array([0, 0, 15.0, 8.333333]))


def testQuadratic():
    x = Fin.solveQPcon(c=__get_c(), A=__get_A(), Q=__get_Q(), qc=17, bxl=__get_bxl(), bxu=__get_bxu(), bcl=__get_bcl(), bcu=__get_bcu())
    npTest.assert_array_almost_equal(x, np.array([0, 0, 15.0, 4.00]))


def testMarkowitzConstraint():
    v1 = 2.0*np.ones(4)
    x0 = np.array([5.0, 1.0, 10.0, 2.0])

    x = Fin.solveMarkowitzConstraint(c=__get_c(), A=__get_A(), Q=__get_Q(), qc=17, v=v1, x0=x0, bxl=__get_bxl(), bxu=__get_bxu(), bcl=__get_bcl(), bcu=__get_bcu())
    npTest.assert_array_almost_equal(x, np.array([3.0, 1.0, 10.0, 2.0]))


def testMarkowitzObjective():
    v1 = 0.5*np.ones(4)
    x0 = np.array([5.0, 1.0, 10.0, 2.0])

    x = Fin.solveMarkowitzObjective(c=__get_c(), A=__get_A(), Q=__get_Q(), v=v1, x0=x0, bxl=__get_bxl(), bxu=__get_bxu(), bcl=__get_bcl(), bcu=__get_bcu())
    npTest.assert_array_almost_equal(x, np.array([5.188598e+00, 9.970451e-08, 7.217103e+00, 2.009898e-08]))


def testQuadraticObjective():
    x = Fin.solveQPobj(c=__get_c(), A=__get_A(), Q=__get_Q(), bxl=__get_bxl(), bxu=__get_bxu(), bcl=__get_bcl(), bcu=__get_bcu())
    npTest.assert_array_almost_equal(x, np.array([5.660383e+00,   5.440500e-10,   6.509425e+00,   1.738264e-10]))

