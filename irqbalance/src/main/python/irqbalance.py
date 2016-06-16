import operator
import re
from prettytable import PrettyTable


class Irq:
    """
    Represents an IRQ entry from /proc/interrupts.

    Contains helper property for getting total # of interrupts for this IRQ
    across all CPUs.
    """

    def __init__(self, irq_num, device_name, irq_type, num_interrupts_per_cpu):
        self.irq_num = irq_num
        self.device_name = device_name
        self.irq_type = irq_type
        self.num_interrupts_per_cpu = num_interrupts_per_cpu

    @property
    def total_num_interrupts(self):
        return sum(self.num_interrupts_per_cpu)


class IrqBalancingRecommendation:
    """
    Represents a recommendation for which IRQs should be pinned to which CPUs in a system.

    It contains several helper methods for getting metrics about the recommendation,
    such as how the interrupts are spread across the CPUs of the system by
    this recommendation as both percentages and counts.
    """

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

    def get_total_num_interrupts_all_cpus(self):
        num_interrupts_per_cpu = []
        for i in range(0, self.num_cpus):
            num_interrupts_per_cpu.append(self.get_num_interrupts_for_cpu(i))
        return sum(num_interrupts_per_cpu)

    def get_percentage_interrupts_for_cpu(self, cpu_num, round_to_places=2):
        num_interrupts_for_cpu = self.get_num_interrupts_for_cpu(cpu_num)
        total_num_interrupts_all_cpus = self.get_total_num_interrupts_all_cpus()
        percentage_interrupts_for_cpu = ((100.0 * num_interrupts_for_cpu) / total_num_interrupts_all_cpus)

        return round(percentage_interrupts_for_cpu, round_to_places)


class IrqBalancingRecommendationPrinter:
    """
    Prints an IRQ balancing recommendation in an easy-to-read manner.

    Used to separate concern of printing from the model object.
    """

    def print_recommendation(self, recommendation, output_stream):
        table = PrettyTable(['Cpu #', '% of Interrupts', '# Interrupts', 'Pinned IRQs'])

        for cpu_num in range(0, recommendation.num_cpus):
            percentage_interrupts_for_cpu = recommendation.get_percentage_interrupts_for_cpu(cpu_num)
            num_interrupts_for_cpu = recommendation.get_num_interrupts_for_cpu(cpu_num)

            irqs_for_cpu = recommendation.get_irqs_for_cpu(cpu_num)
            irq_nums_for_cpu = [irq.irq_num for irq in irqs_for_cpu]

            table.add_row([
                cpu_num,
                "{}%".format(percentage_interrupts_for_cpu),
                num_interrupts_for_cpu,
                ",".join(irq_nums_for_cpu)])

        output_stream.write(table.get_string() + "\n")


class AlternatingNextMaxIrqBalancer:
    """
    A a simple algorithm to balance IRQs across a set of CPUs.

    The algorithm works by sorting all IRQs by their total # of interrupts across
    all CPUs.  It then takes the IRQ with the most interrupt and places it at
    CPU0.  It then grabs the IRQ with the next most interrupts and places it on
    CPU1.  This process repeats until no IRQs are left to place.  During the process
    when the last CPU is reached during the iteration, the next IRQ is placed at
    CPU0 and the iteration continues.
    """

    def __init__(self, num_cpus):
        self.num_cpus = num_cpus

    def balance_irqs(self, irqs):
        """
        Balances a set of IRQs across a set # of CPUs based on total interrupts.

        It takes a set of IRQs, balances them based on its algorithm and returns
        a recommendation that details which IRQs should be pinned to which CPUs.
        """

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
    """
    Parser that extracts IRQ information from a modified /proc/interrupts file.
    """

    def parse_file(self, proc_interrupts_file, num_cpus):
        """
        Parse a modified /proc/interrupts into an array of IRQ objects.
        """

        parsed_irqs = []

        with open(proc_interrupts_file) as pif:
            for line in pif:
                parsed_irq = self.parse_line(line, num_cpus)
                parsed_irqs.append(parsed_irq)

        return parsed_irqs

    def parse_line(self, interrupts_line, num_cpus):
        """
        Parse a individual line in /proc/interrupts into an IRQ object.
        """
        cpu_regex = '(\d+)\s+' * num_cpus
        interrupts_line_regex = '(\d+):\s+{}([\w-]+)\s+(.*)'.format(cpu_regex)

        interrupts_line_compiled = re.compile(interrupts_line_regex)

        interrupts_line_match = interrupts_line_compiled.search(interrupts_line)

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
    num_cpus = int(sys.argv[2])

    proc_interrupts_parser = ProcInterruptsParser()
    parsed_irqs = proc_interrupts_parser.parse_file(proc_interrupts_file, num_cpus)

    irq_balancer = AlternatingNextMaxIrqBalancer(num_cpus)
    balance_irqs_out = irq_balancer.balance_irqs(parsed_irqs)

    recommendation_printer = IrqBalancingRecommendationPrinter()
    recommendation_printer.print_recommendation(balance_irqs_out, sys.stdout)
