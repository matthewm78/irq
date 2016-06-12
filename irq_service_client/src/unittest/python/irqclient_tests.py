import unittest
import irqclient
import json
from unittest.mock import MagicMock

ALL_INTERRUPTS_JSON = json.loads('''{
    "totals": {
        "num_interrupts_all_cpus": 200,
        "num_interrupts_per_cpu": [
            {
                "cpu_num": "0",
                "num_interrupts": 50
            },
            {
                "cpu_num": "1",
                "num_interrupts": 150
            }
        ]
    },
    "interrupts": [
        {
            "irq": "100",
            "device": "eth0-TxRx-0",
            "interrupt_type": "IR-PCI-MSI-edge",
            "num_interrupts_all_cpus": 55,
            "num_interrupts_per_cpu": [
                {
                    "cpu_num": 0,
                    "num_interrupts": 5
                },
                {
                    "cpu_num": 1,
                    "num_interrupts": 50
                }

            ]
        },
        {
            "irq": "101",
            "device": "eth1-TxRx-0",
            "interrupt_type": "IR-PCI-MSI-edge",
            "num_interrupts_all_cpus": 145,
            "num_interrupts_per_cpu": [
                {
                    "cpu_num": 0,
                    "num_interrupts": 45
                },
                {
                    "cpu_num": 1,
                    "num_interrupts": 100
                }

            ]
        }
    ]
}''')

INTERRUPT_TOTALS_JSON = json.loads('''{
    "num_interrupts_all_cpus": 200,
    "num_interrupts_per_cpu": [
        {
            "cpu_num": "0",
            "num_interrupts": 50
        },
        {
            "cpu_num": "1",
            "num_interrupts": 150
        }
    ]
}''')


class IrqClientTest(unittest.TestCase):

    def test_get_interrupt_totals(self):
        mock_response = MagicMock()
        mock_response.get_json = MagicMock(return_value=INTERRUPT_TOTALS_JSON)
        mock_api = MagicMock()
        mock_api.do_get = MagicMock(return_value=mock_response)
        sut = irqclient.IrqClient(mock_api)

        totals = sut.get_interrupt_totals()

        self.assertEquals(200, totals.num_interrupts_all_cpus)
        self.assertEquals(2, totals.num_cpus)
        self.assertEquals(2, len(totals.cpu_interrupt_counts))

