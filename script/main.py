import os
import time
import subprocess
import psutil
import platform
import pyrebase
from datetime import datetime

config = {
 "apiKey": "AIzaSyATj1ov6n6bfJ4QGvv8WrDWeox5aqimH2I",
  "authDomain": "system-monitor-531ab.firebaseapp.com",
  "databaseURL": "https://system-monitor-531ab.firebaseio.com",
  "projectId": "system-monitor-531ab",
  "storageBucket": "system-monitor-531ab.appspot.com",
  "messagingSenderId": "154390991734",
  "appId": "1:154390991734:web:79dc0f4d9d800ed695e057"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def clear():
    if os.name in ('nt','dos'):
        subprocess.call("cls", shell=True)
    elif os.name in ('linux','osx','posix'):
        subprocess.call("clear", shell=True)
    else:
        print("\n") * 120


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def save_metrics():
  uname = platform.uname()
  boot_time_timestamp = psutil.boot_time()
  bt = datetime.fromtimestamp(boot_time_timestamp)

  # General Information
  information = {
    "node": uname.node,
    "system": uname.system,
    "version": uname.version,
    "release": uname.release,
    "machine": uname.machine,
    "processor": uname.processor,
    "boot_time": f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"
  }

  # CPU Information
  cpufreq = psutil.cpu_freq()
  cpu = {
    "physical_cores": psutil.cpu_count(logical=False),
    "total_cores": psutil.cpu_count(logical=True),
    "min": cpufreq.min,
    "max": cpufreq.max,
    "current": cpufreq.current,
    "percentage": psutil.cpu_percent()
  }

  # RAM Information
  svmem = psutil.virtual_memory()
  ram = {
    "total": get_size(svmem.total),
    "available": get_size(svmem.available),
    "used": get_size(svmem.used),
    "percentage": svmem.percent
  }

  # Disk Information
  partition = psutil.disk_partitions()[-1]
  partition_usage = psutil.disk_usage(partition.mountpoint)
  disk_io = psutil.disk_io_counters()
  disk = {
    "total_size": get_size(partition_usage.total),
    "used": get_size(partition_usage.used),
    "free": get_size(partition_usage.free),
    "percentage": partition_usage.percent,
    "total_read": get_size(disk_io.read_bytes),
    "total_write": get_size(disk_io.write_bytes)
  }

  # Network information
  net_counters = psutil.net_io_counters()
  network = {
    "total_sent": get_size(net_counters.bytes_sent),
    "total_received": get_size(net_counters.bytes_recv),
    "packets_sent": net_counters.packets_sent,
    "packets_received": net_counters.packets_recv,
  }

  db.set({
    "information": information,
    "cpu": cpu,
    "ram": ram,
    "disk": disk,
    "network": network
  })


def main():
  print("Enter the duration of the test in minutes:")
  seconds = int(input()) * 60
  print("Starting...")

  for i in range(0, seconds):
    print(f"{i}/{seconds}")
    save_metrics()
    time.sleep(1)
  
  print("Finished...")

main()