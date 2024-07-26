import simpy


class Metrics:
    def __init__(self, simulation_time: int, machines=None):
        if machines is None:
            machines = []
        self.arrived_clients = 0
        self.served_clients = 0
        self.client_waiting_times = []
        self.machine_effective_times = {}
        self.machine_waiting_times = {}
        self.simulation_time = simulation_time
        self.machines = machines

    def record_client(self):
        self.arrived_clients += 1

    def record_service(self, current_time, machine_id, client_waiting_time):
        self.served_clients += 1
        self.client_waiting_times.append((current_time, machine_id, client_waiting_time))

    def init_machine_effective_times(self):
        for machine in self.machines:
            if machine not in self.machine_effective_times:
                self.machine_effective_times[machine] = 0

    def record_machine_effective_time(self, machine: simpy.Resource, effective_time: int):
        if machine in self.machine_effective_times:
            self.machine_effective_times[machine] += effective_time
        else:
            self.machine_effective_times[machine] = effective_time

    def get_machine_effective_time(self, machine_id):
        effective_time = list(self.machine_effective_times.values())[machine_id]
        return effective_time

    def init_machine_waiting_times(self, time):
        for machine in self.machines:
            self.machine_waiting_times[machine] = [(time, (self.machines.index(machine) + 1), 0)]

    def record_machine_waiting_time(self, current_time, machine: simpy.Resource, waiting_time):
        if machine in self.machine_waiting_times:
            self.machine_waiting_times[machine].append((current_time, (self.machines.index(machine) + 1), waiting_time))

    def get_sum_of_machine_waiting_times(self, machine_id):
        times = []
        for time in list(self.machine_waiting_times.values())[machine_id - 1]:
            times.append(time[2])
        return sum(times)

    def get_max_machine_waiting_time(self, machine_id):
        times = []
        for time in list(self.machine_waiting_times.values())[machine_id - 1]:
            times.append(time[2])
        return list(self.machine_waiting_times.values())[machine_id - 1][times.index(max(times))]

    def get_min_machine_waiting_time(self, machine_id):
        times = []
        for time in list(self.machine_waiting_times.values())[machine_id - 1][1:]:
            if time[2] == 0:
                continue
            times.append(time[2])
        return list(self.machine_waiting_times.values())[machine_id - 1][times.index(min(times), 0, len(times) - 1)]

    def get_mean_machine_waiting_time(self, machine_id):
        times = []
        for time in list(self.machine_waiting_times.values())[machine_id - 1][1:]:
            if time[2] == 0:
                continue
            times.append(time[2])
        mean = round((sum(times) / len(times)), 2)
        return mean

    def get_total_clients_served(self):
        return self.served_clients

    def get_max_waiting_time(self):
        times = []
        for time in self.client_waiting_times:
            times.append(time[2])
        return self.client_waiting_times[times.index(max(times))]

    def get_min_waiting_time(self):
        times = []
        for time in self.client_waiting_times:
            times.append(time[2])
        return self.client_waiting_times[times.index(min(times))]

    def get_mean_waiting_time(self):
        times = []
        for time in self.client_waiting_times:
            times.append(time[2])
        mean_time = int(sum(times) / len(times))
        return mean_time
