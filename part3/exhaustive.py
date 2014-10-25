from Crypto.Hash import SHA256
from hashes import hash_rand
from celery import Celery

app = Celery('tasks', broker='amqp://guest@localhost//')


charset = []

for i in range(33,127):
    charset.append(chr(i))

charset_len = len(charset)


@app.task
def printall_hashes(pf, pl):
    prefix = pf
    pass_len = pl
    if pass_len == 0:
        sha256 = SHA256.new(prefix)
        digest = sha256.hexdigest()
        if digest in hash_rand:
            result = digest + "\t" + prefix + "\n"
            r = open('result_rand','w')
            r.write(result)
            r.close()
            print "Found!---->", prefix
        return
    
    else:
        for i in range(0, charset_len):
            printall_hashes(prefix + charset[i], pass_len - 1)
