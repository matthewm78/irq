import re
import operator

class Irq:
    def __init__(self, irq_num, device_name, irq_type, num_interrupts_per_cpu):
        self.irq_num = irq_num
        self.device_name = device_name
        self.irq_type = irq_type
        self.num_interrupts_per_cpu = num_interrupts_per_cpu

    @property
    def total_num_interrupts(self):
        return sum(self.num_interrupts_per_cpu)


class IrqBalancingRecommendation:

    def __init__(self, num_cpus):
        self.num_cpus = num_cpus
        self.irqs_for_cpu = [[] for x in range(0, num_cpus)]

    def add_irq_num_to_cpu(self, cpu_num, irq_num):
        print("Addiing num [{}] for cpu [{}]".format(irq_num,cpu_num))
        self.irqs_for_cpu[cpu_num].append(irq_num)

    def get_irqs_for_cpu(self, cpu_num):
        print("Getting -> {}".format(self.irqs_for_cpu))
        return self.irqs_for_cpu[cpu_num]


class IrqBalancer:

    def __init__(self, num_cpus):
        self.num_cpus = num_cpus

    def balance_irqs(self, irqs):
        recommendation = IrqBalancingRecommendation(self.num_cpus)
        irqs_sorted_by_total_interrupts = self.sort_irqs_by_total(irqs)

        tmp_cpu_num = 0
        for irq in irqs_sorted_by_total_interrupts:
            recommendation.add_irq_num_to_cpu(tmp_cpu_num % self.num_cpus, irq.irq_num)
            tmp_cpu_num += 1

        return recommendation

    def sort_irqs_by_total(self, unsorted_irqs):
        return sorted(unsorted_irqs, key=operator.attrgetter('total_num_interrupts'), reverse=True)

class ProcInterruptsParser:

    def parse_file(self, proc_interrupts_file):
        parsed_irqs = []

        with open(proc_interrupts_file) as pif:
            for line in pif:
                parsed_irq = self.parse_line(line)
                parsed_irqs.append(parsed_irq)

        return parsed_irqs

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
    parsed_irqs = proc_interrupts_parser.parse_file(proc_interrupts_file)

    irq_balancer = IrqBalancer(2)
    balance_irqs_out = irq_balancer.balance_irqs(parsed_irqs)

    print(balance_irqs_out.get_irqs_for_cpu(0))
