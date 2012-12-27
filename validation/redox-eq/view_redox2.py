# python script to view files with techplot header
# make sure you run this script in the library of the outputs.
# you can also run python from the command line typing python
# then you can interact with python like with matlab shell
#import pdb
from pylab import *
import numpy as N
from matplotlib.ticker import Formatter
import os
#class to produce scientific format numbering
class SciFormatter(Formatter):
    def __call__(self, x, pos=None):
        return "%0.E" % x

def read_array2(filename, dtypes,lineskip=3, separator='  '):
    """ Read a file with an arbitrary number of columns.
        The type of data in each column is arbitrary
        It will be cast to the given dtype at runtime
        This is an improved function that also cleanes the data
    """
    startFromLine = lineskip 
    linesCounter = 1
    cast = N.cast
    # a nice syntax to initialize a list with determine size
    data = [[] for dummy in xrange(len(dtypes))]
    for line in open(filename, 'r'):
        #print type(line)
        if linesCounter>startFromLine:
            fields = line.strip().split(separator)
            #clean double numbers because of minus signs
            for i, number in enumerate(fields):
                temp=number.split(" ")
                if len(temp)>1:
                    #pdb.set_trace()
                    del fields[i]
                    for j, hold in enumerate(temp):
                        #print j, hold
                        #pdb.set_trace()
                        fields.insert(i+j,hold)
                        #print len(fields)
                    del temp
            #remove trailing error zeros in fields
            for i, number in enumerate(fields):
                if number[-4]=='-':
                    hold=number[:-4]
                    hold=hold+'e-23'
                    del fields[i]
                    fields.insert(i,hold)
            #split fields and append to data
            for i, number in enumerate(fields):
                data[i].append(number)
               #data[i].append(number)
        linesCounter=linesCounter+1
    #cast data to a nice array
    #pdb.set_trace()
    for i in xrange(len(dtypes)):
        data[i] = cast[dtypes[i]](data[i])
    return N.rec.array(data, dtype=dtypes)
#variables = "x", "y", "z", "K_xx", "K_yy", "K_zz"

def readTechPlotHeader(fileName):
    '''
    This function reads a Techplot file header 
    format. It returns a list which can be used in 
    other functions, to visualize techplot file format
    data using Python.
    the function takes in a file name.
    '''
    fileObject=open(fileName, 'r')
    fileObject.next()
    header=fileObject.next()
    #remove the expresions 'variables = ' and '\n' 
    header=header[12:-1]
    headerCopy=header
    #remove all commas, and convert to list
    header=header.strip().split(',')
    for x in xrange(len(header)):
        header[x]=header[x].strip(' ')
        header[x]=(header[x].strip("\""),'float32')
    fileObject.close()
    return header, headerCopy


#read all data from 3 directories
Crs=['0.1', '1.0','10']
#Crs=['0.1']#, '1.0','10']

datagim=[0]*3
dataos=[0]*3

i=0
for Cr in Crs:
    os.chdir(Cr)
    print os.getcwd()
    gsp_descr,headerCopy=readTechPlotHeader('equil-mixgim_1.gst')
    gsp_descr=N.dtype(gsp_descr)
    datagim[i]=read_array2('equil-mixgim_1.gst', gsp_descr)
    dataos[i]=read_array2('equil-mixos_1.gst', gsp_descr)
    os.chdir('..')
    i=i+1

#variables=["o2(aq)","co3-2","h+1","ch2o"]    
variables=["o2(aq)","so4-2","co3-2","hs-1"\
           ,"ch4(aq)"]
#variables=["o2(aq)","h+1","na+1","so4-2","co3-2","hs-1"\
           #,"ch4(aq)"]

#fig = plt.figure(1)
#plot all concentrations gim
#plt.subplot(131)
#for j in xrange(len(variables)):
#for i in xrange(len(variables)):
#plot(datagim[0]["x"][:41],datagim[0]["so4-2"][:41],'k-')
#plot(datagim[0]["x"][:41],datagim[0]["o2(aq)"][:41],'k-')
#plot(datagim[0]["x"][:41],datagim[0]["co3-2"][:41],'k-')
#plot(datagim[0]["x"][:41],datagim[0]["ch4(aq)"][:41],'k-')
#plot(datagim[0]["x"][:41],datagim[0]["hs-1"][:41],'k-')


#print datagim[1]["x"]
#print datagim[2]["x"]
    #plot(dataos[0]["x"],dataos[0][variables[i]],'r-')

#plot all concentrations gim
#plt.subplot(131)
#for j in xrange(len(variables)):


#for v in variables:
    #plot(datagim[0]["x"][:41],datagim[0][v][:41],'-',label=v+'gim')
    ##plot(dataos[0]["x"][:41],dataos[0][v][:41],'--',label=v+'os')
#legend()

fig = plt.figure(1)
for v in variables:
    plot(datagim[0]["x"][:41],datagim[0][v][:41],'-',label=v+'gim')
    plot(dataos[0]["x"][:41],dataos[0][v][:41],'--',label=v+'os')
#plot(dataos[0]["x"][:41],dataos[0]["hs-1"][:41],'--',label='os')
#plot(datagim[0]["x"][:41],datagim[0]["hs-1"][:41],'--',label='gim')

legend()


fig = plt.figure(2)
ax1 = fig.add_subplot(111)
fig.subplots_adjust(bottom=0.05,top=0.95)
##for d in xrange(len(datagim)):
plot(datagim[0]["x"][:41],datagim[0]["co3-2"][:41],'k-',label="Cr "+Crs[0])
plot(datagim[1]["x"][:41],datagim[1]["co3-2"][:41],'k--',label="Cr "+Crs[1])
plot(datagim[2]["x"][:41],datagim[2]["co3-2"][:41],'k-.',label="Cr "+Crs[2])
xlabel("distance [m]")
ylabel(r'$CO_3^{2-}$' "mol/l")
ax1.yaxis.set_major_formatter(SciFormatter())
title("GIM")
legend()


fig = plt.figure(3)
##for d in xrange(len(datagim)):
plot(dataos[0]["x"][:41],dataos[0]["co3-2"][:41],'k-',label="Cr "+Crs[0])
plot(dataos[1]["x"][:41],dataos[1]["co3-2"][:41],'k--',label="Cr "+Crs[1])
plot(dataos[2]["x"][:41],dataos[2]["co3-2"][:41],'k-.',label="Cr "+Crs[2])
xlabel("distance [m]")
ylabel(r'$CO_3^{2-}$' "mol/l")
title("SNIA")
legend()

fig = plt.figure(4)
##for d in xrange(len(datagim)):
plot(dataos[0]["x"][:41],dataos[0]["co3-2"][:41],'r-',label="Cr "+Crs[0])
plot(dataos[1]["x"][:41],dataos[1]["co3-2"][:41],'r--',label="Cr "+Crs[1])
plot(dataos[2]["x"][:41],dataos[2]["co3-2"][:41],'r-o',label="Cr "+Crs[2])
plot(dataos[0]["x"][:41],datagim[0]["co3-2"][:41],'k-',label="GIM Cr "+Crs[0])
plot(dataos[1]["x"][:41],datagim[1]["co3-2"][:41],'k--',label="GIM Cr "+Crs[1])
plot(dataos[2]["x"][:41],datagim[2]["co3-2"][:41],'k-.',label="GIM Cr "+Crs[2])
xlabel("distance [m]")
ylabel(r'$CO_3^{2-}$' "mol/l")
title("SNIA")
legend(loc=2)

show()

#days=[0,1,10,20,40,50]
#titles=["initial", "day 1","day 10","day 20","day 40","day 50"]
#fig = plt.figure()
#lend=len(days)
##print c
##print type(c)
#for i in xrange(len(days)-1):
    #print type(i)
    ##b=100+10*lend+(i+1)
    #b=511+i
    #print b,i
    #ax1 = fig.add_subplot(b)
    #a=ax1.plot(data[0]['x'],data[i+1]['o2(aq)'],'-o', label="o2(aq)")
    #b=ax1.plot(initial['x'],data[i+1]['ch2o'],'-x',label="ch2o")
    #c=ax1.plot(initial['x'],data[i+1]['co3-2'],'-+',label="co3-2")
    ##c=ax1.plot(initial['x'],data[i][''],'-')
    #ax1.set_ylabel('[mmol/l]')
    #t=ax1.set_title('day'+str(days[i+1]))
    #t.set_position((0.5,1.05))
    #ax1.grid()
###ax1 = fig.add_subplot(151)
#a=ax1.plot(initial['x'],day1['o2(aq)'],'-')
#b=ax1.plot(initial['x'],day1['co3-2'],'-')
#c=ax1.plot(initial['x'],day1['ch2o'],'-')

#ax1.xaxis.tick_top()
#ax1.set_title('K_zz')
#ax1.xaxis.set_major_formatter(SciFormatter())

#bottom, top = ax1.get_ylim()
#fig.ylim(top,bottom)
#ax1.set_ylim(top, bottom)
#ax1.set_xlim(0, max(day1['s_w']))
#ax1.set_xticklables(ax1.get_xticklabels,size=6,rotation=30)
#setp(plt.gca().get_xmajorticklabels(),
#         size=10,rotation=30)



#ax1 = fig.add_subplot(152)
#ax1.plot(day10['h_w'],day1['z'],'-')
##ax1.plot(day1['p_w'],day1['z'],'-')
#ax1.plot(day10['s_w'],day1['z'],'-')
#ax1.plot(day10['theta_w'],day1['z'],'-')
##ax1.plot(day1['p_w'],day1['z'],'-')
#ax1.plot(day10['theta_g'],day1['z'],'-')
#ax1.plot(day10['evap'],day1['z'],'-')
#ax1.xaxis.tick_top()
##ax1.set_title('K_zz')
##ax1.xaxis.set_major_formatter(SciFormatter())
##ax1.set_ylabel('Depth')
#bottom, top = ax1.get_ylim()
##fig.ylim(top,bottom)
#ax1.set_ylim(top, bottom)
#ax1.set_xlim(0, max(day1['s_w']))
#ax1.grid()
#ax1.set_yticklabels([])

#setp(plt.gca().get_xmajorticklabels(),
         #size=10,rotation=30)
#t=ax1.set_title('day 10')
#t.set_position((0.5,1.05))
         
#ax1 = fig.add_subplot(153)
#ax1.plot(day20['h_w'],day1['z'],'-')
##ax1.plot(day1['p_w'],day1['z'],'-')
#ax1.plot(day20['s_w'],day1['z'],'-')
#ax1.plot(day20['theta_w'],day1['z'],'-')
##ax1.plot(day1['p_w'],day1['z'],'-')
#ax1.plot(day20['theta_g'],day1['z'],'-')
#ax1.plot(day20['evap'],day1['z'],'-')
#ax1.xaxis.tick_top()
##ax1.set_title('K_zz')
##ax1.xaxis.set_major_formatter(SciFormatter())
##ax1.set_ylabel('Depth')
#bottom, top = ax1.get_ylim()
##fig.ylim(top,bottom)
#ax1.set_ylim(top, bottom)
#ax1.set_xlim(0, max(day1['s_w']))
#ax1.grid()
#ax1.set_yticklabels([])
##position=(1,2)
#t=ax1.set_title('day 20', position=(100,100))
#t.set_position((0.5, 1.05))
#setp(plt.gca().get_xmajorticklabels(),
         #size=10,rotation=30)


#ax1 = fig.add_subplot(154)
#ax1.plot(day30['h_w'],day1['z'],'-')
##ax1.plot(day1['p_w'],day1['z'],'-')
#ax1.plot(day30['s_w'],day1['z'],'-')
#ax1.plot(day30['theta_w'],day1['z'],'-')
##ax1.plot(day1['p_w'],day1['z'],'-')
#ax1.plot(day30['theta_g'],day1['z'],'-')
#ax1.plot(day30['evap'],day1['z'],'-')
#ax1.xaxis.tick_top()
##ax1.set_title('K_zz')
##ax1.xaxis.set_major_formatter(SciFormatter())
##ax1.set_ylabel('Depth')
#bottom, top = ax1.get_ylim()
##fig.ylim(top,bottom)
#ax1.set_ylim(top, bottom)
#ax1.set_xlim(0, max(day1['s_w']))
#ax1.grid()
#ax1.set_yticklabels([])
#t=ax1.set_title('day 30')
#t.set_position((0.5, 1.05))
#setp(plt.gca().get_xmajorticklabels(),
         #size=10,rotation=30)
                  

#ax1 = fig.add_subplot(155)
#ax1.plot(day30['h_w'],day1['z'],'-')
##ax1.plot(day1['p_w'],day1['z'],'-')
#ax1.plot(day30['s_w'],day1['z'],'-')
#ax1.plot(day30['theta_w'],day1['z'],'-')
##ax1.plot(day1['p_w'],day1['z'],'-')
#ax1.plot(day30['theta_g'],day1['z'],'-')
#ax1.plot(day30['evap'],day1['z'],'-')
#ax1.xaxis.tick_top()
##ax1.set_title('K_zz')
##ax1.xaxis.set_major_formatter(SciFormatter())
##ax1.set_ylabel('Depth')
#bottom, top = ax1.get_ylim()
##fig.ylim(top,bottom)
#ax1.set_ylim(top, bottom)
#ax1.set_xlim(0, max(day1['s_w']))
#ax1.grid()
#ax1.set_yticklabels([])
#t=ax1.set_title('day 50')
#t.set_position((0.5, 1.05))

#setp(plt.gca().get_xmajorticklabels(),
         #size=10,rotation=30)
                
#legend(loc='lower center')
#figlegend(a,b,c,'lower center',ncol=3)
          #('h_w', 's_w', 'theta_w','theta_g','evap'),
#         'lower center',ncol=3)
#show()

#show()
