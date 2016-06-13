class InterruptInfo:
    def __init__(self, irqs, totals):
        self.irqs = irqs
        self.totals = totals


class InterruptTotals:
    def __init__(self, num_interrupts_all_cpus, num_interrupts_per_cpu):
        self.num_interrupts_all_cpus = num_interrupts_all_cpus
        self.num_interrupts_per_cpu = num_interrupts_per_cpu


class Irq:
    def __init__(self, irq_num, irq_type, device_name, num_interrupts_per_cpu):
        self.irq_num = irq_num
        self.irq_type = irq_type
        self.device_name = device_name
        self.num_interrupts_per_cpu = num_interrupts_per_cpu
