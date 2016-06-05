import unittest
import irqbalance

class IrqBalanceTest(unittest.TestCase):

    # Example lines below based off of fictious /proc/interrupts line:
    #  100:       123                456   irq-type      device-name
    DUMMY_IRQ_NUM = "100"
    DUMMY_NUM_INTERRUPTS_CPU0 = 123
    DUMMY_NUM_INTERRUPTS_CPU1 = 567
    DUMMY_IRQ_TYPE = "irq-type"
    DUMMY_IRQ_LINE_BASE = '{}: {} {} {}'.format(
        DUMMY_IRQ_NUM,
        DUMMY_NUM_INTERRUPTS_CPU0,
        DUMMY_NUM_INTERRUPTS_CPU1,
        DUMMY_IRQ_TYPE)
    DUMMY_DEVICE_NAME = 'device-name'

    COMPLETE_IRQ_LINE = '{} {}'.format(DUMMY_IRQ_LINE_BASE, DUMMY_DEVICE_NAME)

    # IRQ_ETH0_WITH_ZERO_SUFFIX = ' eth0-TxRx-0'
    # IRQ_ETH0_WITH_ONE_SUFFIX =' eth0-TxRx-1'
    # IRQ_ETH1_WITH_SUFFIX = ' eth1-TxRx-0'

    # IRQ_LEAST_WHITESPACE = '136: 3320311515           1430447281   IR-PCI-MSI-edge      eth0-TxRx-4'
    # IRQ_MOST_WHITESPACE = '164:       9232                25456   IR-PCI-MSI-edge      eth0'

    def get_dummy_irq_line_with_device_name(self, device_name):
        return '{} {}'.format(self.DUMMY_IRQ_LINE_BASE, device_name)

    def test_parse_proc_interrupts_line_complete_line(self):
        tmp_irq = irqbalance.parse_proc_interrupts_line(self.COMPLETE_IRQ_LINE)

        self.assertEqual(self.DUMMY_IRQ_NUM, tmp_irq.irq_num)
        self.assertEqual(self.DUMMY_DEVICE_NAME, tmp_irq.device_name)
        self.assertEqual(self.DUMMY_IRQ_TYPE, tmp_irq.irq_type)

        self.assertEqual(2, len(tmp_irq.num_interrupts_per_cpu))
        self.assertEqual(self.DUMMY_NUM_INTERRUPTS_CPU0, tmp_irq.num_interrupts_per_cpu[0])
        self.assertEqual(self.DUMMY_NUM_INTERRUPTS_CPU1, tmp_irq.num_interrupts_per_cpu[1])

    def test_parse_proc_interrupts_line_eth0_without_suffix(self):
        tmp_irq = irqbalance.parse_proc_interrupts_line(
            self.get_dummy_irq_line_with_device_name('eth0'))

        self.assertEqual('eth0', tmp_irq.device_name)
