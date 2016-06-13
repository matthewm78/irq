class InterruptInfo:
    def __init__(self, irqs):
        self.irqs = irqs

class Irq:
    def __init__(self, irq_num, irq_type, device_name, num_interrupts_per_cpu):
        self.irq_num = irq_num
        self.irq_type = irq_type
        self.device_name = device_name
        self.num_interrupts_per_cpu = num_interrupts_per_cpu
