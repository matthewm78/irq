import unittest
import irqclient
from httmock import (all_requests, with_httmock)

@all_requests
def mock_api_response_content(url, request):
    mock_json_file = 'src/unittest/resources/api_responses{}.json'.format(url.path)
    with open(mock_json_file, 'r') as mjf:
        mock_json_content = mjf.read()
    return mock_json_content

class IrqClientIntegrationTest(unittest.TestCase):

    @with_httmock(mock_api_response_content)
    def test_get_interrupt_totals(self):
        irq_api = irqclient.IrqServiceApi('localhost')
        sut = irqclient.IrqClient(irq_api)

        totals = sut.get_interrupt_totals()

        self.assertEquals(200, totals.num_interrupts_all_cpus)
        self.assertEquals(2, totals.num_cpus)
        self.assertEquals([50, 150], totals.num_interrupts_per_cpu)