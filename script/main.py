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

def print_metrics():
  print("="*40, "System Information", "="*40)
  uname = platform.uname()
  boot_time_timestamp = psutil.boot_time()
  bt = datetime.fromtimestamp(boot_time_timestamp)

  information = {
    "node": uname.node,
    "system": uname.system,
    "version": uname.version,
    "release": uname.release,
    "machine": uname.machine,
    "processor": uname.processor,
    "boot_time": f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"
  }

  # CPU 
  cpufreq = psutil.cpu_freq()
  cpu = {
    "physical_cores": psutil.cpu_count(logical=False),
    "total_cores": psutil.cpu_count(logical=True),
    "min": cpufreq.min,
    "max": cpufreq.max,
    "current": cpufreq.current,
    "percentage": psutil.cpu_percent()
  }

  # RAM
  svmem = psutil.virtual_memory()
  ram = {
    "total": get_size(svmem.total),
    "available": get_size(svmem.available),
    "used": get_size(svmem.used),
    "percentage": svmem.percent
  }

  # Disk Information
  print("="*40, "Disk Information", "="*40)
  print("Partitions and Usage:")
  # get all disk partitions
  partitions = psutil.disk_partitions()
  for partition in partitions:
      print(f"=== Device: {partition.device} ===")
      print(f"  Mountpoint: {partition.mountpoint}")
      print(f"  File system type: {partition.fstype}")
      try:
          partition_usage = psutil.disk_usage(partition.mountpoint)
      except PermissionError:
          # this can be catched due to the disk that
          # isn't ready
          continue
      print(f"  Total Size: {get_size(partition_usage.total)}")
      print(f"  Used: {get_size(partition_usage.used)}")
      print(f"  Free: {get_size(partition_usage.free)}")
      print(f"  Percentage: {partition_usage.percent}%")
  # get IO statistics since boot
  disk_io = psutil.disk_io_counters()
  print(f"Total read: {get_size(disk_io.read_bytes)}")
  print(f"Total write: {get_size(disk_io.write_bytes)}")

  # Network information
  print("="*40, "Network Information", "="*40)
  net_counters = psutil.net_io_counters()
  print(f"Total Sent: {get_size(net_counters.bytes_sent)}")
  print(f"Total Received: {get_size(net_counters.bytes_recv)}")
  print(f"Packets Sent: {net_counters.packets_sent}")
  print(f"Packets Received: {net_counters.packets_recv}")


  db.set({
    "information": information,
    "cpu": cpu,
    "ram": ram
  })


def main():
  print("Enter the duration of the test in minutes:")
  minutes = int(input())

  for _ in range(0, minutes * 60):
    clear()
    print_metrics()
    time.sleep(1)

main()