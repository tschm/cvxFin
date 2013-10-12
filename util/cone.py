from cvxopt import matrix, solvers
import numpy


class coneAux:
    def __init__(self):
        self.dims = {'l': 0, 'q': [], 's': []}
        self.G = []   # list of rows
        self.h = []   # list of entries

    def __append(self, A, c):
        for row in A:
            self.G.append(row)

        for x in c:
            self.h.append(x)

    def pushLinConstraint(self, A, c):
        self.dims['l'] += A.shape[0]
        self.__append(A, c)

    def pushQuadConstraint(self, Q, c):
        self.dims['q'].append(Q.shape[0])
        self.__append(Q, c)


class conelp:
    def __init__(self, c):
        self.__c = c
        self.aux = coneAux()

    def solve(self):
        if len(self.aux.G) == 0:
            raise ArithmeticError('No constraints')

        A = solvers.conelp(c=matrix(self.__c),
                           G=matrix(numpy.array(self.aux.G)),
                           h=matrix(numpy.array(self.aux.h)),
                           dims=self.aux.dims)

        if A["status"] == "optimal":
            return numpy.array(A['x']).transpose()[0], A
        else:
            raise ArithmeticError("Solution not optimal: " + A["status"])


class coneqp:
    def __init__(self, P, q):
        self.__P = P
        self.__q = q
        self.aux = coneAux()

    def solve(self):
        if len(self.aux.G) == 0:
            raise ArithmeticError('No constraints')

        A = solvers.coneqp(P=matrix(self.__P),
                           q=matrix(self.__q),
                           G=matrix(numpy.array(self.aux.G)),
                           h=matrix(numpy.array(self.aux.h)),
                           dims=self.aux.dims)

        if A["status"] == "optimal":
            return numpy.array(A['x']).transpose()[0], A
        else:
            raise ArithmeticError("Solution not optimal: " + A["status"])

