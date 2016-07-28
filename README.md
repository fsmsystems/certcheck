# certcheck
The main objective of this script is to check the expiration date of an SSL certificate in the simplest way possible using OpenSSL binary. 

#Usage
Usage: certcheck -H [Hostname or IP] -p [port] -s (silent)<br>
-H --host: Hostname or IP <br>
-p --port: HTTPS port <br>
-s --silent: Returns only the difference in days between Now and expire date <br>
 
#Examples:
certcheck.py -H google.es <br>
69 days

certcheck.py -H google.es -p 443 <br>
69 days

certcheck.py -H github.com -p 443 -s <br>
69,2016-10-05
