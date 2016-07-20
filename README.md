# certcheck
The main objective of this script is to check the expiration date of an SSL certificate in the simplest way possible using OpenSSL binary. 

#Usage
Usage: certcheck -H [Hostname or IP] -p [port] -w [days warning] -c [days critical] -s (silent)
 -H --host: Hostname or IP
 -p --port: HTTPS port
 -w or -c: Warning and Critical days to expire optional values
 -s --silent: Returns only the difference in days between Now and expire date
