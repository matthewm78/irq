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

class ProcInterruptsParser:

    def parse_file(self, proc_interrupts_file):
        irqs = []

        with open(proc_interrupts_file) as pif:
            for line in pif:
                tmp_irq = self.parse_line(line)
                irqs.append(tmp_irq)

        return irqs

    def parse_line(self, interrupts_line):
        interrupts_line_regex = re.compile('(\d+):\s+(\d+)\s+(\d+)\s+([\w-]+)\s+(.*)')
        interrupts_line_match = interrupts_line_regex.search(interrupts_line)

        irq_num = interrupts_line_match.group(1)
        device_name = interrupts_line_match.group(5)
        irq_type = interrupts_line_match.group(4)
        num_interrupts_cpu0 = int(interrupts_line_match.group(2))
        num_interrupts_cpu1 = int(interrupts_line_match.group(3))
        num_interrupts_per_cpu = [num_interrupts_cpu0, num_interrupts_cpu1]

        return Irq(irq_num, device_name, irq_type, num_interrupts_per_cpu)

if __name__ == '__main__':
    import sys

    proc_interrupts_file = sys.argv[1]

    proc_interrupts_parser = ProcInterruptsParser()
    parsed_irqs = proc_interrupts_parser.parse_irqs(proc_interrupts_file)

    irq_balancer = IrqBalancer()
    balance_irqs_out = irq_balancer.balance(parsed_irqs)

    print(balance_irqs_out)
