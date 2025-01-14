#!/usr/bin/env python3
import os
import sys
import time
import _thread

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
from panda import Panda  # noqa: E402

# This script is intended to be used in conjunction with the echo_loopback_test.py test script from panda jungle.
# It sends a reversed response back for every message received containing b"test".

def heartbeat_thread(p):
  while True:
    try:
      p.send_heartbeat()
      p.can_send(0x10,b"\x78\x65\x73\x74", 1)
      print(p.health())
      time.sleep(0.5)
    except Exception:
      continue

# Resend every CAN message that has been received on the same bus, but with the data reversed
if __name__ == "__main__":
  p = Panda()
  _thread.start_new_thread(heartbeat_thread, (p,))
  p.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
  p.set_power_save(False)
  p.set_can_loopback(True)


  while True:
    incoming = p.can_recv()
    for message in incoming:
      address, notused, data, bus = message
      print(message)
      if b'test' in data:
        p.can_send(0x11,b"\x74\x65\x73\x74", 1)
        p.can_send(0x10,b"\x74\x65\x73\x74", 1)
