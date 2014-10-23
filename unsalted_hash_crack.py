import sys
from Crypto.Hash import SHA256
from celery import Celery

app = Celery('tasks', broker='amqp://guest@localhost//')

hash_nosalt = [\
              '6ca52258a43795ab5c89513f9984b8f3d3d0aa61fb7792ecefe8d90010ee39f2',\
              '3ed7277d453de87de1ff43780dd2fe3288d6f0110b35efd7cff339ec1010d0ac',\
              'b10a28c941345adca500690e77d5ff0a0036ccf414ee9fd132569d55021ded33',\
              'db5b14610f668b1a4c24f501cfc8125e03c67fcb032fa6b294a3ef63abb0cfc3',\
              '927c449a69cdd7fb2e4e9dc45801cfae21d27ddceb2056d37b660e155633b5de',\
              ]

hash_salted = [\
            '80387:3e3e74770c8ab2a1b42d77ce0d4a19220187f289e434bd710527fa773f445003',\
            '33981:210c07ee8e84b84348dd96938dc7cdcf000866be6ab554de1b822f8497798e3b',\
            '45432:e2912cf9efaee95b09de244c55f94029f5b163bd94f8d3a2c6f9efd55668636e',\
            '25271:f1b812e9b6ae7cf240f5514f08d26234145679413db882f4b92104cc49fa9cfc',\
            '72518:07031ca1e515aa4c54f11c47cf81f04f684d1de7926e8fcc522880b6364457ce',\
            '12984:8bdd0dc96c9d83665eeb04eb4b8bcfb14d27a75cc308d320004f6410fd88f132',\
            ]



hash_salted_dict = {}
for h in hash_salted:
    fields = h.partition(":")
    hash_salted_dict[fields[0]] = fields[2]





f = open('pass/rockyou.100000.txt','r')
passwords = f.readlines()
f.close()

pass_dict = {}
f = open('pass/rockyou.100000.hash','r')
for line in f:
    line = line.strip("\n")
    fields = line.partition(" ")
    pass_dict[fields[0]] = fields[2]
f.close()



@app.task
def unsalted_crack_dictionary():
    for h in hash_nosalt:
        if h in pass_dict:
            r = open('result_nosalt_dict/'+h, 'w')
            r.write(h + "\t" + pass_dict[h] + '\n')
            r.close()


@app.task
def unsalted_crack_digits_ap(start,end):
    for i in range(start, end):
        curr_pass = passwords[i].strip("\n")
        for digit in range(0,10):
            a = curr_pass + str(digit)
            p = str(digit) + curr_pass
            
            a_sha256 = SHA256.new(a)        
            p_sha256 = SHA256.new(p) 
            
            a_digest = a_sha256.hexdigest()
            p_digest = p_sha256.hexdigest()

         
            if a_digest in hash_nosalt:
                r = open('result_crack_digits_ap/'+ a_digest, 'w')
                result = a_digest + "\t" + a + "\n"
                r.write(result)
                r.close()
                print "Found!---> ", result

            if p_digest in hash_nosalt:
                r = open('result_crack_digits_ap/'+ p_digest, 'w')
                result = p_digest + "\t" + p + "\n"
                r.write(result)
                r.close()
                print "Found!---> ", result
        

@app.task
def salted_crack_aps(start, end):
    for i in range (start, end):
        curr_pass = passwords[i].strip("\n")
        for h in hash_salted:
            fields = h.partition(":")
            salt = fields[0]
            salted_pass = curr_pass + fields[0]
            
            #print salted_pass

            sha256_s = SHA256.new(salted_pass)
            
            s_digest = sha256_s.hexdigest()
            
            if s_digest == fields[2]:
                r = open('result_salted/'+ s_digest, 'w')
                result = s_digest + "\t" + salt + " : " + curr_pass + "\n"
                r.write(result)
                r.close()
                print "Found!---> ", result
            
            for digit in range(0,10):
                a = salt + curr_pass + str(digit)
                p = salt + str(digit) + curr_pass

                a_sha256 = SHA256.new(a)
                p_sha256 = SHA256.new(p)

                a_digest = a_sha256.hexdigest()
                p_digest = p_sha256.hexdigest()
            
                #print a
                #print p
                
                if a_digest == fields[2]:
                    r = open('result_salted/'+ a_digest, 'w')
                    result = a_digest + "\t" + salt + " : " + curr_pass + str(digit) + "\n"
                    r.write(result)
                    r.close()
                    print "Found!---> ", result

                if p_digest == fields[2]:
                    r = open('result_salted/'+ p_digest, 'w')
                    result = p_digest + "\t" + salt + " : " + str(digit) + curr_pass + "\n"
                    r.write(result)
                    r.close()
                    print "Found!---> ", result







@app.task
def salted_crack_combinitions(start, end):

    for i in range(start, end):
        curr_pass = passwords[i].strip("\n")
        print curr_pass
        for other in passwords:
            other = other.strip("\n")
           
            for h in hash_salted_dict:
                appended = h + curr_pass + other
                
                a_sha256 = SHA256.new(appended)

                a_digest = a_sha256.hexdigest()
               
                #print appended 
               
                if a_digest == hash_salted_dict[h]:
                    r = open('result_salted_combinition/'+ a_digest, 'w')
                    result = a_digest + "\t" + h + " : "   + curr_pass + other + " : "+ appended + "\n"
                    r.write(result)
                    r.close()
                    print "Found!---> ", result




@app.task
def unsalted_crack_combinitions(start, end):

    for i in range(start, end):
        curr_pass = passwords[i].strip("\n")
        print curr_pass
        for other in passwords:
            other = other.strip("\n")
            appended = curr_pass + other
            prepended = other + curr_pass
            
            a_sha256 = SHA256.new(appended)
            p_sha256 = SHA256.new(prepended)

            a_digest = a_sha256.hexdigest()
            p_digest = p_sha256.hexdigest()
            
            #print appended, a_digest
            #print prepended, p_digest
           
            if a_digest in hash_nosalt:
                r = open('result/'+ a_digest, 'w')
                result = a_digest + "\t" + appended
                r.write(result)
                r.close()
                print "Found!---> ", result

            if p_digest in hash_nosalt:
                r = open('result/'+ p_digest, 'w')
                result = p_digest + "\t" + prepended
                r.write(result)
                r.close()
                print "Found!---> ", result

#combinitions_in_range(0,10)











#pass_dict = {}

#f = open('rockyou.100000.hash','r')
#for line in f:
    #x = line.strip('\n')
    #x = x.partition(' ')
    #pass_dict[x[0]] = x[2]
#for i in range(0,10):
    #a = x[2] + str(i)
    #p = str(i) + x[2]
    #hash_append = SHA256.new(a)
    #hash_prepend = SHA256.new(p)
    #pass_dict[a] = hash_append.hexdigest()
    #pass_dict[p] = hash_prepend.hexdigest()
#f.close()


#print "Dictionary length", len(pass_dict)
#print "\nResults--\n"
#for h in hash_nosalt:
    #if h in pass_dict:
        #print h, pass_dict[h]

#f = open('rockyou.100000.txt','r')
#lines = f.readlines()
#f.close()

#count = 0
#for h in hash_salted:
    #x = h.split(":")
    #salt = x[0]
    #hs = x[1]
    #count = count + 1
    #print "----", count, "----"
    #found = False 
    #for password in lines:
        #password = password.strip("\n")
        #salted_pass = salt + password
        #sha256 = SHA256.new(salted_pass)
        #if sha256.hexdigest() == hs:
            #print "Found!", hs, password
            #break
        
        #for i in range(0,10):
            #a = password+str(i)
            #p = str(i)+str(i)
            #salted_a = salt + a
            #salted_p = salt + p

            #sha256_a = SHA256.new(salted_a)
            #sha256_p = SHA256.new(salted_p)

            #if sha256_a.hexdigest() == hs:
                #print "Found!", hs, a
                #found = True        
            #if sha256_p.hexdigest() == hs:
                #print "Found!", hs, p
                #found = True

        #if found:
            #found = False
            #break


##Salted Hashes










##print "Looking for joined passwords..."
##count = 0
##for line1 in lines:
    ##for line2 in lines:
    ##joined_password = line1.strip('\n') + line2.strip('\n')
##h = SHA256.new(joined_password)
    ###pass_dict[h.hexdigest()] = joined_password
##sha256 = h.hexdigest()
    ##if sha256 in hash_nosalt:
    ##print "Found!->>>>", sha256, joined_password
    ##count = count + 1

    ##if count%1000 == 0:
    ##print "----",count,"----"

