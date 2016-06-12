
class CpuInterruptCount:
    def __init__(self, cpu_num, num_interrupts):
        self.cpu_num = cpu_num
        self.num_interrupts = num_interrupts


class InterruptTotals:
    def __init__(self, num_cpus, num_interrupts_all_cpus, cpu_interrupt_counts):
        self.num_cpus = num_cpus
        self.num_interrupts_all_cpus = num_interrupts_all_cpus
        self.cpu_interrupt_counts = cpu_interrupt_counts

    def get_interrupts_for_cpu(self, cpu_num):
        return [cic for cic in self.cpu_interrupt_counts if cic.cpu_num == cpu_num][0].num_interrupts

class IrqClient:

    def __init__(self, api):
        self.api = api

    def get_interrupt_totals(self):
        response = self.api.do_get("/interrupts")
        response_json = response.get_json()

        cpu_interrupt_counts = []
        num_interrupts_per_cpu_json = response_json['num_interrupts_per_cpu']
        for cpu_json in num_interrupts_per_cpu_json:
            cpu_interrupt_counts.append(CpuInterruptCount(
                cpu_json['cpu_num'],
                cpu_json['num_interrupts']))

        return InterruptTotals(
            len(cpu_interrupt_counts),
            response_json['num_interrupts_all_cpus'],
            cpu_interrupt_counts)
