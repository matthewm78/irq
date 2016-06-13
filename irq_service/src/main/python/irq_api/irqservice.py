from irq_api.util import IrqService, ProcInterruptsParser

import multiprocessing
from flask import Flask, jsonify
from flask.ext.restful import Api, fields, marshal

app = Flask(__name__, static_url_path="")
api = Api(app)

irq_fields = {
    'irq_num': fields.String,
    'irq_type': fields.String,
    'device_name': fields.String,
    'num_interrupts_per_cpu': fields.List(fields.Integer)
}

interrupt_info_fields = {
    'interrupts': fields.List(fields.Nested(irq_fields), attribute='irqs')
}

PROC_INTERRUPTS_FILE = '/proc/interrupts'
NUM_CPUS = multiprocessing.cpu_count()

proc_interrupts_parser = ProcInterruptsParser(PROC_INTERRUPTS_FILE, NUM_CPUS)
irq_service = IrqService(proc_interrupts_parser)

@app.route('/interrupts', methods=['GET'])
def get_interrupts():
        interrupt_info = irq_service.get_interrupts()
        return jsonify(marshal(interrupt_info, interrupt_info_fields))

