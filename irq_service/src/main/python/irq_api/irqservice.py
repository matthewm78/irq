from irq_api.util import SmpAffinityUtil, InterruptTotalsParser, IrqService, ProcInterruptsParser

import multiprocessing
from flask import Flask, jsonify, request
from flask.ext.restful import Api, fields, marshal

app = Flask(__name__, static_url_path="")
api = Api(app)

irq_fields = {
    'irq_num': fields.String,
    'irq_type': fields.String,
    'device_name': fields.String,
    'num_interrupts_per_cpu': fields.List(fields.Integer)
}

interrupt_totals_fields = {
    'num_interrupts_all_cpus': fields.Integer,
    'num_interrupts_per_cpu': fields.List(fields.Integer)
}

interrupt_info_fields = {
    'totals': fields.Nested(interrupt_totals_fields),
    'interrupts': fields.List(fields.Nested(irq_fields), attribute='irqs')
}

irq_cpu_affinity_fields = {
    'irq_num': fields.String,
    'cpu_affinity': fields.String
}

PROC_INTERRUPTS_FILE = '/proc/interrupts'
NUM_CPUS = multiprocessing.cpu_count()

proc_interrupts_parser = ProcInterruptsParser(PROC_INTERRUPTS_FILE, NUM_CPUS)
interrupt_totals_parser = InterruptTotalsParser()
smp_affinity_parser = SmpAffinityUtil('/proc/irq/{}/smp_affinity')
interrupt_totals_parser = InterruptTotalsParser()

irq_service = IrqService(proc_interrupts_parser, interrupt_totals_parser, smp_affinity_parser)

@app.route('/interrupts', methods=['GET'])
def get_interrupts():
        interrupt_info = irq_service.get_interrupts()
        return jsonify(marshal(interrupt_info, interrupt_info_fields))

@app.route('/interrupts/totals', methods=['GET'])
def get_interrupt_totals():
        totals = irq_service.get_interrupt_totals()
        return jsonify(marshal(totals, interrupt_totals_fields))

@app.route('/interrupts/<string:irq>/cpu_affinity', methods=['GET'])
def get_irq_cpu_affinity(irq):
        response = irq_service.get_irq_cpu_affinity(irq)
        return jsonify(marshal(response, irq_cpu_affinity_fields))

@app.route('/interrupts/<string:irq>/cpu_affinity', methods=['PUT'])
def set_irq_cpu_affinity(irq):
        cpu_affinity_mask = request.form['cpu_affinity_mask']
        response = irq_service.set_irq_cpu_affinity(irq, cpu_affinity_mask)
        return jsonify(marshal(response, irq_cpu_affinity_fields))
