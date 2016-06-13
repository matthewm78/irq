import re

class Irq:
    def __init__(self, irq_num, irq_type, device_name, num_interrupts_per_cpu):
        self.irq_num = irq_num
        self.irq_type = irq_type
        self.device_name = device_name
        self.num_interrupts_per_cpu = num_interrupts_per_cpu


class ProcInterruptsParser:

    def __init__(self, num_cpus):
        self.num_cpus = num_cpus

    def parse_file(self, proc_interrupts_file):
        parsed_irqs = []

        with open(proc_interrupts_file) as pif:
            for line in pif:
                parsed_irq = self.parse_line(line)
                parsed_irqs.append(parsed_irq)

        return parsed_irqs

    def parse_line(self, interrupts_line):
        cpu_regex = '(\d+)\s+' * self.num_cpus
        interrupts_line_regex = '(\d+):\s+{}([\w-]+)\s+(.*)'.format(cpu_regex)

        interrupts_line_compiled = re.compile(interrupts_line_regex)
        interrupts_line_match = interrupts_line_compiled.search(interrupts_line)

        irq_num = interrupts_line_match.group(1)
        irq_type = interrupts_line_match.group(2 + self.num_cpus)
        device_name = interrupts_line_match.group(3 + self.num_cpus)

        num_interrupts_per_cpu = []
        for cpu_num in range(0, self.num_cpus):
            tmp_cpu_interrupts = int(interrupts_line_match.group(2 + cpu_num))
            num_interrupts_per_cpu.append(tmp_cpu_interrupts)

        return Irq(irq_num, irq_type, device_name, num_interrupts_per_cpu)
