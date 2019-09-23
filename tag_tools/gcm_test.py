# python3
import hashlib
import hmac
import urllib.parse

protocol = 'http'
host = '127.0.0.1:8000'
# key = 'S6m9HLqCmFeKyuZk'
key = 'FVqLmdjQP9hTvuJq' # n
# secret = 'YZPn4SqrUwznTqJUqTTRlHmLMKK80Tjo'
secret = 'f6Nk3BekSdsQQ9VPBuLZOybNE6nOUuAl' # n
uri = '/api/v1/datasets/1'
qs = 'a=2&b=1'
content = ''
date = 'Mon, 3 Jan 2010 08:33:47 GMT'
nonce = "nonce1234"
method = 'GET'
path = urllib.parse.quote('/api/v1/datasets/1', safe='')
args = urllib.parse.quote('a=2&b=1', safe='')

get_sign = hmac.new(
    secret.encode('utf-8'),
    '&'.join([method, path, args, "", date, nonce, key]).encode('utf-8'),
    hashlib.sha1).hexdigest()

print('&'.join([method, path, args, "", date, nonce, key]).encode('utf-8'))
print('cmd: curl -v -k -X %s -d %s "%s://%s%s?%s" -H "X-Request-Method: GET" -H "X-Request-Path: /api/v1/datasets/1?a=2&b=1" -H "X-Request-Date: %s" -H "X-Request-Nonce: %s" -H "Authorization: HUBBLE %s:%s"' %
        (method, content, protocol, host, uri, qs, date, nonce, key, get_sign))