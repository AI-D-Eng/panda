#!/usr/bin/env python3

import csv
from panda import Panda
import time

def can_logger():
  p = Panda()

  try:
    outputfile = open('output.csv', 'w')
    outputfile_cabana = open('output_cabana.csv', 'w')
    csvwriter = csv.writer(outputfile)
    csvwriter_cabana = csv.writer(outputfile_cabana)

    # Write Header
    csvwriter.writerow(['Bus', 'MessageID', 'Message', 'MessageLength'])

    #time,addr,bus,data
    #time.time()
    csvwriter_cabana.writerow(['time', 'addr', 'bus', 'data'])
    print("Writing csv file output.csv. Press Ctrl-C to exit...\n")

    bus0_msg_cnt = 0
    bus1_msg_cnt = 0
    bus2_msg_cnt = 0

    while True:
      can_recv = p.can_recv()

      for address, _, dat, src in can_recv:
        csvwriter.writerow([str(src), str(hex(address)), f"0x{dat.hex()}", len(dat)])
        csvwriter_cabana.writerow([str(time.time()), str(int(address)), str(src),f"0x{dat.hex()}"])

        if src == 0:
          bus0_msg_cnt += 1
        elif src == 1:
          bus1_msg_cnt += 1
        elif src == 2:
          bus2_msg_cnt += 1

        print(f"Message Counts... Bus 0: {bus0_msg_cnt} Bus 1: {bus1_msg_cnt} Bus 2: {bus2_msg_cnt}", end='\r')

  except KeyboardInterrupt:
    print(f"\nNow exiting. Final message Counts... Bus 0: {bus0_msg_cnt} Bus 1: {bus1_msg_cnt} Bus 2: {bus2_msg_cnt}")
    outputfile.close()

if __name__ == "__main__":
  can_logger()
