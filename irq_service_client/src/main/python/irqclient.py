
class IrqServiceResponse:
    def __init__(self, response_json):
        self.response_json = response_json

class CpuInterrupts:
    def __init__(self, cpu_num, num_interrupts):
        self.cpu_num = cpu_num
        self.num_interrupts = num_interrupts

class InterruptTotals:
    def __init__(self, interrupt_totals_json):
        self.num_interrupts_all_cpus = interrupt_totals_json['num_interrupts_all_cpus']

        num_interrupts_per_cpu = []
        num_interrupts_per_cpu_json = interrupt_totals_json['num_interrupts_per_cpu']
        for cpu_interrupts in num_interrupts_per_cpu_json:
            num_interrupts_per_cpu.append(CpuInterrupts(
                cpu_interrupts['cpu_num'],
                cpu_interrupts['num_interrupts']))

        self.num_interrupts_per_cpu = num_interrupts_per_cpu

class IrqClient:
    def __init__(self, api):
        self.api = api

    def get_interrupt_totals(self):
        response = self.api.do_get("/interrupts")
        response_json = response.get_json()

        return InterruptTotals(response_json)