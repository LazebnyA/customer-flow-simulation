import simulation


def get_mean(lst):
    return sum(lst) / len(lst)


def generate_machines_mean_client_waiting_times_dict(n_range, *params_list):
    map_to_return = {}

    p_list = list(params_list)

    for i in n_range:
        p_list[3] = i

        print(f"n={i}\n")
        lst_of_values = []
        for j in range(50):
            print(f"Значення середнього часу очікування клієнта для {j+1}-ої симуляції = {Simulation.run_simulation_and_get_values_to_optimize(*p_list)[0]}")
            print(
                f"Значення середнього часу очікування автомата для {j+1}-ої симуляції = {Simulation.run_simulation_and_get_values_to_optimize(*p_list)[1]}\n")
            lst_of_values.append(Simulation.run_simulation_and_get_values_to_optimize(*p_list))
        map_to_return[i] = get_mean([item[0] for item in lst_of_values]), get_mean([item[1] for item in lst_of_values])
    return map_to_return


# cwt - clients waiting times
# mwt - machines waiting times
def get_optimal_n_machines(n_dict, alpha, beta):
    values = list(n_dict.values())
    loss_functions = [alpha * values[i][0] + beta * values[i][1] for i in range(len(values))]

    min_loss = min(loss_functions)
    min_index = loss_functions.index(min_loss)
    optimal_n = list(n_dict.keys())[min_index]

    return optimal_n



def optimize(alpha, beta, n_range, *params_lst):
    # Alpha - priority of minimizing mean_client_waiting_time
    # Beta  - priority of minimizing mean_machines_waiting_time

    n_dict = generate_machines_mean_client_waiting_times_dict(n_range, *params_lst)

    print()

    print("Результати експерименту: ")
    for n in list(n_dict.keys()):
        print(f"    Середній час очікування клієнта для n = {n}:  {n_dict[n][0]} с.")
        print(f"    Середній час очікування автомата для n = {n}:  {round(n_dict[n][1], 2)} с.\n")

    print()
    print(
        f"Оптимальна кількість каво-машин для мінімізації цих показників (для параметрів alpha = {alpha}; beta = {beta})\nn_optimal = {get_optimal_n_machines(n_dict, alpha, beta)}")
