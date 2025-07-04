# Copyright 2020 Thomas Schmelzer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import cvxpy as cvx

from . import util as ccu


def __weight(c, bxl, bxu):
    x = cvx.Variable(c.size)
    return x, [bxl <= x, x <= bxu]


def __constraint(x, A, bcl, bcu):
    return [A @ x <= bcu, bcl <= A @ x]


def solveLP(c, A, bxl, bxu, bcl, bcu):
    """
    Solves a linear program

    maximize    c'*x
    subject to  bcl <= A*x <= bcu
                bxl <=  x  <= bxu
    """
    x, constraints = __weight(c, bxl, bxu)

    constraints = constraints + __constraint(x, A, bcl, bcu)

    objective = x.T @ c
    print(ccu.installed_solvers())
    ccu.maximize(objective=objective, constraints=constraints, verbose=True)
    return x.value


def solveQPcon(c, A, Q, qc, bxl, bxu, bcl, bcu):
    """
    Solves a convex program with a quadratic constraint

    maximize      c'*x
    subject to    bcl <= A*x <= bcu
                  bxl <=  x  <= bxu
                sqrt(x'*Q*x) <= qc
    """
    x, constraints = __weight(c, bxl, bxu)
    constraints = constraints + __constraint(x, A, bcl, bcu) + [cvx.quad_form(x, Q) <= qc * qc]
    objective = x.T @ c
    ccu.maximize(objective=objective, constraints=constraints)
    return x.value


def solveQPobj(c, A, Q, bxl, bxu, bcl, bcu):
    """
    Solves a convex program with a quadratic objective

    maximize    c'*x - (1/2) x'*Q*x
    subject to    bcl <= A*x <= bcu
                  bxl <=  x  <= bxu
    """
    x = cvx.Variable(len(c))
    constraints = [A @ x <= bcu, bcl <= A @ x, bxl <= x, x <= bxu]
    objective = x.T @ c - 0.5 * cvx.quad_form(x, Q)
    ccu.maximize(objective=objective, constraints=constraints)
    return x.value


def solveMarkowitzConstraint(c, A, Q, qc, v, x0, bxl, bxu, bcl, bcu):
    """
    Solves a convex program with a quadratic constraint and linear abs penalty

    maximize     c'*x - v'*abs{x - x0}
    subject to    bcl <= A*x <= bcu
                  bxl <=  x  <= bxu
                sqrt(x'*Q*x) <= qc
    """
    x = cvx.Variable(len(c))
    constraints = [
        A @ x <= bcu,
        bcl <= A @ x,
        bxl <= x,
        x <= bxu,
        cvx.quad_form(x, Q) <= qc * qc,
    ]
    objective = x.T @ c - cvx.abs(x - x0).T @ v
    ccu.maximize(objective=objective, constraints=constraints)
    return x.value


def solveMarkowitzObjective(c, A, Q, v, x0, bxl, bxu, bcl, bcu):
    """
    Solves a convex program with a quadratic constraint and linear abs penalty

    maximize     c'*x - (1/2) x'*Q*x - v'*abs{x - x0}
    subject to    bcl <= A*x <= bcu
                  bxl <=  x  <= bxu
    """
    x = cvx.Variable(len(c))
    constraints = [A @ x <= bcu, bcl <= A @ x, bxl <= x, x <= bxu]
    objective = x.T @ c - 0.5 * cvx.quad_form(x, Q) - cvx.abs(x - x0).T @ v
    ccu.maximize(objective=objective, constraints=constraints, verbose=True)
    return x.value
