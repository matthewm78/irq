from irqapi.models import CpuAffinityInfo, IrqInfo, InterruptTotals

class IrqService:

    def __init__(self, proc_interrupts_parser, interrupt_totals_parser, smp_affinity_util):
        self.proc_interrupts_parser = proc_interrupts_parser
        self.interrupt_totals_parser = interrupt_totals_parser
        self.smp_affinity_util = smp_affinity_util

    def get_irqs(self):
        irqs = self.proc_interrupts_parser.parse_file()

        # Set cpu_affinity for IRQs
        for irq in irqs:
            cpu_affinity_info = self.get_irq_cpu_affinity(irq.irq_num)
            irq.cpu_affinity = cpu_affinity_info.cpu_affinity

        totals = self.interrupt_totals_parser.get_totals(irqs)
        irq_info = IrqInfo(irqs, totals)
        return irq_info

    def get_irq_cpu_affinity(self, irq):
        smp_affinity = self.smp_affinity_util.get_irq_smp_affinity(irq)
        return CpuAffinityInfo(irq, smp_affinity)

    def set_irq_cpu_affinity(self, irq, cpu_affinity_mask):
        smp_affinity = self.smp_affinity_util.set_irq_smp_affinity(irq, cpu_affinity_mask)
        return CpuAffinityInfo(irq, smp_affinity)


class InterruptTotalsParser:

    def get_totals(self, irqs):
        num_cpus = len(irqs[0].num_interrupts_per_cpu)

        total_num_interrupts_per_cpu = []
        for cpu_num in range(0, num_cpus):
            curr_cpu_sum = sum([irq.num_interrupts_per_cpu[cpu_num] for irq in irqs])
            total_num_interrupts_per_cpu.append(curr_cpu_sum)

        total_num_interrupts_all_cpus = sum(total_num_interrupts_per_cpu)

        return InterruptTotals(total_num_interrupts_all_cpus, total_num_interrupts_per_cpu)
