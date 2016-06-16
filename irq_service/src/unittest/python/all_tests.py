from irqapi.models import Irq
from irqapi.daos import ProcInterruptsDao
from irqapi.util import InterruptTotalsParser

import unittest

class InterruptTotalsParserTest(unittest.TestCase):
    def test_get_totals(self):
        # Total cpu0 -> 3
        # Total cpu1 -> 6
        # Total cpu2 -> 9
        # Total all cpus -> 18
        mock_irqs = [
            Irq(None, None, None, [1, 2, 3]),
            Irq(None, None, None, [1, 2, 3]),
            Irq(None, None, None, [1, 2, 3])
        ]
        sut = InterruptTotalsParser()
        totals = sut.get_totals(mock_irqs)

        self.assertEquals([3, 6, 9], totals.num_interrupts_per_cpu)
        self.assertEquals(18, totals.num_interrupts_all_cpus)


class ProcInterruptsDaoTest(unittest.TestCase):

    def test_parse_line_with_non_numerical_irq_num_should_return_none(self):
        line = "NMI:  10  irq-type  device-name"

        sut = ProcInterruptsDao(None, 1)
        tmp_irq = sut.parse_line(line)

        self.assertEquals(None, tmp_irq)

    def test_parse_line_multiple_cpus(self):
        multi_cpu_line = "100:  10  20  30  irq-type  device-name"

        sut = ProcInterruptsDao(None, 3)
        tmp_irq = sut.parse_line(multi_cpu_line)

        self.assertEquals([10, 20, 30], tmp_irq.num_interrupts_per_cpu)

    def test_parse_proc_interrupts_line_real_line_least_whitespace(self):
        IRQ_LEAST_WHITESPACE = '136: 3320311515           1430447281   IR-PCI-MSI-edge      eth0-TxRx-4'

        sut = ProcInterruptsDao(None, 2)
        tmp_irq = sut.parse_line(IRQ_LEAST_WHITESPACE)

        self.assertEqual("136", tmp_irq.irq_num)
        self.assertEqual('eth0-TxRx-4', tmp_irq.device_name)
        self.assertEqual("IR-PCI-MSI-edge", tmp_irq.irq_type)

        self.assertEqual(2, len(tmp_irq.num_interrupts_per_cpu))
        self.assertEqual(3320311515, tmp_irq.num_interrupts_per_cpu[0])
        self.assertEqual(1430447281, tmp_irq.num_interrupts_per_cpu[1])

    def test_parse_proc_interrupts_line_real_line_most_whitespace(self):
        IRQ_MOST_WHITESPACE = '164:       9232                25456   IR-PCI-MSI-edge      eth0'

        sut = ProcInterruptsDao(None, 2)
        tmp_irq = sut.parse_line(IRQ_MOST_WHITESPACE)

        self.assertEqual("164", tmp_irq.irq_num)
        self.assertEqual('eth0', tmp_irq.device_name)
        self.assertEqual("IR-PCI-MSI-edge", tmp_irq.irq_type)

        self.assertEqual(2, len(tmp_irq.num_interrupts_per_cpu))
        self.assertEqual(9232, tmp_irq.num_interrupts_per_cpu[0])
        self.assertEqual(25456, tmp_irq.num_interrupts_per_cpu[1])
