
from threading import Thread
import time

def daemon(irq_service, interrupts_db):
    while True:
        with open(interrupts_db, 'a+') as interrupts_db_file:
            totals = irq_service.get_interrupt_totals()
            unix_timestamp = time.time()
            interrupts_per_cpu_csv = ",".join([str(x) for x in totals.num_interrupts_per_cpu])
            db_line = "{},{}\n".format(unix_timestamp, interrupts_per_cpu_csv)
            interrupts_db_file.write(db_line)
        time.sleep(10)

INTERRUPTS_DB = '/tmp/proc_interrupts.db'
thr = Thread(target=daemon, args=[irq_service, INTERRUPTS_DB])
thr.start()