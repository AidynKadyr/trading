start_day = "2019-01-01"
forecast_day = "2023-09-01"
dataset_name = "IB_eurpln_2023-09-24.csv"
exp_id = "USDZAR_2"
save = True
position_size = 1000000
commission_per_trade = 27

n_estimators_list = [ 100]
max_depth_list = [6]
eta_list = [0.275, 0.3, 0.325]
gamma_list = [0,1]
min_child_weight_list = [1]
lambda_list = [1, 0.1, 0.5, 0]
alpha_list = [0, 0.1, 0.5, 1]
objective_list = ["reg:squarederror"] #["reg:pseudohubererror", 

weights = True