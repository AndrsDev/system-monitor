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
  print(f"System: {uname.system}")
  print(f"Node Name: {uname.node}")
  print(f"Release: {uname.release}")
  print(f"Version: {uname.version}")
  print(f"Machine: {uname.machine}")
  print(f"Processor: {uname.processor}")
  boot_time_timestamp = psutil.boot_time()
  bt = datetime.fromtimestamp(boot_time_timestamp)
  print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

  # let's print CPU information
  print("="*40, "CPU Info", "="*40)
  # number of cores
  print("Physical cores:", psutil.cpu_count(logical=False))
  print("Total cores:", psutil.cpu_count(logical=True))
  # CPU frequencies
  cpufreq = psutil.cpu_freq()

  db.child("data").child("cpu").set({
    "min": cpufreq.min,
    "max": cpufreq.max,
    "current": cpufreq.current,
    "percentage": psutil.cpu_percent(),
  })

  print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
  print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
  print(f"Current Frequency: {cpufreq.current:.2f}Mhz")

  # CPU usage
  # print("CPU Usage Per Core:")
  # for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
  #     print(f"Core {i}: {percentage}%")
  print(f"Total CPU Usage: {psutil.cpu_percent()}%")


  # Memory Information
  print("="*40, "Memory Information", "="*40)

  # get the memory details
  svmem = psutil.virtual_memory()
  print(f"Total: {get_size(svmem.total)}")
  print(f"Available: {get_size(svmem.available)}")
  print(f"Used: {get_size(svmem.used)}")
  print(f"Percentage: {svmem.percent}%")

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


def main():
  print("Enter the duration of the test in minutes:")
  minutes = int(input())

  for _ in range(0, minutes * 60):
    clear()
    print_metrics()
    time.sleep(1)

main()