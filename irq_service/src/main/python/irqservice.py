from flask import Flask, jsonify

app = Flask(__name__)

class Irq:
    def __init__(self, irq_num, device_name, irq_type, num_interrupts_per_cpu):
        self.irq_num = irq_num
        self.device_name = device_name
        self.irq_type = irq_type
        self.num_interrupts_per_cpu = num_interrupts_per_cpu

@app.route('/interrupts/totals')
def get_interrupts():
    irq = Irq("121", "eth0", "EDGE", [100, 200])
    j = jsonify(irq.__dict__)
    return j
