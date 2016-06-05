import unittest
import irqbalance

class IrqBalanceTest(unittest.TestCase):

    IRQ_ETH0_WITHOUT_SUFFIX = '164:       9232                25456   IR-PCI-MSI-edge      eth0'

    # IRQ_ETH0_WITH_ZERO_SUFFIX = '132:    7805535           2676698559   IR-PCI-MSI-edge      eth0-TxRx-0'
    # IRQ_ETH0_WITH_ONE_SUFFIX ='133:  177894710             78268272   IR-PCI-MSI-edge      eth0-TxRx-1'
    # IRQ_ETH1_WITH_SUFFIX = '165:     189741               411172   IR-PCI-MSI-edge      eth1-TxRx-0'

    # IRQ_LEAST_WHITESPACE = '136: 3320311515           1430447281   IR-PCI-MSI-edge      eth0-TxRx-4'
    # IRQ_MOST_WHITESPACE = '164:       9232                25456   IR-PCI-MSI-edge      eth0'

    def test_parse_proc_interrupts_line_eth0_without_suffix(self):
        tmp_irq = irqbalance.parse_proc_interrupts_line(self.IRQ_ETH0_WITHOUT_SUFFIX)

        self.assertEqual("164", tmp_irq.irq_num)
        self.assertEqual("eth0", tmp_irq.device_name)
        self.assertEqual("IR-PCI-MSI-edge", tmp_irq.irq_type)
        self.assertEqual(2, len(tmp_irq.num_interrupts_per_cpu))
        self.assertEqual(9232, tmp_irq.num_interrupts_per_cpu[0])
        self.assertEqual(25456, tmp_irq.num_interrupts_per_cpu[1])