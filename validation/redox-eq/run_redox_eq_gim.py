#!/usr/bin/python

import os
from time import *

#define parameters
dirs=['0.1', '1.0','10']
#dirs=['0.1']
#dirs=['1.0','10']
#problems=['equil-mixgim','equil-mixos']
problems=['equil-mixgim']
min3p='../../../min3p_gfortran.e'

#open cpu info
cpu=open('/proc/cpuinfo')
#advance to the right place in the file
for i in range(3):
    cpu.next()

#open log file
f=open('redox_eq_run_gim.log','w')
l='file\t\t\tCourant Number\t\tRun Time [sec]\t\t Time'\
    ' [hours:min:sec]\t\tExit Status\n'

f.write(l)
f.close()

delX=0.25
stepCounter=0
sumTs=0.0
endLine='         ***************** normal exit ********'\
         +'**********\n'

normalExit='N'
for j in xrange(len(dirs)):
    for i in xrange(len(problems)):
        f=open('redox_eq_run_gim.log','a')
        os.chdir(dirs[j])
        a = time()
        os.system(min3p+'\t'+problems[i])
        b = time()-a
        #caluclate average Cr Number:
        log=open(problems[i]+'.log','r')
        log=log.readlines()
        if log[-3]==endLine:
            normalExit='Y'
        else:
            normalExit='N'
        for line in log:
            if line[0:8]=='timestep':
                stepCounter=stepCounter+1
                sumTs=sumTs+float(line[52:61])
        avgT=sumTs/stepCounter
        print avgT
        avgCr=avgT/delX
        avgCr=str(avgCr)
        avgCr=avgCr[0:5]
        os.chdir('..')
        l=dirs[j]+'\\'+problems[i]+'.dat'+'\t\t\t'+avgCr+'\t\t\t'\
          +str(b)+'\t\t\t'\
          +str(int(b/3600))+'h:'+str(int(b/60))+'m:'\
          +str(int(b%60))+'s\t\t'+normalExit+'\n'
        print l
        #raw_input("\n\nPress the enter key to exit.")
        f.write(l)        
        f.close() 
        sumTs=0.0
        stepCounter=0 
          
#write cpu info to file
f=open('redox_eq_run_gim.log','a')
f.write('\n\nCPU INFO\n\n')
for i in range(4):
    f.write(cpu.next())
#close log file
f.close()
