import pycurl
import argparse, shlex
from io import BytesIO, StringIO
import os, re, sys, getpass # JMW
import curl_config

parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('url', nargs='?') # make this optional
parser.add_argument('-d', '--data')
parser.add_argument('-o', '--output', default=None)
parser.add_argument('--data-binary', default=None) #JMW changed
parser.add_argument('-H', '--header', action='append', default=[])
parser.add_argument('--compressed', action='store_true')
parser.add_argument('-k', '--insecure', action='store_true') #JMW
parser.add_argument('-b', '--cookie', default=None) # JMW
parser.add_argument('-c', '--cookie-jar', default=None) # JMW
parser.add_argument('-L', '--location', action='store_true') # JMW
parser.add_argument('-K', '--config', nargs='?',
                    const='.curlrc') # JMW
parser.add_argument('--url')
parser.add_argument('-O','--remote-name', action='store_true')

def curl_translate(curl_command):
    method = "get"
    
    tokens = shlex.split(curl_command)
    parsed_args = parser.parse_args(tokens)

    if parsed_args.config: # config file specified
        if parsed_args.config == '-': 
            # read from stdin
            print "reading config from stdin"
            curl_command = sys.stdin.read()
        else:
            print "loading config file {}".format(parsed_args.config)
            curl_command = curl_config.convert(parsed_args.config)
        tokens = shlex.split(curl_command)
        parsed_args = parser.parse_args(tokens)

    print parsed_args # debug
    
    login = raw_input('Login: ')
    pw = getpass.getpass()

    buf = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, parsed_args.url)
    c.setopt(c.WRITEDATA, buf)
    if parsed_args.remote_name:
        parsed_args.output = parsed_args.url.split('/')[-1] # get file name from provided URL
    if parsed_args.location:
        # print "set FOLLOWLOCATION to 1" # debug
        c.setopt(c.FOLLOWLOCATION, 1)
    if parsed_args.insecure:
        # print "setting SSL_VERIFYPEER to False" # debug
        c.setopt(c.SSL_VERIFYPEER, False)
    if parsed_args.cookie:
        print "setting cookie to {}".format(parsed_args.cookie)
        c.setopt(c.COOKIEFILE, parsed_args.cookie)
    if parsed_args.cookie_jar:
        print "set cookie jar to {}".format(parsed_args.cookie_jar)
        c.setopt(c.COOKIEJAR, parsed_args.cookie_jar)

    if parsed_args.compressed:
        pass
        # TODO: set a header to accept compressed here
        #print "setting COMPRESSED to True"
    c.perform()
    # print "Status: {}".format(c.getinfo(c.RESPONSE_CODE)) # debug
    c.close()

    if parsed_args.output:
        with open(parsed_args.output, 'wb') as outfile:
            outfile.write(buf.getvalue())
    else:
        sys.stdout.write(buf.getvalue())

if __name__ == "__main__":
    curl_translate(sys.argv[1])  
