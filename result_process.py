import sys
import csv
import operator
import pandas as pd
import MySQLdb
import os 
import traceback
import ntpath

import socket, struct


def ip2long(ip):
        """
        Convert an IP string to long
        """
        packedIP = socket.inet_aton(ip)
        return struct.unpack("!L", packedIP)[0]

'''
reads csvs to fill in newCurrIPs and newSuccessIPs lists with IPs with updated scores
sorts newCurrIPs with smallest scores at the top
'''
def score_update(alpha, successIPsSorted, currIPsSorted, newCurrIPs, newSuccessIPs):
  #s, c iterators for successIPSorted and currIPsSorted respectively
  s = 0
  c = 0
  
  #iterates through overlap area of successIPsSorted and currIPsSorted
  while s < len(successIPsSorted) and c < len(currIPsSorted):
    success = successIPsSorted[s][0]
    print(currIPsSorted)
    curr, total_str, score_str, zipCode = currIPsSorted[c]
    total = float(total_str)
    score = float(score_str)
    
    '''
    due to current set up of zmap (to only return successful pings)
    if on first ping, ip is not up, the ip is instantly rotated out 
    this means all additions, start at 1/1 scoring
    '''
    if success < curr:
      newSuccessIPs.append([success, 1, 1, zipCode])
      s += 1
    elif success == curr:
      new_score = (1 - alpha) * score + alpha * 1
      total += 1
      newCurrIPs.append([curr, total, new_score, zipCode])
      s += 1
      c += 1
    else:
      new_score = (1 - alpha) * score + alpha * 0
      total += 1
      newCurrIPs.append([curr, total, new_score, zipCode])
      c += 1

  #adding in additional successful IPs
  while s < len(successIPsSorted):
    success = successIPsSorted[s][0]
    newSuccessIPs.append([success, 1, 1])
    s += 1

  
  #updating scores for additional existing IPs
  while c < len(currIPsSorted):
    curr, total_str, score_str = currIPsSorted[c]
    total = float(total_str)
    score = float(score_str)

    new_score = (1 - alpha) * score + alpha * 0
    total += 1
    newCurrIPs.append([curr, total, new_score])
    c += 1

  #sort by score (curr: percentage success) 
  newCurrIPs.sort(key = lambda row: row[2])


'''
pop out IPs according to param values
'''
def popIPs(swap_rate, min_perc, min_hit, newCurrIPs):
  swapped_count = 0
  i = 0
  print "popped IPs:"
  while swapped_count < int(swap_rate*len(newCurrIPs)) and i < len(newCurrIPs):
    if newCurrIPs[i][1] >= min_hit and newCurrIPs[i][2] <= min_perc:
      poppedIP = newCurrIPs.pop(i)
      print poppedIP[0], poppedIP[2]
      swapped_count += 1
    else:
      i += 1
  print "total popped:", swapped_count
  newCurrIPs.sort(key = lambda row: (row[2], row[1]), reverse=True)


def compute_bt(dt_file):
  # DB Config
  conn = MySQLdb.connect(host= "localhost",
                          user="mantessa",
                          passwd="DNA@mantessa!",
                          db="mantessa_pipeline")

  dbcursor = conn.cursor()
  ###############################################

  alpha = 0.125
  swap_rate = 0.1
  min_perc = 0.7
  min_hit = 10

  #opening and sorting corresponding csvs
  try:
    print("Reading most recent data")
    successIPsReader = csv.reader(open(dt_file, 'rb'))
    successIPsSorted = sorted(successIPsReader, key=operator.itemgetter(0))
  except:
    print "no file name inputed"
    exit()

  # TODO: We temporarily assume here that ipScoresReader and successIpsReader 
  # are strictly parallel lists. 
  try:
    ipScoresDf = pd.read_sql('SELECT ip, counter, score, zipCode FROM scandata;', con=conn)
    #currIPsSorted = sorted(ipScoresReader, key=operator.itemgetter(0))
    # TODO add DF support 
    currIPsSorted = ipScoresDf.sort(['ip', 'score']).tolist()
  except:
    currIPsSorted = []

  newCurrIPs = []
  newSuccessIPs = []

  score_update(alpha, successIPsSorted, currIPsSorted, newCurrIPs, newSuccessIPs)
  popIPs(swap_rate, min_perc, min_hit, newCurrIPs)

  ## Do for newCurrIPs and newSuccessIPs
  # TODO optimize this bc theyre each sorted 
  # it also might better be done above 
  for i, ip in enumerate(newCurrIPs):
    if ip in successIPsSorted:
      newCurrIPs[i].append(1)
    else:
      newCurrIPs[i].append(0)

  #This works
  zcodes = get_zip_codes([ip2long(x[0]) for x in newSuccessIPs], dbcursor)

  for i, ip in enumerate(newSuccessIPs):
    newSuccessIPs[i].append(zcodes[i])
    if ip in successIPsSorted:
      newSuccessIPs[i].append(1)
    else:
      newSuccessIPs[i].append(0)

  #wipe old file and write in new values
  open("./current_data/ipscores.csv", "w").close()
  ipScoresWriter = csv.writer(open('ipscores.csv', 'wb'))

  for ip in newCurrIPs:
    ipScoresWriter.writerow(ip)

  for ip in newSuccessIPs:
    ipScoresWriter.writerow(ip)

  pid = os.fork()
  if pid == 0:
    # child
    update_score_table(dt_file, newCurrIPs, newSuccessIPs)
    print("Database updated successfully")
    sys.exit(0)
  else:
    # parent
    pass 

  print "complete"

def get_zip_codes(ips, crsr):
  stmt = "SELECT zipCode FROM scandata WHERE ip="
  zcode = []
  for ip in ips:
    crsr.execute(stmt + str(ip))
    try:
      zcode.append(crsr.fetchall()[0][0])
    except:
      zcode.append('unknown')
  return zcode

def update_score_table(dt, ip_scores_curr, ip_scores_success): 
  col_name = ntpath.basename(dt)

  #Establish DB connection
  conn = MySQLdb.connect(host= "localhost",
                          user="mantessa",
                          passwd="DNA@mantessa!",
                          db="mantessa_pipeline")

  dbcursor = conn.cursor()

  #Create column for current scan
  # TODO when we only scan some IPs at a time, we'll need some flag to indicate if an
  # IP wasn't scanned at all (0 implies scanned and off)
  try:
    dbcursor.execute("alter table scores add "+col_name+" DECIMAL DEFAULT 0")
    conn.commit()
  except Exception as e:
    print "Oops!! Something went wrong "+str(e)
    conn.rollback()  

  #Update database
  #TODO increase efficieny (bulk statement execution AND file iteration)
  stmt = "INSERT IGNORE INTO scores (ip,curscore,"+col_name+") VALUES ( %s , %s , %s ) ON DUPLICATE KEY UPDATE curscore=%s , "+col_name+"=%s;"
  try:
    # For each IP in file (each is up), update db row
    # good thing we have that index! 
    for ip in ip_scores_curr:
      ip_long = ip2long(ip[0])
      s = ip[2]
      dbcursor.execute(stmt, [ip_long, s, s ,s ,s])

    for ip in ip_scores_success:
      ip_long = ip2long(ip[0])
      s = ip[2]
      dbcursor.execute(stmt, [ip_long, s, s ,s ,s])

    dbcursor.execute("DELETE FROM scandata WHERE ip = 0;")
    conn.commit()
  except Exception as e:
    print "Oops!! Something went wrong "+str(e)
    print traceback.print_exc()
    conn.rollback()  

  conn.close()


