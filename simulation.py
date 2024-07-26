import metrics
import simpy
from scipy.optimize import shgo
import numpy as np
import datetime as dt
from typing import List
import helper


# np.random.seed(123123123)


def generate_exp_rand_value(lambda_value):
    return round(
        np.random.exponential(1 / lambda_value) * 3600
    )


def find_best_machine(machines, remaining_times):
    min_time = remaining_times[machines[np.random.randint(0, len(machines))]]
    best_machine = machines[np.random.randint(0, len(machines))]

    for machine in machines:
        if remaining_times[machine] < min_time:
            min_time = remaining_times[machine]
            best_machine = machine

    # indices = []
    # if min_time == 0:
    #     for machine in machines:
    #         if remaining_times[machine] == 0:
    #             indices +=
    #     best_machine = machines[np.random.randint(0, count)]


    return best_machine


class MachineStatus:
    def __init__(self):
        self.last_service_start = 0


class MessageProcessor:
    def __init__(self, ):
        pass

    def process(self, message):
        pass

    def stop(self):
        pass


class ConsoleMessageProcessor(MessageProcessor):
    def __init__(self):
        super().__init__()

    def process(self, message):
        print(message)

    def stop(self):
        pass


def consider_process(env, start_time, simulation_time, machine_statuses, metrics_monitor, machines, remaining_times, update_time):
    while True:

        yield env.timeout(update_time)

        for machine in machines:

            remaining_service_time = remaining_times[machine]

            if remaining_service_time > 0:
                remaining_times[machine] -= update_time

        if simulation_time - env.now == 1:
            for i in range(len(machines)):
                waiting_time = max(0, env.now - machine_statuses[i].last_service_start)
                metrics_monitor.record_machine_waiting_time(Helper.desc_seconds(start_time, env.now), machines[i],
                                                            waiting_time)


def serve_customer(
        env,
        cust_id,
        machine,
        machine_id,
        service_time,
        start_time,
        metrics_monitor: Metrics,
        message_processor: MessageProcessor
):
    arrival_time = env.now
    message = f"Клієнт #{cust_id} встає в чергу о {Helper.desc_seconds(start_time, arrival_time)}\n"
    message_processor.process(message)

    with machine.request() as request:
        yield request

        service_start_time = env.now

        waiting_time = (service_start_time - arrival_time)

        message = f"Клієнт #{cust_id} встає біля автомату #{machine_id}, щоб зробити замовлення о {Helper.desc_seconds(start_time, service_start_time)}\n"
        message_processor.process(message)
        yield env.timeout(service_time)

        metrics_monitor.record_machine_effective_time(machine, service_time)
        metrics_monitor.record_service(Helper.desc_seconds(start_time, env.now), machine_id,
                                       service_time + waiting_time)

        message = f"Клієнт #{cust_id} отримав своє замовлення о {Helper.desc_seconds(start_time, env.now)} від автомату під номером #{machine_id}\n"
        message_processor.process(message)


def queue_system(
        env,
        machine_statuses,
        lambda_clients_flow,
        service_rate,
        serving_time,
        machines,
        remaining_times,
        start_time,
        metrics_monitor: Metrics,
        message_processor: MessageProcessor
):
    cust_id = 0

    while True:

        for i in range(start_time.hour, start_time.hour + len(lambda_clients_flow)):
            if dt.time(i, start_time.minute, start_time.second) <= Helper.desc_seconds_value(start_time, env.now).time() < dt.time(i + 1, start_time.minute, start_time.second):
                yield env.timeout(generate_exp_rand_value(lambda_clients_flow[i - start_time.hour]))

        cust_id += 1
        metrics_monitor.record_client()

        best_machine = find_best_machine(machines, remaining_times)
        machine_id = machines.index(best_machine)

        service_time = serving_time + generate_exp_rand_value(service_rate)

        waiting_time = max(0, env.now - machine_statuses[machine_id].last_service_start)

        metrics_monitor.record_machine_waiting_time(Helper.desc_seconds(start_time, env.now), best_machine,
                                                    waiting_time)
        machine_statuses[machine_id].last_service_start = env.now + service_time

        remaining_times[best_machine] += service_time

        env.process(
            serve_customer(
                env,
                cust_id,
                best_machine,
                machine_id + 1,
                service_time,
                start_time,
                metrics_monitor,
                message_processor
            )
        )




def simulation_process(
        env: simpy.Environment,
        simulation_time: int,
        arrival_rate,
        service_rate,
        serving_time,
        machines,
        remaining_times,
        start_time,
        metrics_monitor: Metrics,
        message_processor: MessageProcessor
):
    machine_statuses = [MachineStatus() for _ in range(len(machines))]

    env.process(
        queue_system(
            env,
            machine_statuses,
            arrival_rate,
            service_rate,
            serving_time,
            machines,
            remaining_times,
            start_time,
            metrics_monitor,
            message_processor
        )
    )
    env.process(
        consider_process(env, start_time, simulation_time, machine_statuses, metrics_monitor, machines, remaining_times, 1)
    )
    env.run(until=simulation_time)
    message_processor.process("Симуляція завершена!")


def run_simulation(
        env: simpy.Environment(),
        simulation_time: int,
        start_time: dt.time,
        n_machines: int,
        arrival_rate: List[float],
        service_rate: float,
        serving_time: float,
        message_processor: MessageProcessor
):
    metrics_monitor = Metrics.Metrics(simulation_time)

    machines = [simpy.Resource(env, capacity=1) for i in range(n_machines)]
    metrics_monitor.machines = machines

    metrics_monitor.init_machine_effective_times()
    metrics_monitor.init_machine_waiting_times(start_time)

    remaining_times = {}
    for machine in machines:
        remaining_times[machine] = 0

    simulation_process(
        env,
        simulation_time,
        arrival_rate,
        service_rate,
        serving_time,
        machines,
        remaining_times,
        start_time,
        metrics_monitor,
        message_processor
    )

    message_processor.stop()

    return metrics_monitor


def run_simulation_and_get_values_to_optimize(env, simulation_time, start_time, n, arrival_rate_list, service_rate_value, serving_time):

    new_metrics = run_simulation(
        env=simpy.Environment(),
        simulation_time=simulation_time,
        start_time=start_time,
        n_machines=n,
        arrival_rate=arrival_rate_list,
        service_rate=service_rate_value,
        serving_time=serving_time,
        message_processor=MessageProcessor()
    )

    lst_of_values = []
    for i in range(n):
        lst_of_values.append(new_metrics.get_mean_machine_waiting_time(i + 1))

    mean_clients_waiting_times = new_metrics.get_mean_waiting_time()
    mean_machines_waiting_times = sum(lst_of_values)/len(lst_of_values)

    return mean_clients_waiting_times, mean_machines_waiting_times
