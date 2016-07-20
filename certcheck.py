# -*- encoding: utf-8 -*-
#!/usr/bin/python2
#
# Ferran Serafini
# BSD Licence

import os
import datetime
import sys
import getopt

def check_date_with_wcparams(obj_expiredate,date_today,diff_date,umbral_warning,umbral_critical):
    if diff_date.days > umbral_warning:
        return 0 # OK
    else:
        if diff_date.days <= umbral_warning:
            if diff_date.days <= umbral_critical:
                return 2 # CRITICAL
            else:
                return 1 # WARNING

def print_to_stdout(status,diff_date,silent):
    if silent: # if only want to see value without logics 
        print str(diff_date.days)
    else: # Normal view
        out_str=str(diff_date.days) + ' days left for '+_host
        if status == 0:
            print 'OK: '+out_str
        if status == 1:
            print 'WARNING: '+out_str
        if status == 2:
            print 'CRITICAL: '+out_str

def usage(version):
        print 'Certcheck '+version+ '(FSM)'
        print 'Usage: checkcert -H [Hostname or IP] -p [port] -w [days warning] -c [days critical] -s (silent)' 
        print ' -H --host: Hostname or IP'
        print ' -p --port: HTTPS port'
        print ' -w or -c: Warning and Critical days to expire optional values'
        print ' -s --silent: Returns only the difference in days between Now and expire date'
        sys.exit(0)

if __name__ == "__main__":
        version = '0.0.1'
        silent = False
        options, remainder = getopt.gnu_getopt(sys.argv[1:], 'H:p:w:c:sh', ['Host=','port=','warning=','critical=',])
        #print 'OPTIONS   :', options

        for opt, arg in options:
            if opt in ('-h', '--help'):
                usage(version)
            elif opt in ('-H','--host'):
                _host = arg
            elif opt in ('-p', '--port'):
                _port = arg
            elif opt in ('-s', '--silent'):
                silent = True
            elif opt in ('-w', '--warn'):
                 umbral_warning = int(arg)
            elif opt in ('-c', '--crit'):
                 umbral_critical = int(arg)

        date_today = datetime.datetime.now()#.strftime('%b %d %H:%M:%S %Y %Z')
        openssl_cmd='echo | openssl s_client -connect '+_host+':'+_port+' 2>/dev/null | openssl x509 -noout -dates'
        proc = os.popen(openssl_cmd).read().split('\n')
        
        expiredate = proc[1].split('=')[1]   # expiredate from cert
        obj_expiredate = datetime.datetime.strptime(expiredate, '%b %d %H:%M:%S %Y %Z') # object transformation
        diff_date = obj_expiredate - date_today # difference of obj_expiredate - date_today
        
        status = check_date_with_wcparams(obj_expiredate,date_today,diff_date,umbral_warning,umbral_critical) # Devuelve si es OK,W,C
        print_to_stdout(status,diff_date,silent) # Salida
