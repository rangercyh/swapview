#!/usr/bin/env python3

import os
import re

format = "%5s %9s %s"
totalFmt = "Total: %8s"

def filesize(size):
  '''将 数字 转化为 xxKiB 的形式'''
  units = 'KMGT'
  left = abs(size)
  unit = -1
  while left > 1100 and unit < 3:
    left = left / 1024
    unit += 1
  if unit == -1:
    return '%dB' % size
  else:
    if size < 0:
      left = -left
    return '%.1f%siB' % (left, units[unit])

def getSwapFor(pid):
  try:
    comm = open('/proc/%s/cmdline' % pid).read().replace('\x00', ' ')
    s = 0
    for l in open('/proc/%s/smaps' % pid):
      if l.startswith('Swap:'):
        s += int(re.search(r'\d+', l).group(0))
    return pid, s * 1024, comm[:-1]
  except (IOError, OSError):
    return pid, 0, ''

def getSwap():
  ret = []
  for pid in os.listdir('/proc'):
    if pid.isdigit():
      s = getSwapFor(pid)
      if s[1] > 0:
        ret.append(s)
  ret.sort(key=lambda x: x[1])
  return ret

def main():
  print(format % ('PID', 'SWAP', 'COMMAND'))
  results = getSwap()
  for pid, swap, comm in results:
    print(format % (pid, filesize(swap), comm))
  t = filesize(sum(x[1] for x in results))
  print(totalFmt % t)

if __name__ == '__main__':
  main()
