# certcheck
The main objective of this script is to check the expiration date of an SSL certificate in the simplest way possible using OpenSSL binary. 

#Usage
Usage: certcheck -H [Hostname or IP] -p [port] -w [days warning] -c [days critical] -s (silent)<br>
-H --host: Hostname or IP <br>
-p --port: HTTPS port <br>
-w or -c: Warning and Critical days to expire optional values <br>
-s --silent: Returns only the difference in days between Now and expire date <br>
 
#Examples:
certcheck.py -H github.com -p 443 -w 60 -c 30 <br>
OK: 665 days left for github.com

certcheck.py -H github.com -p 443 -w 60 -c 30 -s <br>
665
