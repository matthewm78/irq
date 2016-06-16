from irqapi.models import InterruptTotals

class InterruptTotalsParser:

    def get_totals(self, irqs):
        num_cpus = len(irqs[0].num_interrupts_per_cpu)

        total_num_interrupts_per_cpu = []
        for cpu_num in range(0, num_cpus):
            curr_cpu_sum = sum([irq.num_interrupts_per_cpu[cpu_num] for irq in irqs])
            total_num_interrupts_per_cpu.append(curr_cpu_sum)

        total_num_interrupts_all_cpus = sum(total_num_interrupts_per_cpu)

        return InterruptTotals(total_num_interrupts_all_cpus, total_num_interrupts_per_cpu)
