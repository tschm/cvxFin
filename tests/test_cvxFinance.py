import numpy as np
import numpy.testing as npTest
import pytest

import cvx.finance.Finance as Fin


@pytest.fixture()
def c():
    return np.array([3.0, 1.0, 5.0, 1.0])


@pytest.fixture()
def A():
    return np.array([[3.0, 1.0, 2.0, 0.0], [2.0, 1.0, 3.0, 1.0], [0.0, 2.0, 0.0, 3.0]])


@pytest.fixture()
def Q():
    return np.array(
        [
            [1.0, 0.3, 0.2, 0.2],
            [0.3, 1.0, 0.25, 0.5],
            [0.2, 0.25, 1.0, 0.4],
            [0.2, 0.5, 0.4, 1.0],
        ]
    )


@pytest.fixture()
def bxl():
    return np.zeros(4)


@pytest.fixture()
def bxu():
    return np.array([1e6, 10.0, 1e6, 1e6])


@pytest.fixture()
def bcl():
    return np.array([30.0, 15.0, -1e6])


@pytest.fixture()
def bcu():
    return np.array([30.0, 1e6, 25.0])


def testLinear(c, A, bxl, bxu, bcl, bcu):
    # see the example at
    # http://docs.mosek.com/6.0/capi/node007.html#250240248
    y = Fin.solveLP(c=c, A=A, bxl=bxl, bxu=bxu, bcl=bcl, bcu=bcu)
    npTest.assert_array_almost_equal(y, np.array([0, 0, 15.0, 8.333333]))


def testQuadratic(c, A, Q, bxl, bxu, bcl, bcu):
    x = Fin.solveQPcon(c=c, A=A, Q=Q, qc=17, bxl=bxl, bxu=bxu, bcl=bcl, bcu=bcu)
    npTest.assert_array_almost_equal(x, np.array([0, 0, 15.0, 4.00]))


def testMarkowitzConstraint(c, A, Q, bxl, bxu, bcl, bcu):
    v1 = 2.0 * np.ones(4)
    x0 = np.array([5.0, 1.0, 10.0, 2.0])

    x = Fin.solveMarkowitzConstraint(
        c=c, A=A, Q=Q, qc=17, v=v1, x0=x0, bxl=bxl, bxu=bxu, bcl=bcl, bcu=bcu
    )
    npTest.assert_array_almost_equal(x, np.array([3.0, 1.0, 10.0, 2.0]))


def testMarkowitzObjective(c, A, Q, bxl, bxu, bcl, bcu):
    v1 = 0.5 * np.ones(4)
    x0 = np.array([5.0, 1.0, 10.0, 2.0])

    x = Fin.solveMarkowitzObjective(
        c=c, A=A, Q=Q, v=v1, x0=x0, bxl=bxl, bxu=bxu, bcl=bcl, bcu=bcu
    )

    npTest.assert_array_almost_equal(
        x, np.array([5.188679e00, 6.545244e-08, 7.216981e00, 1.297973e-08])
    )


def testQuadraticObjective(c, A, Q, bxl, bxu, bcl, bcu):
    x = Fin.solveQPobj(c=c, A=A, Q=Q, bxl=bxl, bxu=bxu, bcl=bcl, bcu=bcu)
    diff = x - np.array([5.660383e00, 5.440500e-10, 6.509425e00, 1.738264e-10])
    assert np.linalg.norm(diff, ord=1) < 1e-4
