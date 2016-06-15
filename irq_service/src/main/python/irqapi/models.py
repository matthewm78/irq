from flask.ext.restful import fields

#------------------------------------------------------------------------------
# Marshaller mappings
#------------------------------------------------------------------------------
irq_fields = {
    'irq_num': fields.String,
    'irq_type': fields.String,
    'device_name': fields.String,
    'cpu_affinity': fields.String,
    'num_interrupts_per_cpu': fields.List(fields.Integer)
}

interrupt_totals_fields = {
    'num_interrupts_all_cpus': fields.Integer,
    'num_interrupts_per_cpu': fields.List(fields.Integer)
}

interrupt_totals_for_period_fields = {
    'num_interrupts_per_cpu': fields.List(fields.Integer),
    'percent_interrupts_per_cpu': fields.List(fields.Float),
    'num_interrupts_all_cpus': fields.Integer,
    'period_duration_seconds': fields.Integer,
    'num_cpus': fields.Integer
}

irq_info_fields = {
    'totals': fields.Nested(interrupt_totals_fields),
    'irqs': fields.List(fields.Nested(irq_fields), attribute='irqs')
}

irq_cpu_affinity_fields = {
    'irq_num': fields.String,
    'cpu_affinity': fields.String
}

#------------------------------------------------------------------------------
# Models
#------------------------------------------------------------------------------
class CpuAffinityInfo:
    def __init__(self, irq_num, cpu_affinity):
        self.irq_num = irq_num
        self.cpu_affinity = cpu_affinity

class InterruptTotals:
    def __init__(self, num_interrupts_all_cpus, num_interrupts_per_cpu):
        self.num_interrupts_all_cpus = num_interrupts_all_cpus
        self.num_interrupts_per_cpu = num_interrupts_per_cpu

class InterruptTotalsForPeriod:
    def __init__(self, num_interrupts_per_cpu, period_duration_seconds, num_cpus) :
        self.num_interrupts_per_cpu = num_interrupts_per_cpu
        self.period_duration_seconds = period_duration_seconds
        self.num_cpus = num_cpus

        self.num_interrupts_all_cpus = sum(num_interrupts_per_cpu)
        self.percent_interrupts_per_cpu = [100.0*(cpu/self.num_interrupts_all_cpus) for cpu in num_interrupts_per_cpu]

class Irq:
    def __init__(self, irq_num, irq_type, device_name, num_interrupts_per_cpu):
        self.irq_num = irq_num
        self.irq_type = irq_type
        self.device_name = device_name
        self.num_interrupts_per_cpu = num_interrupts_per_cpu
        self.cpu_affinity = None

class IrqInfo:
    def __init__(self, irqs, totals):
        self.irqs = irqs
        self.totals = totals
