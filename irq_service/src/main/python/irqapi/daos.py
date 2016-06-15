from irqapi.models import Irq, InterruptTotalsForPeriod, InterruptTotalsForPeriodForCpu
import re
import time

class InterruptTsdbDao:

    def __init__(self, interrupt_tsdb_file, num_cpus):
        self.interrupt_tsdb_file = interrupt_tsdb_file
        self.num_cpus = num_cpus

    def get_interrupts_for_period(self, period_duration_seconds):
        now = time.time()
        start_time_unix = now - period_duration_seconds
        start_totals, end_totals = self._find_start_end_interrupt_totals(start_time_unix)
        interrupts_for_period_per_cpu = [end - start for start, end in zip(start_totals, end_totals)]

        print("Diff line parts -> {}".format(interrupts_for_period_per_cpu))

        return InterruptTotalsForPeriod(
            interrupts_for_period_per_cpu,
            period_duration_seconds,
            self.num_cpus)

    def get_interrupts_for_period_for_cpu(self, cpu_num, period_duration_seconds):
        totals_for_period = self.get_interrupts_for_period(period_duration_seconds)

        return InterruptTotalsForPeriodForCpu(
            totals_for_period.num_interrupts_per_cpu[cpu_num],
            totals_for_period.percent_interrupts_per_cpu[cpu_num],
            period_duration_seconds,
            self.num_cpus,
            totals_for_period.num_interrupts_all_cpus)

    def _find_start_end_interrupt_totals(self, start_time_unix):
        start_totals = []
        end_totals = []
        with open(self.interrupt_tsdb_file, 'r') as itf:
            match_found = False
            for line in itf.readlines():
                line_parts = [float(x) for x in line.strip().split(',')]
                line_timestamp = line_parts[0]
                line_totals = line_parts[1:]
                if not match_found and line_timestamp >= start_time_unix:
                    start_totals = line_totals
                    match_found = True
            end_totals = line_totals

        return start_totals, end_totals


class ProcInterruptsDao:

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


class SmpAffinityDao:

    def __init__(self, smp_affinity_file_pattern):
        self.smp_affinity_file_pattern = smp_affinity_file_pattern

    def get_irq_smp_affinity(self, irq):
        smp_affinity_file = self.smp_affinity_file_pattern.format(irq)
        with open(smp_affinity_file, 'r') as saf:
            smp_affinity = saf.readline().strip()
        return smp_affinity

    def set_irq_smp_affinity(self, irq, smp_affinity_mask):
        smp_affinity_file = self.smp_affinity_file_pattern.format(irq)
        with open(smp_affinity_file, "w") as saf:
            saf.write(smp_affinity_mask + "\n")
        return self.get_irq_smp_affinity(irq)

