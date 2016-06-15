import time
from threading import Thread

class InterruptTsdbThread(Thread):
    def __init__(self, irq_service, interrupt_db_file, sampling_interval_seconds):
        self.irq_service = irq_service
        self.interrupt_db_file = interrupt_db_file
        self.sampling_interval_seconds = sampling_interval_seconds
        Thread.__init__(self)

    def run(self):
        print("--TSDB Starting --------------------------------------------------------")
        while True:
            with open(self.interrupt_db_file, 'a+') as interrupt_db_fh:
                totals = self.irq_service.get_interrupt_totals()
                unix_timestamp = time.time()
                interrupts_per_cpu_csv = ",".join([str(x) for x in totals.num_interrupts_per_cpu])
                db_line = "{},{}\n".format(unix_timestamp, interrupts_per_cpu_csv)

                interrupt_db_fh.write(db_line)
            time.sleep(self.sampling_interval_seconds)
