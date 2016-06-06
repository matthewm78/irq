import re

class Irq:
    def __init__(self, irq_num, device_name, irq_type, num_interrupts_per_cpu):
        self.irq_num = irq_num
        self.device_name = device_name
        self.irq_type = irq_type
        self.num_interrupts_per_cpu = num_interrupts_per_cpu

    @property
    def total_num_interrupts(self):
        return sum(self.num_interrupts_per_cpu)

def parse_proc_interrupts_line(interrupts_line):
    print(interrupts_line)
    interrupts_line_regex = re.compile('(\d+):\s+(\d+)\s+(\d+)\s+([\w-]+)\s+(.*)')
    interrupts_line_match = interrupts_line_regex.search(interrupts_line)

    irq_num = interrupts_line_match.group(1)
    device_name = interrupts_line_match.group(5)
    irq_type = interrupts_line_match.group(4)
    num_interrupts_cpu0 = int(interrupts_line_match.group(2))
    num_interrupts_cpu1 = int(interrupts_line_match.group(3))
    num_interrupts_per_cpu = [num_interrupts_cpu0, num_interrupts_cpu1]

    return Irq(irq_num, device_name, irq_type, num_interrupts_per_cpu)