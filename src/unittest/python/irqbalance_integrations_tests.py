import unittest
import irqbalance


class ProcInterruptsParserIntegrationTest(unittest.TestCase):

    def setUp(self):
        self.proc_interrupts_parser = irqbalance.ProcInterruptsParser()

    def test_parse_file(self):
        tmp_irqs = self.proc_interrupts_parser.parse_file('src/unittest/python/basic_proc_interrupts.txt')

        self.assertEquals(2, len(tmp_irqs))

        tmp_irq_one = tmp_irqs[0]
        self.assertEquals("100", tmp_irq_one.irq_num)
        self.assertEquals("eth0-irq-100", tmp_irq_one.device_name)
        self.assertEquals("IR-PCI-MSI-edge", tmp_irq_one.irq_type)
        self.assertEquals(1, tmp_irq_one.num_interrupts_per_cpu[0])
        self.assertEquals(1, tmp_irq_one.num_interrupts_per_cpu[1])

        tmp_irq_two = tmp_irqs[1]
        self.assertEquals("101", tmp_irq_two.irq_num)
        self.assertEquals("eth0-irq-101", tmp_irq_two.device_name)
        self.assertEquals("IR-PCI-MSI-edge", tmp_irq_two.irq_type)
        self.assertEquals(2, tmp_irq_two.num_interrupts_per_cpu[0])
        self.assertEquals(2, tmp_irq_two.num_interrupts_per_cpu[1])