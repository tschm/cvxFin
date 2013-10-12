import unittest
import logging

import numpy
import numpy.testing as npTest

from cvx.cvxFinance import solveLP, solveQPcon, solveMarkowitzConstraint, solveQPobj, solveMarkowitzObjective


class cvxFinanceTest(unittest.TestCase):
    #def setUp(self):
    #    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    def __get_c(self):
        return numpy.array([3.0, 1.0, 5.0, 1.0])

    def __get_A(self):
        return numpy.array([[3.0, 1.0, 2.0, 0.0],
                            [2.0, 1.0, 3.0, 1.0],
                            [0.0, 2.0, 0.0, 3.0]])

    def __get_Q(self):
        return numpy.array([[1.0, 0.3, 0.2, 0.2],
                            [0.3, 1.0, 0.25, 0.5],
                            [0.2, 0.25, 1.0, 0.4],
                            [0.2, 0.5, 0.4, 1.0]])

    def __get_bxl(self):
        return numpy.zeros(4)

    def __get_bxu(self):
        return numpy.array([numpy.inf, 10.0, numpy.inf, numpy.inf])

    def __get_bcl(self):
        return numpy.array([30.0, 15.0, -numpy.inf])

    def __get_bcu(self):
        return numpy.array([30.0, numpy.inf, 25.0])

    def testLinear(self):
        #see the example at
        #http://docs.mosek.com/6.0/capi/node007.html#250240248
        y = solveLP(c=self.__get_c(),
                    A=self.__get_A(),
                    bxl=self.__get_bxl(),
                    bxu=self.__get_bxu(),
                    bcl=self.__get_bcl(),
                    bcu=self.__get_bcu())

        npTest.assert_array_almost_equal(y, numpy.array([0, 0, 15.0, 8.333333]))

    def testLinearFalseBounds(self):
        self.assertRaises(AssertionError, solveLP,
                          c=numpy.array([1.0]),
                          A=[],
                          bxl=numpy.array([2.0]),
                          bxu=numpy.array([0.0]),
                          bcl=[],
                          bcu=[])

    def testLinearBoundsTooShort(self):
        self.assertRaises(AssertionError, solveLP,
                          c=numpy.array([1.0, 2.0]),
                          A=[],
                          bxl=numpy.array([2.0]),
                          bxu=numpy.array([0.0]),
                          bcl=[],
                          bcu=[])

    def testLinearNoConstraints(self):
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
        self.assertRaises(ArithmeticError, solveLP,
                          c=numpy.array([1.0]),
                          A=numpy.array([1.0]),
                          bxl=numpy.array([-numpy.inf]),
                          bxu=numpy.array([numpy.inf]),
                          bcl=numpy.array([-numpy.inf]),
                          bcu=numpy.array([numpy.inf]))

    def testLinearInfeasible(self):
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
        self.assertRaises(ArithmeticError, solveLP,
                          c=numpy.array([1.0, 1.0]),
                          A=numpy.array([[1.0, 0.0], [1.0, 1.0]]),
                          bxl=numpy.array([0.0, 0.0]),
                          bxu=numpy.array([1.0, 1.0]),
                          bcl=numpy.array([3.0, 3.0]),
                          bcu=numpy.array([5.0, 5.0]))

    def testQuadratic(self):
        x = solveQPcon(c=self.__get_c(), A=self.__get_A(), Q=self.__get_Q(), qc=17, bxl=self.__get_bxl(),
                       bxu=self.__get_bxu(),
                       bcl=self.__get_bcl(),
                       bcu=self.__get_bcu())

        npTest.assert_array_almost_equal(x, numpy.array([0, 0, 15.0, 4.00]))

    def testQuadNegative(self):
        self.assertRaises(AssertionError, solveQPcon, c=self.__get_c(), A=self.__get_A(), Q=self.__get_Q(), qc=-17,
                          bxl=self.__get_bxl(),
                          bxu=self.__get_bxu(),
                          bcl=self.__get_bcl(),
                          bcu=self.__get_bcu())

    def testQuadInfeasible(self):
        self.assertRaises(ArithmeticError, solveQPcon, c=self.__get_c(), A=self.__get_A(), Q=self.__get_Q(), qc=1,
                          bxl=numpy.array([2.0, 2.0, 2.0, 2.0]),
                          bxu=numpy.array([5.0, 5.0, 5.0, 5.0]),
                          bcl=self.__get_bcl(),
                          bcu=self.__get_bcu())

    def testMarkowitzConstraint(self):
        v1 = numpy.zeros(4)
        v1.fill(2.0)
        x0 = numpy.array([5.0, 1.0, 10.0, 2.0])

        x = solveMarkowitzConstraint(c=self.__get_c(), A=self.__get_A(), Q=self.__get_Q(), qc=17, v=v1, x0=x0,
                                     bxl=self.__get_bxl(),
                                     bxu=self.__get_bxu(),
                                     bcl=self.__get_bcl(),
                                     bcu=self.__get_bcu())

        npTest.assert_array_almost_equal(x, numpy.array([3.0, 1.0, 10.0, 2.0]))

    def testMarkowitzObjective(self):
        v1 = numpy.zeros(4)
        v1.fill(0.5)
        x0 = numpy.array([5.0, 1.0, 10.0, 2.0])

        x = solveMarkowitzObjective(c=self.__get_c(), A=self.__get_A(), Q=self.__get_Q(), v=v1, x0=x0,
                                    bxl=self.__get_bxl(),
                                    bxu=self.__get_bxu(),
                                    bcl=self.__get_bcl(),
                                    bcu=self.__get_bcu())

        npTest.assert_array_almost_equal(x, numpy.array([5.18867943e+00, 1.11254698e-06, 7.21698030e+00,
                                                         2.46512400e-08]))

    def testQuadraticObjective(self):
        x = solveQPobj(c=self.__get_c(), A=self.__get_A(), Q=self.__get_Q(), bxl=self.__get_bxl(),
                       bxu=self.__get_bxu(),
                       bcl=self.__get_bcl(),
                       bcu=self.__get_bcu())

        npTest.assert_array_almost_equal(x,
                                         numpy.array([5.66037740e+00, 7.27653920e-08, 6.50943386e+00, 2.54269440e-07]))


if __name__ == '__main__':
    from cvxopt import solvers

    solvers.options['show_progress'] = False
    unittest.main()
