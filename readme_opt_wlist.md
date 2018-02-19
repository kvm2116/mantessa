# Watchlist generation
## result_process.py
1. set coefficients (in file)
- alpha for EMWA (suggested value .125)
- swap_rate max of low scoring IP
- min_perc of scores remaining in optimal watchlist
- min_hit of score before it can be popped off watchlist
2. choose script for main (in file)
- while maintaining/updating watchlist, ensure maintain_watchlist code is uncommented
- this is the watchlist we will be running zmap scans on
- list of IPs and their scores will be in ipscores.csv
3. choose input source/directory (ensure ipscores.csv in folder with script)
- if file: 
	`python result_process.py <new-file-path>`
- if dir: 
	`for file in <dir-path>/*; do python result_process.py $file; done`
- (optimal whitelist is ipscores.csv)

# Optimal Watchlist Analysis
## result_process.py
Once control watchlist is generated from zmap scans, obtain optimal watchlist.
1. choose script for main (in file)
- ensure generate_scan_watchlist code is uncommented
	- this is the watchlist we will use to identify outages and perform analysis
	- subset of ipscores.csv IPs with high enough score and times hit
	- list of IPs and their scores will be in ipscan.csv
- note this code can be uncommented during watchlist generation without affecting results
2. choose input source/directory
- if file: 
	`python franction_calc.py ipscan.csv <outage-file-path>`
- if dir: 
	`for file in <dir-path>/*; do python frantion_calc.py ipscan.csv $file; done`
- note watchlist analyzed can be changed (to compare to filtered watchlist, etc)
	`python franction_calc.py <watchlist-file-path> <outage-file-path>`
- (fraction of watchlist IPs up at time of zmap scan in optimal_frac.csv)
3. compare fraction of watchlist to ground truth fractions via excel

