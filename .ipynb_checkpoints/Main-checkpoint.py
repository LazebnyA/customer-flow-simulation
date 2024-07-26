import datetime as dt
import simpy
import simulation
import helper
import optimization


def input_parameters():
    print("1. Ввести параметри")
    print("2. Завершити виконання програми")


def main_menu():
    print("1. Запустити симуляцію")
    print("2. Оптимізувати параметр кількості автоматів")
    print("3. Завершити виконання програми")


def get_simulation_parameters():
    print()
    print("Введіть параметри: ")
    print("Початковий час симуляції: ")

    start_time_hour = int(input("Введіть годину: "))
    start_time_minute = int(input("Введіть хвилину: "))
    start_time_second = int(input("Введіть секунду: "))

    start_time = dt.time(start_time_hour, start_time_minute, start_time_second)

    simulation_time = int(input("Скільки часу продовжуватиметься симуляція (в годинах): "))

    list_of_hours = [dt.time(start_time_hour + i, start_time_minute, start_time_second) for i in range(simulation_time)]

    n_machines = int(input("Кількість встановлених машин: "))

    print(
        "Список вхідних параметрів лямбда, що позначають інтенсивність потоку клієнтів в годину (починаючи з початкового часу симуляції по-годинно індекс позначає годину з моменту початку симуляції): ")
    arrival_rate_list = [
        int(input(f"Введіть параметр лямбда, що відповідає часу [{i} - {dt.time(i.hour + 1, i.minute, i.second)}] : "))
        for i in list_of_hours]

    service_rate_value = int(input("Скільки клієнтів автомат здатний обслужити за годину: "))
    serving_time = int(input("Скільки часу займає приготування кави: "))

    return [simpy.Environment(),
            simulation_time * 3600,
            start_time,
            n_machines,
            arrival_rate_list,
            service_rate_value,
            serving_time]


def run_simulation_menu(env, simulation_time, start_time, n_machines, arrival_rate_list, service_rate_value,
                        serving_time):
    params_lst = [env,
                  simulation_time,
                  start_time,
                  n_machines,
                  arrival_rate_list,
                  service_rate_value,
                  serving_time,
                  Simulation.ConsoleMessageProcessor()]

    print(params_lst)

    metrics = Simulation.run_simulation(*params_lst)

    print()
    print("1. Вивести дані метрики")
    print("2. Далі")
    user_input = input("")

    if user_input == "1":
        # Вивести дані метрики
        print('_' * 50 + '\nРезультати симуляції: \n')

        print(f"Кількість клієнтів, що прибули: {metrics.arrived_clients}")
        print(f"Кількість обслужених клієнтів: {metrics.served_clients}")
        print(
            f"Максимальний час очікування клієнта: {Helper.normalize_time_value(metrics.get_max_waiting_time()[2])}, о {metrics.get_max_waiting_time()[0]}, біля {metrics.get_max_waiting_time()[1]}-го автомату")
        print(
            f"Мінімальний час очікування клієнта: {Helper.normalize_time_value(metrics.get_min_waiting_time()[2])}, о {metrics.get_min_waiting_time()[0]}, біля {metrics.get_min_waiting_time()[1]}-го автомату")
        print(f"Середній час очікування клієнта: {Helper.normalize_time_value(metrics.get_mean_waiting_time())} с.\n")

        for i in range(n_machines):
            print(
                f"Загальний час ефективної роботи {i + 1}-го автомата: {Helper.normalize_time_value(metrics.get_machine_effective_time(i))} ")

        print()

        for i in range(n_machines):
            print(
                f"Загальний час очікування {i + 1}-го автомата на клієнта\ів: {Helper.normalize_time_value(metrics.get_sum_of_machine_waiting_times(i + 1))} ")

        print()

        for i in range(n_machines):
            print(
                f"Максимальний час очікування {i + 1}-го автомата на клієнта\ів: {Helper.normalize_time_value(metrics.get_max_machine_waiting_time(i + 1)[2])}, клієнт перебив очікування о {metrics.get_max_machine_waiting_time(i + 1)[0]}")

        print()

        for i in range(n_machines):
            print(
                f"Мінімальний час очікування {i + 1}-го автомата на клієнта\ів: {Helper.normalize_time_value(metrics.get_min_machine_waiting_time(i + 1)[2])}, клієнт перебив очікування о {metrics.get_min_machine_waiting_time(i + 1)[0]}")

        print()

        for i in range(n_machines):
            print(
                f"Середній час очікування {i + 1}-го автомата на клієнта\ів: {(Helper.normalize_time_value(metrics.get_mean_machine_waiting_time(i + 1)))}")


def optimize_parameter_menu(*params_list):
    n_max = int(input("Введіть поріг n-кількості машин (n_max): "))

    alpha = float(input("Введіть параметр альфа, що визначає пріоритет мінімізації середнього часу очікування клієнта "
                      "на своє замовлення: alpha = "))
    beta = float(input("Введіть параметр бета, що визначає пріоритет мінімізації середнього часу очікування каво-автомата"
                      "на свого клієнта: beta = "))
    Optimization.optimize(alpha, beta, range(1, n_max+1), *params_list)



class Main:
    while True:
        input_parameters()

        choice = input("Виберіть опцію (1-2): ")

        if choice == "1":

            parameters = get_simulation_parameters()

            while True:
                print()

                main_menu()

                choice = input("Виберіть опцію (1-3): ")

                if choice == "1":
                    run_simulation_menu(*parameters)
                elif choice == "2":
                    print()
                    optimize_parameter_menu(*parameters)
                elif choice == "3":
                    print("Ввести нові параметри симуляції.")
                    break
                else:
                    print("Некоректне введення. Будь ласка, виберіть опцію від 1 до 3.")
        else:
            break
