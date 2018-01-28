import sys
import csv
import operator
import MySQLdb as mdb
import pandas as pd
import ip

from config import USERNAME
from config import PASSWORD
from db_config import COLUMN_NAME
from sqlalchemy import create_engine

def insert_column(scan_result_file_name):
  col_name = scan_result_file_name
  #Establish DB connection
  conn = MySQLdb.connect(host= "localhost",
                          user="root",
                          passwd="DNA@mantessa!",
                          db="mantessa_db9")

  dbcursor = conn.cursor()

  #Create column for current scan
  # TODO when we only scan some IPs at a time, we'll need some flag to indicate if an
  # IP wasn't scanned at all (0 implies scanned and off)
  try:
    dbcursor.execute("alter table mantessa add "+col_name+" BOOLEAN DEFAULT 0")
    conn.commit()
  except Exception as e:
    print "Oops!! Something went wrong "+str(e)
    conn.rollback()  

  #Update database
  #TODO increase efficieny (bulk statement execution AND file iteration)
  stmt = "INSERT IGNORE INTO mantessa (ip,"+col_name+") VALUES (%s,1) ON DUPLICATE KEY UPDATE counter=counter+1 ,"+col_name+"=1;"
  try:
    scan_result_file = open(scan_result_file_name, 'r')
    lines = f.readlines()

    # For each IP in file (each is up), update db row
    # good thing we have that index! 
    for ip in lines:
      ip_long = ip.ip2long(ip)
      dbcursor.execute(stmt, ip_long)
    conn.commit()
  except:
    print "Oops!! Something went wrong "+str(e)
    conn.rollback()  

  conn.close()