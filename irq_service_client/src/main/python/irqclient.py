import requests
import json
from prettytable import PrettyTable

class IrqServiceApi:
    def __init__(self, host, port=80):
        self.host = host
        self.port = port

    def do_get(self, path):
        url = "http://{}:{}{}".format(self.host, self.port, path)
        response = requests.get(url)
        return response.json()


class PrintHelper:
    def __init__(self, out_stream):
        self.out_stream = out_stream

    def print_interrupts(self, interrupts):
        num_interrupts_all_cpus = interrupts['totals']['num_interrupts_all_cpus']
        num_interrupts_per_cpu = interrupts['totals']['num_interrupts_per_cpu']

        irqs = interrupts['interrupts']
        num_cpus = len(irqs[0]['num_interrupts_per_cpu'])

        cpu_columns = []
        for i in range(0, num_cpus):
            cpu_columns.append("CPU{}".format(i))

        columns = ["IRQ"]  + ["Irq Type", "Device"] + cpu_columns
        table = PrettyTable(columns)
        for irq in irqs:
            columns = []
            columns.append(irq['irq_num'])
            columns.append(irq['device_name'])
            columns.append(irq['irq_type'])
            columns += irq['num_interrupts_per_cpu']
            table.add_row(columns)

        totals_columns = ["Totals:"]
        totals_columns += ["", ""]
        totals_columns += num_interrupts_per_cpu
        table.add_row(totals_columns)

        self.out_stream.write(table.get_string(sortby="IRQ") + "\n")

    def print_interrupt_totals(self, interrupt_totals):
        num_interrupts_all_cpus = interrupt_totals['num_interrupts_all_cpus']
        num_interrupts_per_cpu = interrupt_totals['num_interrupts_per_cpu']

        table = PrettyTable(["Cpu #", "Total Interrupts"])
        for i in range(0, len(num_interrupts_per_cpu)):
            table.add_row([
                "CPU{}".format(i),
                num_interrupts_per_cpu[i]
            ])
        table.add_row(["Total:", num_interrupts_all_cpus])

        self.out_stream.write(table.get_string() + "\n")


class IrqClient:

    def __init__(self, api):
        self.api = api

    def get_interrupts(self):
        response_dict = self.api.do_get("/interrupts")
        return response_dict

    def get_interrupt_totals(self):
        response_dict = self.api.do_get("/interrupts/totals")
        return response_dict