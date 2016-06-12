import requests


class InterruptTotals:
    def __init__(self, num_cpus, num_interrupts_all_cpus, num_interrupts_per_cpu):
        self.num_cpus = num_cpus
        self.num_interrupts_all_cpus = num_interrupts_all_cpus
        self.num_interrupts_per_cpu = num_interrupts_per_cpu


class IrqServiceApi:
    def __init__(self, host, port=80):
        self.host = host
        self.port = port

    def do_get(self, path):
        url = "http://{}:{}{}".format(self.host, self.port, path)
        response = requests.get(url)
        return response.json()


class IrqClient:

    def __init__(self, api):
        self.api = api

    def get_interrupt_totals(self):
        response_json = self.api.do_get("/interrupts/totals")

        num_cpus = response_json['num_cpus']
        num_interrupts_all_cpus = response_json['num_interrupts_all_cpus']

        num_interrupts_per_cpu = []
        per_cpu_json = response_json['num_interrupts_per_cpu']
        for cpu_num in range(0, num_cpus):
            cpu_interrupts = [x for x in per_cpu_json if x['cpu_num'] == cpu_num][0]
            num_interrupts_per_cpu.append(cpu_interrupts['num_interrupts'])

        return InterruptTotals(
            num_cpus,
            num_interrupts_all_cpus,
            num_interrupts_per_cpu)
