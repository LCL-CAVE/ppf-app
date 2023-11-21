import time
import cvxpy as cp
import numpy as np
from cvxpy import OSQP


# need to be fixed:
# EFFICIENCY_RATE = 1, param_charge_cap, param_storage_cap

def forwardOptimizationSolver(data, X_test, dict_inverseModel, start_date_test, finish_date_test):
    data = data
    features = X_test

    NUM_TECH = data['param_generation_cap'].shape[1]
    NUM_PERIOD = features.shape[0]
    NUM_FEATURES = features.shape[1]
    EFFICIENCY_RATE = 1

    # Parameters
    param_charge_cap = 3 * np.ones(NUM_PERIOD)
    param_discharge_cap = 3 * np.ones(NUM_PERIOD)
    param_storage_cap = (10 ** 6) * np.ones(NUM_PERIOD)
    param_demand = data['param_demand'][start_date_test:finish_date_test].values
    param_demand = np.ravel(param_demand)
    param_generation_cap = data['param_generation_cap'][start_date_test:finish_date_test].values.T
    # param_rampup_cap = np.tile(dict_inverseModel['out_rampup_cap'], (1, NUM_PERIOD)).reshape((NUM_TECH, NUM_PERIOD))
    param_rampup_cap = np.tile(dict_inverseModel['out_rampup_cap'][:, np.newaxis], (1, NUM_PERIOD))
    # param_rampdown_cap = np.tile(dict_inverseModel['out_rampdown_cap'], (1, NUM_PERIOD)).reshape((NUM_TECH, NUM_PERIOD))
    param_rampdown_cap = np.tile(dict_inverseModel['out_rampdown_cap'][:, np.newaxis], (1, NUM_PERIOD))
    param_coef_marginal = dict_inverseModel['out_coef_marginal']
    param_coef_rampup = dict_inverseModel['out_coef_rampup']
    param_marginal_cost = (np.inner(dict_inverseModel['out_coef_marginal'], features))  # + (b_pp.transpose())
    param_rampup_cost = (np.inner(dict_inverseModel['out_coef_rampup'], features))  # + (b_rr.transpose())
    param_q = dict_inverseModel['out_q']

    # Variables
    var_generation = cp.Variable((NUM_TECH, NUM_PERIOD), nonneg=True)
    var_storage_level = cp.Variable(NUM_PERIOD, nonneg=True)
    var_charge_cap = cp.Variable(NUM_PERIOD, nonneg=True)
    var_discharge_cap = cp.Variable(NUM_PERIOD, nonneg=True)
    var_ramp_up = cp.Variable((NUM_TECH, NUM_PERIOD), nonneg=True)
    var_ramp_down = cp.Variable((NUM_TECH, NUM_PERIOD), nonneg=True)

    objective = cp.Minimize(cp.sum(cp.multiply(param_marginal_cost, var_generation)))
    # + cp.sum(cp.multiply(param_q, var_generation ** 2))
    # + cp.sum(cp.multiply(param_rampup_cost, var_ramp_up)))

    # Constraints
    constraints = [
        var_generation <= param_generation_cap
    ]

    constraints += [
        cp.sum(var_generation, axis=0) <= param_demand
    ]

    constraints += [
        cp.sum(var_generation, axis=0) >= param_demand - .01
    ]

    constraints += [
        var_discharge_cap[0] == 0
    ]

    constraints += [
        var_charge_cap[0] == 0
    ]

    constraints += [
        var_storage_level[0] == 0.5 * param_storage_cap[0]
    ]

    constraints += [
        var_ramp_down[:, 0] == 0
    ]

    constraints += [
        var_ramp_up[:, 0] == 0
    ]

    constraints += [
        var_storage_level <= param_storage_cap
    ]

    constraints += [
        var_discharge_cap <= param_discharge_cap
    ]

    constraints += [
        var_charge_cap <= param_charge_cap
    ]

    constraints += [
        var_ramp_down <= param_rampdown_cap
    ]

    constraints += [
        var_ramp_up <= param_rampup_cap
    ]

    constraints += [
        cp.sum(var_generation, axis=0) + var_discharge_cap - var_charge_cap <= param_demand
    ]

    constraints += [
        cp.sum(var_generation, axis=0) + var_discharge_cap - var_charge_cap >= param_demand - .01
    ]

    constraints += [
        cp.diff(var_storage_level, k=1) <= EFFICIENCY_RATE * var_charge_cap[1:] - (
                1 / EFFICIENCY_RATE) * var_charge_cap[1:]
    ]

    constraints += [
        cp.diff(var_storage_level, k=1) >= EFFICIENCY_RATE * var_charge_cap[1:] - (
                1 / EFFICIENCY_RATE) * var_charge_cap[1:] - .01
    ]

    # constraints += [
    #     cp.diff(var_generation, k=1, axis=1) <= var_ramp_up[:, 1:] - var_ramp_down[:, 1:]
    #     ]
    #
    # constraints += [
    #     cp.diff(var_generation, k=1, axis=1) >= var_ramp_up[:, 1:] - var_ramp_down[:, 1:] - .01
    #     ]

    # Create problem and solve
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.ECOS)
    # problem.solve(solver=cp.OSQP, verbose=True, eps_abs=.1, eps_rel=.1)
    # problem.solve(solver=cp.GUROBI, verbose=True, abstol=.1)

    dict_forwardModel = {
        "out_predicted_prices": constraints[2].dual_value,
        "out_forward_obj_value": problem.objective.value,
        "out_generation": var_generation.value,
        "out_storage_level": var_storage_level.value,
        "out_charge_cap": var_charge_cap.value,
        "out_discharge_cap": var_discharge_cap.value
    }

    return dict_forwardModel
