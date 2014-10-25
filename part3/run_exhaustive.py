from exhaustive import *

task_prefix = 2

for i in range(0,len(charset)):
    for j in range(0,len(charset)):
        print "New Node",j 
        printall_hashes.delay(charset[i]+charset[j], 3)


 
