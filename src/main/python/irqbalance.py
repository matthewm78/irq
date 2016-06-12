import re
import operator
from prettytable import PrettyTable


class Irq:
    def __init__(self, irq_num, device_name, irq_type, num_interrupts_per_cpu):
        self.irq_num = irq_num
        self.device_name = device_name
        self.irq_type = irq_type
        self.num_interrupts_per_cpu = num_interrupts_per_cpu

    @property
    def total_num_interrupts(self):
        return sum(self.num_interrupts_per_cpu)

class IrqBalancingRecommendationMetricsPrinter:

    def print_metrics(self, recommendation, output_stream):
        table = PrettyTable(['Cpu #', 'Percent of Interrupts'])

        percentage_interrupts_per_cpu = recommendation.percentage_interrupts_per_cpu

        for i in range(recommendation.num_cpus):
            table.add_row([i, "{}%".format(percentage_interrupts_per_cpu[i])])

        output_stream.write(table.get_string() + "\n")


class IrqBalancingRecommendationPrinter:

    def print_recommendation(self, recommendation, output_stream):
        table = PrettyTable(['Cpu #', 'Pinned IRQs'])

        num_cpus = recommendation.num_cpus
        for cpu_num in range(0, num_cpus):
            irqs_for_cpu = recommendation.get_irqs_for_cpu(cpu_num)
            irq_nums_for_cpu = [irq.irq_num for irq in irqs_for_cpu]
            table.add_row([cpu_num, ",".join(irq_nums_for_cpu)])

        output_stream.write(table.get_string() + "\n")


class IrqBalancingRecommendationMetrics:
    ROUND_TO_PLACES = 2

    def __init__(self, num_interrupts_per_cpu):
        self.num_interrupts_per_cpu = num_interrupts_per_cpu
        self.num_cpus = len(num_interrupts_per_cpu)
        self.total_num_interrupts_all_cpus = sum(self.num_interrupts_per_cpu)
        self.percentage_interrupts_per_cpu = [
            round((100.0 * n) / self.total_num_interrupts_all_cpus, self.ROUND_TO_PLACES)
            for n in self.num_interrupts_per_cpu]


class IrqBalancingRecommendation:

    def __init__(self, num_cpus):
        self.num_cpus = num_cpus
        self.irqs_for_cpu = [[] for x in range(0, num_cpus)]

    def pin_irq_to_cpu(self, cpu_num, irq):
        self.irqs_for_cpu[cpu_num].append(irq)

    def get_irqs_for_cpu(self, cpu_num):
        return self.irqs_for_cpu[cpu_num]

    def get_num_interrupts_for_cpu(self, cpu_num):
        irqs_for_cpu_to_sum = self.get_irqs_for_cpu(cpu_num)
        return sum(i.total_num_interrupts for i in irqs_for_cpu_to_sum)

    def get_metrics(self):
        num_interrupts_per_cpu = []
        for i in range(0, self.num_cpus):
            num_interrupts_per_cpu.append(self.get_num_interrupts_for_cpu(i))

        return IrqBalancingRecommendationMetrics(num_interrupts_per_cpu)


class IrqBalancer:

    def __init__(self, num_cpus):
        self.num_cpus = num_cpus

    def balance_irqs(self, irqs):
        recommendation = IrqBalancingRecommendation(self.num_cpus)
        irqs_sorted_by_total_interrupts = self.sort_irqs_by_total(irqs)

        counter = 0
        while len(irqs_sorted_by_total_interrupts) > 0:
            irq_with_next_max_interrupts = irqs_sorted_by_total_interrupts.pop()
            num_next_cpu_in_rotation = counter % self.num_cpus

            recommendation.pin_irq_to_cpu(
                num_next_cpu_in_rotation,
                irq_with_next_max_interrupts)

            counter += 1

        return recommendation

    def sort_irqs_by_total(self, unsorted_irqs):
        return sorted(unsorted_irqs, key=operator.attrgetter('total_num_interrupts'), reverse=False)

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

    recommendation_printer = IrqBalancingRecommendationPrinter()
    recommendation_printer.print_recommendation(balance_irqs_out, sys.stdout)

    metrics_printer = IrqBalancingRecommendationMetricsPrinter()
    metrics_printer.print_metrics(balance_irqs_out.get_metrics(), sys.stdout)
