# -*- encoding: utf-8 -*-
#!/usr/bin/python2
#

#
#   Copyright (C) 2016 Ferran Serafini 
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License Version 2 as
#   published by the Free Software Foundation.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import os
import datetime
import sys
import getopt
import subprocess
from subprocess import PIPE,Popen


def print_to_stdout(diff_date,silent,obj_expiredate):
    if silent: # if only want to see value without logics 
        print str(diff_date.days)+','+str(obj_expiredate).split(' ')[0]
    else:
        print str(diff_date.days) +' days'

def usage(version):
        print 'Certcheck '+version+ '(LLSVDC)'
        print 'Usage: certcheck -H [Hostname or IP] -p [port] -w [days warning] -c [days critical] -s (silent)' 
        print ' -H --host: Hostname or IP'
        print ' -p --port: HTTPS port'
        print ' -s --silent: Returns only the number of the days remaining'
        print 'SEE THE MAN PAGE (https://github.com/fsmsystems/certcheck)  FOR MORE OPTIONS AND EXAMPLES'
        sys.exit(0)


def search_openssl():
    openssl_bin = os.popen('whereis openssl').read().split()[1]
    return openssl_bin

if __name__ == "__main__":
        version = '0.0.4'       # Version :)
        openssl_bin = search_openssl() # serach openssl binary with system whereis
        silent = False          # 
        _port = '443'           # Default port if is not passed as parameter

        try: 
            options, remainder = getopt.gnu_getopt(sys.argv[1:], 'H:p:hs', ['Host=','port=',])
        except getopt.GetoptError,e:
            print 'LOL: You miss something!!',e
            sys.exit(1)
        #print 'OPTIONS   :', options
        if options:     # don't die with blank parameters
         for opt, arg in options:
            if opt in ('-h', '--help'):
                usage(version)
            elif opt in ('-H','--host'):
                 _host = arg
            elif opt in ('-p', '--port'):
                _port = arg
            elif opt in ('-s', '--silent'):
                silent = True
        else:
             usage(version) # like good commands

        date_today = datetime.datetime.now()    # Today Now date to compare

        try:    # This will be the command to send to system with openssl
            openssl_cmd='echo | '+openssl_bin+' s_client -connect '+str(_host)+':'+str(_port)+' 2>/dev/null | '+openssl_bin+' x509 -noout -dates'
        except NameError:
            print "Check the inserted parameters please. Is missing something"
            sys.exit(1)

        # This implementation is for compatibility with python 2.6 from the past machines!!
        p = Popen([openssl_cmd], stdout=PIPE, shell=True, stderr=subprocess.STDOUT )
        proc = p.communicate()[0].split('\n')
    
        if 'unable to load certificate' in proc[0]: # Preventing to see the ugly error from openssl command
            print 'Unable to load certificate. Check entered host and try again'
            sys.exit(1)
        else:
            expiredate = proc[1].split('=')[1]   # Expiredate from certificate read with openssl
            obj_expiredate = datetime.datetime.strptime(expiredate, '%b %d %H:%M:%S %Y %Z') # object transformation
            diff_date = obj_expiredate - date_today # difference of obj_expiredate - date_today
            print_to_stdout(diff_date,silent,obj_expiredate) # Output
