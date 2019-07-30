import subprocess
import curses
stdscr = curses.initscr()
curses.noecho()
import BasicTUI as BT
import npyscreen
import os
x = BT.screen()
num_workers = x[0]
model = (x[2])

#prints all data from TUI
#for i in x:
#    print(i)

def worker_add(file):
    f = open(file,'r')
    lines = f.readlines()

    for i in lines:
        if '#new worker' in i:
            pos = lines.index(i)
        if '#master code' in i:
            pos_m = lines.index(i)

    copy = lines[0:pos+1]
    l = lines[0:pos + 1]

    for i in range(1,num_workers):
        a = [x.replace('worker0','worker'+str(i)) for x in copy]
        l.extend(a)
        
    a = []
    
    if(model == 'K-Means Clustering'):    
        for i in range(0,num_workers):
             for  j in range(0,2):
                a = [x.replace('worker0','subworker'+str(i)+str(j)) for x in copy]
                a = [x.replace('km_worker_res','km_v3_subworker') for x in a]
                l.extend(a)
                
    l.extend(lines[pos_m:])
    f.close()

    f1 = open(file,'w')
    f1.writelines(l)
    f1.close()

os.system('cat ./deploy_creator.yaml > ./deploy_creator1.yaml')
os.system('cat ./svc_create.yaml > ./svc_create1.yaml')
worker_add('deploy_creator1.yaml')
worker_add('svc_create1.yaml')


#print('Creating cluster on GCP..')
#subprocess.call('make -f clusters.makefile create',shell=True)
#print('Cluster created on GCP!')

print('Setup started')
subprocess.call('./deploy_all.sh',shell=True)
