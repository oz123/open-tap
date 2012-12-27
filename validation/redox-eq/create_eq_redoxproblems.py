#!/usr/bin/python

# create problem directories and files for running the ionx problem
# in OS and GIM modes in the following Courant Numbers, ion exchange
# capacities and Total run times:
# Cr Numbers = 0.1, 1.0, 10.0
# Ion Exchange Capacity = 0.0175, 0.175, 1.75, 17.5
# Days = 15, 150, 1500, 15000
# Output times: 5,15,30,150,300,1500, 3000,15000

import os
import shutil
Crs=['0.1', '1.0','10']
days=['5','5','5']
#time steps controling the Cr number
timeSteps=['0.025d0','0.25d0','2.5d0']
 
#create directories
#for v in VC:
    #os.mkdir(v+'VC')
    #os.chdir(v+'VC')
    #for Cr in Crs:
        #os.mkdir(Cr)      
    #os.chdir('..')
            

#read template file
templateF=open('redox_template_eq.dat','r')
templateF=templateF.readlines()

outPutTimes=['10.0','10.0','10.0']

#insert file with correct Cr number to each direcory with GIM mode,
#write correct output times
for i in xrange(len(timeSteps)):
    os.chdir(Crs[i])
    templateF=open('../redox_template_eq.dat','r')
    templateF=templateF.readlines()
    tempFile=templateF   
    #print tempFile
    #raw_input("\n\nPress the enter key to exit.")
     #modify header
    tempFile[5]=tempFile[5][:-2]+timeSteps[i]+'\n'
    print tempFile[5]
    tempFile[7]=tempFile[7][:-2]+timeSteps[i]+'/0.25 ='+Crs[i]+'\n'
    #modify min. max. time steps
    tempFile[98]=timeSteps[i]+tempFile[98]
    
    tempFile[97]=timeSteps[i]+tempFile[97]
    
    #modify final solution time
    tempFile[96]=outPutTimes[i]+'d0'+tempFile[96]    
    #modify output times
    tempFile[182]=days[i]+'d0 '+outPutTimes[i]+'d0'+tempFile[182]
    #choose solution method GIM
    tempFile[147]=tempFile[147][1:]
    
    print os.getcwd()
    #print tempFile
    f=open('equil-mixgim.dat','w')
    f.writelines(tempFile)
    f.close()
    raw_input("\n\nPress the enter key to exit.")
    f=open('equil-mixos.dat','w')
    # insert operation split
    tempFile[146]=tempFile[146][1:]
    tempFile[147]="!"+tempFile[147]
    f.writelines(tempFile)
    f.close()
    tempFile=[]
    print "at end", tempFile
    os.chdir('..')   
    
    raw_input("\n\nPress the enter key to exit.")
