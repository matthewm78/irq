from irqapi.daos import InterruptTsdbDao, ProcInterruptsDao, SmpAffinityDao
from irqapi.services import InterruptTotalsParser, InterruptService, IrqService
from irqapi.models import (irq_fields, interrupts_for_period_for_cpu_fields, irq_info_fields,
                            irq_cpu_affinity_fields, interrupts_for_period_fields)
from irqapi.tsdb import InterruptTsdbThread

import multiprocessing
from flask import Flask, jsonify, request
from flask.ext.restful import marshal

#------------------------------------------------------------------------------
# Initialize Flask
#------------------------------------------------------------------------------
app = Flask(__name__, static_url_path="")

#------------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------------
PROC_INTERRUPTS_FILE = '/proc/interrupts'
NUM_CPUS = multiprocessing.cpu_count()
INTERRUPT_TSDB_FILE = '/tmp/proc_interrupts.db'
INTERRUPT_TSDB_SAMPLING_INTERVAL_SECONDS = 5

#------------------------------------------------------------------------------
# Wire-up dependency graph
#------------------------------------------------------------------------------
proc_interrupts_dao = ProcInterruptsDao(PROC_INTERRUPTS_FILE, NUM_CPUS)
smp_affinity_dao = SmpAffinityDao('/proc/irq/{}/smp_affinity')
interrupt_tsdb_dao = InterruptTsdbDao(INTERRUPT_TSDB_FILE, NUM_CPUS)

interrupt_totals_parser = InterruptTotalsParser()

irq_service = IrqService(proc_interrupts_dao, interrupt_totals_parser, smp_affinity_dao)
interrupt_service = InterruptService(interrupt_tsdb_dao)

#------------------------------------------------------------------------------
# Route Definitions
#------------------------------------------------------------------------------
@app.route('/interrupts', methods=['GET'])
def get_interrupts_for_period():
    period_duration_seconds = int(request.args.get('period_seconds', 60))
    interrupts_for_period = interrupt_service.get_interrupts_for_period(period_duration_seconds)
    return jsonify(marshal(interrupts_for_period, interrupts_for_period_fields))

@app.route('/interrupts/cpu/<int:cpu_num>', methods=['GET'])
def get_interrupts_for_period_for_cpu(cpu_num):
    period_duration_seconds = int(request.args.get('period_seconds', 60))
    interrupts_for_period_for_cpu = interrupt_service.get_interrupts_for_period_for_cpu(
        cpu_num,
        period_duration_seconds)
    return jsonify(marshal(interrupts_for_period_for_cpu, interrupts_for_period_for_cpu_fields))

@app.route('/irqs', methods=['GET'])
def get_irqs():
    irq_info = irq_service.get_irqs()
    return jsonify(marshal(irq_info, irq_info_fields))

# @app.route('/interrupts/totals', methods=['GET'])
# def get_interrupt_totals():
#         totals = irq_service.get_interrupt_totals()
#         return jsonify(marshal(totals, interrupt_totals_fields))

@app.route('/irqs/<string:irq>/cpu_affinity', methods=['GET'])
def get_irq_cpu_affinity(irq):
    response = irq_service.get_irq_cpu_affinity(irq)
    return jsonify(marshal(response, irq_cpu_affinity_fields))

@app.route('/irqs/<string:irq>/cpu_affinity', methods=['PUT'])
def set_irq_cpu_affinity(irq):
    cpu_affinity_mask = request.form['cpu_affinity_mask']
    response = irq_service.set_irq_cpu_affinity(irq, cpu_affinity_mask)
    return jsonify(marshal(response, irq_cpu_affinity_fields))

#------------------------------------------------------------------------------
# Run: start Flask & interrupts TSTSDB
#------------------------------------------------------------------------------
def run():
    tsdb_thread = InterruptTsdbThread(
        irq_service,
        INTERRUPT_TSDB_FILE,
        INTERRUPT_TSDB_SAMPLING_INTERVAL_SECONDS)

    tsdb_thread.start()
    app.run(debug=True, use_reloader=True)
    tsdb_thread.join()
