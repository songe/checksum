from flask import Flask, abort, request
import hashlib

app = Flask(__name__)

@app.route('/create-checksum')
def create_checksum():
    url = get_query_param('url')
    return "{url}&checksum={checksum}".format(url=url, checksum=get_sha1(url))

@app.route('/check-checksum')
def check_checksum():
    url = get_query_param('url')
    checksum = get_query_param('checksum')

    if verify_checksum(url, checksum):
        return 'verified'
    else:
        abort(400)

def get_query_param(name, abortIfNone=True):
    value = request.args.get(name)
    app.logger.debug('%s: %s', name, value)

    if abortIfNone and value is None:
        abort(400)

    return value

def get_sha1(string):
    return hashlib.sha1(string).hexdigest()

def verify_checksum(string, expected):
    actual = get_sha1(string)
    return actual == expected

if __name__ == '__main__':
    app.debug = True #FIXME
    app.run()
