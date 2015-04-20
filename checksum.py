from flask import Flask, abort, request
from urlparse import urlparse, parse_qsl
import hashlib

app = Flask(__name__)

ALLOW_NESTED_CHECKSUM = True

@app.route('/create-checksum')
def create_checksum():
    url = get_url(request, ALLOW_NESTED_CHECKSUM)

    return "{url}&checksum={checksum}".format(url=url, checksum=get_sha1(url))

@app.route('/check-checksum')
def check_checksum():
    url = get_url(request)
    checksum = get_checksum(request)

    if verify_checksum(url, checksum):
        return 'verified'
    else:
        abort(400)

def get_url(request, includeChecksum=False):
    params = parse_qsl(request.query_string)
    url = ''
    append = False
    for param in params[:-1]:
        if param[0] == 'url':
            url = param[1]
            if contains_query_string(url):
                append = True # include the rest of the querystring as part of the URL
            else:
                break
        elif append:
            url += to_query_string(param)

    # handle last/only parameter
    if params:
        param = params[-1]
        if (param[0] == 'url'):
            url = param[1]
        elif (append and (param[0] != 'checksum' or includeChecksum)):
            url += to_query_string(param)

    if not url:
        abort(400)

    return url

def to_query_string(param):
    return '&{name}={value}'.format(name=param[0], value=param[1])

def get_checksum(request):
    values = request.args.getlist('checksum')

    if not values:
        abort(400)

    return values[-1]

def contains_query_string(url):
    parsed = urlparse(url)
    return not not parsed.query

def get_sha1(string):
    return hashlib.sha1(string).hexdigest()

def verify_checksum(string, expected):
    actual = get_sha1(string)
    app.logger.debug('checksum: expected={0}, actual={1}'.format(expected, actual))
    return actual == expected

if __name__ == '__main__':
    app.debug = True #FIXME
    app.run()
