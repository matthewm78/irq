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

    def get_interrupt_totals(self):
        response_dict = self.api.do_get("/interrupts/totals")
        return response_dict