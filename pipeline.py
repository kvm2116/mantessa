# Python pipeline to execute all 
# functionality for MANTESSA pipeline 
import os 
import subprocess
from subprocess import call 
import datetime 
import database
import sys 

#ZMAP_SCAN_DATA = 'current_zmap_data.txt'
WHITELIST_FILE = "./whitelist.csv"



def main():

  # Start a zmap scan
  dt_file = run_scan()

  # Run scoring algorithm
  #score(dt_file)

  # update_map()


# Run a zmap scan
# When the zmap scan is finished do 1 thing
#     1. One process should insert scan data into DB 
def run_scan():
  # Execute zmap scan from whitelist
  instant = datetime.datetime.now().strftime("%Y%m%dT%H_%M_%S")
  dt_file = "d_" + instant

  #######################################################
  #Commenting out scan and replacing dt file for testing 
  dt_file = 'd_20180127T20_45_31'
  # subprocess.call("touch " + dt_file +" && sudo /usr/local/Cellar/zmap/2.1.1/sbin/zmap -B 15M --probe-module=icmp_echoscan --whitelist-file=\"" + WHITELIST_FILE + "\" -o -")# + dt_file)
  #######################################################

  # Fork to insert into DB 
  pid = os.fork()
  if pid == 0:
    # child
    database.insert_column(dt_file)
    print("Database updated successfully")
    sys.exit(0)
  else:
    # parent
    pass 

  return dt_file

# Run the scoring algorithm 
# When the scores are computed do 2 things
#     1. Send the top N IPs to the mapping job
#     2. Write the list of IPs to scan next time back to a file
#def score(dt_file):
  



# If the map is not runnig, run it
# Write a new datafile for the map to read from 
#def update_map():


main() 
