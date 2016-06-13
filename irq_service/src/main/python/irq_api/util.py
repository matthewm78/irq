import re
from irq_api.common import InterruptInfo, InterruptTotals, Irq

class IrqService:
    def __init__(self, proc_interrupts_parser, interrupt_totals_parser):
        self.proc_interrupts_parser = proc_interrupts_parser
        self.interrupt_totals_parser = interrupt_totals_parser

    def get_interrupts(self):
        irqs = self.proc_interrupts_parser.parse_file()
        totals = self.interrupt_totals_parser.get_totals(irqs)
        interrupt_info = InterruptInfo(irqs, totals)
        return interrupt_info


class InterruptTotalsParser:

    def get_totals(self, irqs):
        num_cpus = len(irqs[0].num_interrupts_per_cpu)

        total_num_interrupts_per_cpu = []
        for cpu_num in range(0, num_cpus):
            curr_cpu_sum = sum([irq.num_interrupts_per_cpu[cpu_num] for irq in irqs])
            total_num_interrupts_per_cpu.append(curr_cpu_sum)

        total_num_interrupts_all_cpus = sum(total_num_interrupts_per_cpu)

        return InterruptTotals(total_num_interrupts_all_cpus, total_num_interrupts_per_cpu)


class ProcInterruptsParser:

    def __init__(self, proc_interrupts_file, num_cpus):
        self.proc_interrupts_file = proc_interrupts_file
        self.num_cpus = num_cpus

    def parse_file(self):
        parsed_irqs = []

        with open(self.proc_interrupts_file) as pif:
            # Discard header
            pif.readline()

            for line in pif:
                parsed_irq = self.parse_line(line)
                if parsed_irq is not None:
                    parsed_irqs.append(parsed_irq)

        return parsed_irqs

    def parse_line(self, interrupts_line):
        cpu_regex = '(\d+)\s+' * self.num_cpus
        interrupts_line_regex = '(\d+):\s+{}([\w-]+)\s+(.*)'.format(cpu_regex)

        interrupts_line_compiled = re.compile(interrupts_line_regex)
        interrupts_line_match = interrupts_line_compiled.search(interrupts_line)

        if interrupts_line_match is None:
            return None

        irq_num = interrupts_line_match.group(1)
        irq_type = interrupts_line_match.group(2 + self.num_cpus)
        device_name = interrupts_line_match.group(3 + self.num_cpus)

        num_interrupts_per_cpu = []
        for cpu_num in range(0, self.num_cpus):
            tmp_cpu_interrupts = int(interrupts_line_match.group(2 + cpu_num))
            num_interrupts_per_cpu.append(tmp_cpu_interrupts)

        return Irq(irq_num, irq_type, device_name, num_interrupts_per_cpu)