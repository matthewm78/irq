from irqapi.models import CpuAffinityInfo, IrqInfo

class InterruptService:

    def __init__(self, interrupt_tsdb_dao):
        self.interrupt_tsdb_dao = interrupt_tsdb_dao

    def get_interrupts_for_period(self, period_duration_seconds):
        return self.interrupt_tsdb_dao.get_interrupts_for_period(period_duration_seconds)

    def get_interrupts_for_period_for_cpu(self, cpu_num, period_duration_seconds):
        return self.interrupt_tsdb_dao.get_interrupts_for_period_for_cpu(
            cpu_num,
            period_duration_seconds)


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

    def get_interrupt_totals(self):
        irqs = self.proc_interrupts_parser.parse_file()
        totals = self.interrupt_totals_parser.get_totals(irqs)
        return totals

    def get_irq_cpu_affinity(self, irq):
        smp_affinity = self.smp_affinity_util.get_irq_smp_affinity(irq)
        return CpuAffinityInfo(irq, smp_affinity)

    def set_irq_cpu_affinity(self, irq, cpu_affinity_mask):
        smp_affinity = self.smp_affinity_util.set_irq_smp_affinity(irq, cpu_affinity_mask)
        return CpuAffinityInfo(irq, smp_affinity)
