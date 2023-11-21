import numpy as np
import cvxpy as cp
# need to be fixed: param_lasso_1, param_lasso_2, vaout_intercept_rampupi_1, vaout_intercept_rampupi_2
# EFFICIENCY_RATE = 1, param_storage_cap, param_storage, param_charge_cap, param_charge
import logging
from cvxpy import ECOS

# Create and configure logger
logging.basicConfig(format='%(asctime)s %(message)s')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


def inverseOptimizationSolver(data, X_train, start_date_train, finish_date_train, param_lasso_1, param_lasso_2):
    data = data
    features = X_train

    NUM_TECH = data['param_generation_cap'].shape[1]
    NUM_PERIOD = features.shape[0]
    NUM_FEATURES = features.shape[1]
    EFFICIENCY_RATE = 1

    set_tech = list(range(NUM_TECH))
    set_period = list(range(NUM_PERIOD))
    set_features = list(range(NUM_FEATURES))

    # Parameters
    param_features = features.values.transpose()
    param_real_prices = data['param_real_prices'][start_date_train:finish_date_train].values.ravel()
    param_charge_cap = 3 * np.ones(NUM_PERIOD)
    param_discharge_cap = 3 * np.ones(NUM_PERIOD)
    param_charge = np.random.uniform(0, 3.0001, size=NUM_PERIOD)
    param_discharge = np.random.uniform(0, 3.0001, size=NUM_PERIOD)
    param_storage_cap = (10 ** 6) * np.ones(NUM_PERIOD)
    param_storage = np.random.uniform(0.4 * (10 ** 6), 0.8 * (10 ** 6), size=NUM_PERIOD)
    param_generation_cap = data['param_generation_cap'][start_date_train:finish_date_train].values.transpose()
    param_generation = data['param_generation'][start_date_train:finish_date_train].values.transpose()
    param_rampups = np.maximum(np.diff(param_generation, axis=1), 0)  # ramp-ups
    param_rampdowns = np.maximum(np.diff(-param_generation, axis=1), 0)  # ramp-downs
    param_rampup_cap = np.max(param_rampups, axis=1)
    param_rampdown_cap = np.max(param_rampdowns, axis=1)

    # Subsets
    u_alpha_d, u_alpha_t = np.column_stack(np.where(param_generation > 0)), np.column_stack(
        np.where(param_generation < param_generation_cap))
    u_yp_d, u_yp_t = np.column_stack(np.where(param_charge > 0)), np.column_stack(
        np.where(param_charge < param_charge_cap))
    u_yn_d, u_yn_t = np.column_stack(np.where(param_discharge > 0)), np.column_stack(
        np.where(param_discharge < param_discharge_cap))
    u_beta_d, u_beta_t = np.column_stack(np.where(param_storage > 0)), np.column_stack(
        np.where(param_storage < param_storage_cap))
    u_delta_d, u_delta_t = np.column_stack(np.where(param_rampups > 0.01)), np.column_stack(
        np.where(param_rampups < (0.98 * param_rampup_cap[:, np.newaxis])))
    u_theta_d, u_theta_t = np.column_stack(np.where(param_rampdowns > 0.01)), np.column_stack(
        np.where(param_rampdowns < (0.98 * param_rampdown_cap[:, np.newaxis])))
    u_beta_d = u_beta_d.flatten()
    u_beta_t = u_beta_t.flatten()
    u_yp_d = u_yp_d.flatten()
    u_yp_t = u_yp_t.flatten()
    u_yn_d = u_yn_d.flatten()
    u_yn_t = u_yn_t.flatten()

    # Variables
    var_marginal_cost_1 = cp.Variable((len(set_tech), len(set_period)), nonneg=True)
    var_marginal_cost_2 = cp.Variable((len(set_tech), len(set_period)), nonneg=True)
    var_q = cp.Variable(len(set_tech), nonneg=True)
    var_rampup_cost = cp.Variable((len(set_tech), len(set_period)), nonneg=True)
    var_overline_alpha = cp.Variable((len(set_tech), len(set_period)), nonneg=True)
    var_underline_alpha = cp.Variable((len(set_tech), len(set_period)), nonneg=True)
    var_overline_beta = cp.Variable(len(set_period), nonneg=True)
    var_underline_beta = cp.Variable(len(set_period), nonneg=True)
    var_pi_1 = cp.Variable(len(set_period), nonneg=True)
    var_pi_2 = cp.Variable(len(set_period), nonneg=True)
    var_mu_1 = cp.Variable((len(set_tech), len(set_period)), nonneg=True)
    var_mu_2 = cp.Variable((len(set_tech), len(set_period)), nonneg=True)
    var_overline_delta = cp.Variable((len(set_tech), len(set_period)), nonneg=True)
    var_underline_delta = cp.Variable((len(set_tech), len(set_period)), nonneg=True)
    var_overline_theta = cp.Variable((len(set_tech), len(set_period)), nonneg=True)
    var_underline_theta = cp.Variable((len(set_tech), len(set_period)), nonneg=True)
    var_overline_gamma_neg = cp.Variable(len(set_period), nonneg=True)
    var_underline_gamma_neg = cp.Variable(len(set_period), nonneg=True)
    var_overline_gamma_pos = cp.Variable(len(set_period), nonneg=True)
    var_underline_gamma_pos = cp.Variable(len(set_period), nonneg=True)
    var_coef_marginal_1 = cp.Variable((len(set_tech), len(set_features)), nonneg=True)
    var_coef_marginal_2 = cp.Variable((len(set_tech), len(set_features)), nonneg=True)
    var_intercept_marginal = cp.Variable(len(set_tech), nonneg=True)
    var_coef_rampup_1 = cp.Variable((len(set_tech), len(set_features)), nonneg=True)
    var_coef_rampup_2 = cp.Variable((len(set_tech), len(set_features)), nonneg=True)
    var_intercept_rampup = cp.Variable(len(set_tech), nonneg=True)
    var_epsilon_1 = cp.Variable((len(set_tech), len(set_period)), nonneg=True)
    var_epsilon_2 = cp.Variable((len(set_tech), len(set_period)), nonneg=True)
    var_epsilon_prime_1 = cp.Variable((len(set_tech), len(set_period)), nonneg=True)
    var_epsilon_prime_2 = cp.Variable((len(set_tech), len(set_period)), nonneg=True)

    logger.info("starting to read obj of InverseModel")
    objective = cp.Minimize(
        cp.sum((var_coef_marginal_1 + var_coef_marginal_2 + var_intercept_marginal[:,
                                                            np.newaxis])) +
        cp.sum((var_coef_rampup_1 + var_coef_rampup_2 + var_intercept_rampup[:,
                                                        np.newaxis])) +
        cp.sum(var_epsilon_1 + var_epsilon_2 + var_epsilon_prime_1 + var_epsilon_prime_2)
    )
    logger.info("reading obj of InverseModel is finished")
    # Constraints
    logger.info("starting to read constrs of InverseModel")
    constraints = [
        var_marginal_cost_1 - var_marginal_cost_2 ==
        (var_coef_marginal_1 - var_coef_marginal_2) @ param_features +
        var_intercept_marginal[:, np.newaxis] +
        var_epsilon_1 - var_epsilon_2
    ]  # marginal_cost_1

    constraints += [
        var_rampup_cost ==
        (var_coef_rampup_1 - var_coef_rampup_2) @ param_features +
        var_intercept_rampup[:, np.newaxis] +
        var_epsilon_prime_1 - var_epsilon_prime_2
    ]  # rampup_cost

    constraints += [
        var_marginal_cost_1[:, :-1] - var_marginal_cost_2[:, :-1] -
        # + (2 * var_q[:, np.newaxis].T @ param_generation[:, :-1]) -
        param_real_prices[np.newaxis, :-1] -
        var_underline_alpha[:, :-1] + var_overline_alpha[:, :-1]
        - var_mu_1[:, :-1] + var_mu_2[:, :-1] +
        var_mu_1[:, 1:] - var_mu_2[:, 1:] == 0
    ]  # C1

    constraints += [
        param_real_prices -
        EFFICIENCY_RATE * (var_pi_1 - var_pi_2) -
        var_underline_gamma_pos + var_overline_gamma_pos == 0
    ]  # C2

    constraints += [
        -param_real_prices +
        (1 / EFFICIENCY_RATE) * (var_pi_1 - var_pi_2) -
        var_underline_gamma_neg + var_overline_gamma_neg == 0
    ]  # C3

    constraints += [
        var_pi_1[:-1] - var_pi_2[:-1] -
        var_pi_1[1:] + var_pi_2[1:] +
        var_underline_beta[:-1] - var_overline_beta[:-1] == 0
    ]  # C4

    constraints += [
        var_pi_1[NUM_PERIOD - 1] -
        var_pi_2[NUM_PERIOD - 1] +
        var_underline_beta[NUM_PERIOD - 1] -
        var_overline_beta[NUM_PERIOD - 1] == 0
    ]  # C5

    constraints += [
        var_underline_alpha[list(u_alpha_d[:, 0]), list(u_alpha_d[:, 1])] == 0
    ]  # C6

    constraints += [
        var_overline_alpha[list(u_alpha_t[:, 0]), list(u_alpha_t[:, 1])] == 0
    ]  # C7

    constraints += [
        var_underline_beta[list(u_beta_d)] == 0
    ]  # C12

    constraints += [
        var_overline_beta[list(u_beta_t)] == 0
    ]  # C13

    constraints += [
        var_mu_1 - var_mu_2 +
        var_overline_delta - var_underline_delta +
        var_rampup_cost == 0
    ]  # C14

    constraints += [
        -var_mu_1 + var_mu_2 +
        var_overline_theta - var_underline_theta == 0
    ]  # C15

    constraints += [
        var_overline_delta[list(u_delta_t[:, 0]), list(u_delta_t[:, 1])] == 0
    ]  # C16

    constraints += [
        var_underline_delta[list(u_delta_d[:, 0]), list(u_delta_d[:, 1])] == 0
    ]  # C17

    constraints += [
        var_overline_theta[list(u_theta_t[:, 0]), list(u_theta_t[:, 1])] == 0
    ]  # C18

    constraints += [
        var_underline_theta[list(u_theta_d[:, 0]), list(u_theta_d[:, 1])] == 0
    ]  # C19

    logger.info("reading constrs of InverseModel is finished")

    logger.info("pushing the obj and constrs into the problem instance")
    # Create problem and solve
    problem = cp.Problem(objective, constraints)
    logger.info("attempting to solve")
    # problem.solve(solver=cp.ECOS)

    problem.solve(solver=cp.OSQP, verbose=True, eps_abs=.1, eps_rel=.1)

    dict_inverseModel = {
        "out_inverse_obj_value": problem.objective.value,
        "out_q": var_q.value,
        "out_marginal_cost_train": var_marginal_cost_1.value - var_marginal_cost_2.value,
        "out_rampup_cost_train": var_rampup_cost.value,
        "out_coef_marginal": var_coef_marginal_1.value - var_coef_marginal_2.value,
        "out_intercept_marginal": var_intercept_marginal,
        "out_coef_rampup": var_coef_rampup_1 - var_coef_rampup_2,
        "out_intercept_rampup": var_intercept_rampup,
        "out_rampup_cap": param_rampup_cap,
        "out_rampdown_cap": param_rampdown_cap
    }

    return dict_inverseModel
