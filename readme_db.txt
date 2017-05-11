# By Tushar Agarwal

Mantessa Usage Guide:

1)	Using Censys to fetch data: 
   a.	Go to Scripts folder
   b.	Update UID and SECRET in config.py after getting these from https://censys.io/account
   c.	From terminal run: python fetch_data_from_censys <date>
     i.	Eg. fetch_data_from_censys 20170207
    ii.	Date format is Year+Month+Day
2)	Next install MySQL on your system (See MySQL Reference guide)
   a.	Go to mantessa_db folder from terminal
   b.	Login to your MySQL instance
   c.	From console run: source mantissa_sql.sql to setup the database

Building the Static IP dataset:

For the 6 months data, repeat the following:

2)	Run: python update_db.py <date>

Finally, from the mysql console do:

3)     Choose a counter value for static IP addresses

Finding failure:

1)	From a new terminal window; Run: python find_failure.py <date>
2)	Next Run: python query_db.py <date>. This will dump all the ip,latitude,longitude
 Combinations for which there may be a power failure in failure_data folder.	

