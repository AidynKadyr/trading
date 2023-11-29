import numpy as np
import itertools


def get_all_params(
    n_estimators_list,
    max_depth_list,
    eta_list,
    gamma_list,
    min_child_weight_list,
    lmbda_list,
    alpha_list,
    objective_list
):
    """Return a list of all possible combinations of hyperparameters.

    Args:
        n_estimators_list (list): List of integers representing number of trees in the forest.
        max_depth_list (list): List of integers representing maximum depth of the trees.
        eta_list (list): List of floats representing learning rate.
        gamma_list (list): List of floats representing minimum loss reduction required to split a leaf.
        min_child_weight_list (list): List of floats representing minimum sum of instance weight required in a child.
        lmbda_list (list): List of floats representing L2 regularization term on weights.
        alpha_list (list): List of floats representing L1 regularization term on weights.

    Returns:
        list: A list of dictionaries, where each dictionary
        represents a combination of hyperparameters.
    """
    # Generate all possible combinations of hyperparameters
    hyperparameter_combinations = list(
        itertools.product(
            n_estimators_list,
            max_depth_list,
            eta_list,
            gamma_list,
            min_child_weight_list,
            lmbda_list,
            alpha_list,
            objective_list,
        )
    )
    # Convert each combination to a dictionary with named hyperparameters
    hyperparameters_list = [
        {
            "n_estimators": n_estimators_choice,
            "max_depth": max_depth_choice,
            "eta": eta_choice,
            "gamma": gamma_choice,
            "min_child_weight": min_child_weight_choice,
            "lambda": lmbda_choice,
            "alpha": alpha_choice,
            "objective":objective_choice
        }
        for n_estimators_choice, max_depth_choice, eta_choice, 
        gamma_choice, min_child_weight_choice, lmbda_choice, 
        alpha_choice, objective_choice in hyperparameter_combinations
    ]
    return hyperparameters_list



