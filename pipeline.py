# Python pipeline to execute all 
# functionality for MANTESSA pipeline 

from subprocess import call 
import datetime 

#ZMAP_SCAN_DATA = 'current_zmap_data.txt'
WHITELIST_FILE = 'whitelist.csv'



def main():

  # Start a zmap scan
  run_scan()

  # Run scoring algorithm
  score()

  update_map()


# Run a zmap scan
# When the zmap scan is finished do 2 things
#     1. One process should insert scan data into DB 
#     2. Kick off job to ru nthe scoring algorithm / create list of IPs to map
def run_scan():
  # Execute zmap scan from whitelist
  instant = datetime.datetime.now.strftime("%Y%m%dT%H_%M_%S")
  dt_file = "d_" + instant
  subprocess.call("sudo zmap -B 15M --probe-module=icmp_echoscan --whitelist-file=\"" + WHITELIST_FILE + "\" -o " + dt_file)
  
  # Fork to insert into DB 


  # Exit 


# Run the scoring algorithm 
# When the scores are computed do 2 things
#     1. Send the top N IPs to the mapping job
#     2. Write the list of IPs to scan next time back to a file
def score():



# If the map is not runnig, run it
# Write a new datafile for the map to read from 
def update_map():


main() 