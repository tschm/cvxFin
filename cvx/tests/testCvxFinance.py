from nose.tools import with_setup
from nose.tools import assert_raises

from cvxopt import solvers

import numpy as np
import numpy.testing as npTest

import cvx.cvxFinance as cvx


def setup_func():
    solvers.options['show_progress'] = False


def teardown_func():
    pass


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
    return np.array([np.inf, 10.0, np.inf, np.inf])


def __get_bcl():
    return np.array([30.0, 15.0, -np.inf])


def __get_bcu():
    return np.array([30.0, np.inf, 25.0])


@with_setup(setup_func, teardown_func)
def testLinear():
    #see the example at
    #http://docs.mosek.com/6.0/capi/node007.html#250240248
    y = cvx.solveLP(c=__get_c(), A=__get_A(), bxl=__get_bxl(), bxu=__get_bxu(), bcl=__get_bcl(), bcu=__get_bcu())
    npTest.assert_array_almost_equal(y, np.array([0, 0, 15.0, 8.333333]))


@with_setup(setup_func, teardown_func)
def testLinearFalseBounds():
    assert_raises(AssertionError, cvx.solveLP, c=np.array([1.0]), A=[], bxl=np.array([2.0]), bxu=np.array([0.0]), bcl=[], bcu=[])


@with_setup(setup_func, teardown_func)
def testLinearBoundsTooShort():
    assert_raises(AssertionError, cvx.solveLP,
                  c=np.array([1.0, 2.0]),
                  A=[],
                  bxl=np.array([2.0]),
                  bxu=np.array([0.0]),
                  bcl=[],
                  bcu=[])


@with_setup(setup_func, teardown_func)
def testLinearNoConstraints():
    assert_raises(ArithmeticError, cvx.solveLP,
                  c=np.array([1.0]),
                  A=np.array([1.0]),
                  bxl=np.array([-np.inf]),
                  bxu=np.array([np.inf]),
                  bcl=np.array([-np.inf]),
                  bcu=np.array([np.inf]))


@with_setup(setup_func, teardown_func)
def testLinearInfeasible():
    assert_raises(ArithmeticError, cvx.solveLP,
                  c=np.array([1.0, 1.0]),
                  A=np.array([[1.0, 0.0], [1.0, 1.0]]),
                  bxl=np.array([0.0, 0.0]),
                  bxu=np.array([1.0, 1.0]),
                  bcl=np.array([3.0, 3.0]),
                  bcu=np.array([5.0, 5.0]))


@with_setup(setup_func, teardown_func)
def testQuadratic():
    x = cvx.solveQPcon(c=__get_c(), A=__get_A(), Q=__get_Q(), qc=17, bxl=__get_bxl(), bxu=__get_bxu(), bcl=__get_bcl(), bcu=__get_bcu())
    npTest.assert_array_almost_equal(x, np.array([0, 0, 15.0, 4.00]))


@with_setup(setup_func, teardown_func)
def testQuadNegative():
    assert_raises(AssertionError, cvx.solveQPcon, c=__get_c(), A=__get_A(), Q=__get_Q(), qc=-17,
                  bxl=__get_bxl(), bxu=__get_bxu(), bcl=__get_bcl(), bcu=__get_bcu())


@with_setup(setup_func, teardown_func)
def testQuadInfeasible():
    assert_raises(ArithmeticError, cvx.solveQPcon, c=__get_c(), A=__get_A(), Q=__get_Q(), qc=1,
                  bxl=np.array([2.0, 2.0, 2.0, 2.0]), bxu=np.array([5.0, 5.0, 5.0, 5.0]), bcl=__get_bcl(), bcu=__get_bcu())


@with_setup(setup_func, teardown_func)
def testMarkowitzConstraint():
    v1 = 2.0*np.ones(4)
    x0 = np.array([5.0, 1.0, 10.0, 2.0])

    x = cvx.solveMarkowitzConstraint(c=__get_c(), A=__get_A(), Q=__get_Q(), qc=17, v=v1, x0=x0, bxl=__get_bxl(), bxu=__get_bxu(), bcl=__get_bcl(), bcu=__get_bcu())
    npTest.assert_array_almost_equal(x, np.array([3.0, 1.0, 10.0, 2.0]))


@with_setup(setup_func, teardown_func)
def testMarkowitzObjective():
    v1 = 0.5*np.ones(4)
    x0 = np.array([5.0, 1.0, 10.0, 2.0])

    x = cvx.solveMarkowitzObjective(c=__get_c(), A=__get_A(), Q=__get_Q(), v=v1, x0=x0, bxl=__get_bxl(), bxu=__get_bxu(), bcl=__get_bcl(), bcu=__get_bcu())
    npTest.assert_array_almost_equal(x, np.array([5.18867943e+00, 1.11254698e-06, 7.21698030e+00, 2.46512400e-08]))


@with_setup(setup_func, teardown_func)
def testQuadraticObjective():
    x = cvx.solveQPobj(c=__get_c(), A=__get_A(), Q=__get_Q(), bxl=__get_bxl(), bxu=__get_bxu(), bcl=__get_bcl(), bcu=__get_bcu())
    npTest.assert_array_almost_equal(x, np.array([5.66037740e+00, 7.27653920e-08, 6.50943386e+00, 2.54269440e-07]))

