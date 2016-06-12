
class InterruptTotals:
    def __init__(self, num_cpus, num_interrupts_all_cpus, num_interrupts_per_cpu):
        self.num_cpus = num_cpus
        self.num_interrupts_all_cpus = num_interrupts_all_cpus
        self.num_interrupts_per_cpu = num_interrupts_per_cpu


class IrqServiceApi:
    def __init__(self):
        pass

    def do_get(self, path):
        return {}


class IrqClient:

    def __init__(self, api):
        self.api = api

    def get_interrupt_totals(self):
        response_json = self.api.do_get("/interrupts")

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
