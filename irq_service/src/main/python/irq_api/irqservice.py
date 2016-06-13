from flask import Flask, jsonify
from irq_api.common import Irq

app = Flask(__name__)

@app.route('/interrupts/totals')
def get_interrupts():
    irq = Irq("121", "EDGE", "eth0", [100, 200])
    j = jsonify(irq.__dict__)
    return j
