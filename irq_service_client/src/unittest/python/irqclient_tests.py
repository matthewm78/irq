import unittest
import irqclient
import json
from unittest.mock import MagicMock


INTERRUPT_TOTALS_JSON = json.loads('''{
    "num_interrupts_all_cpus": 200,
    "num_interrupts_per_cpu": [50, 150]
}''')


class IrqClientTest(unittest.TestCase):

    def test_get_interrupt_totals(self):
        mock_api = MagicMock()
        mock_api.do_get = MagicMock(return_value=INTERRUPT_TOTALS_JSON)
        sut = irqclient.IrqClient(mock_api)

        totals = sut.get_interrupt_totals()

        self.assertEquals(200, totals.num_interrupts_all_cpus)
        self.assertEquals(2, totals.num_cpus)
        self.assertEquals([50, 150], totals.num_interrupts_per_cpu)
