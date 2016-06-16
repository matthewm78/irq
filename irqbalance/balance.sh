#!/bin/bash

error_exit() {
  local _msg=$1

  echo "[ERROR] $_msg"
  echo
  echo "Usage: $0 <proc_interrupts_file> <num_cpus_in_proc_interrupts>"
  exit 1
}

PROC_INTERRUPTS_FILE=$1
NUM_CPUS_IN_PROC_INTERRUPTS=$2

if [ ! -f "$PROC_INTERRUPTS_FILE" ]; then
  error_exit "you must provide a /proc/interrupts example file"
fi
if [ -z "$NUM_CPUS_IN_PROC_INTERRUPTS" ]; then
  error_exit "you must provide the # of CPUs represented in /proc/interrupts example file"
fi

python3 src/main/python/irqbalance.py "$PROC_INTERRUPTS_FILE" "$NUM_CPUS_IN_PROC_INTERRUPTS"

