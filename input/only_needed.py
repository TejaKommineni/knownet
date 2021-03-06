import random
import csv
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pandas
import matplotlib.pyplot as plt
from matplotlib import mlab
from ipaddress import ip_address

def controlled_setting():
    generate_scanners()
    out = csv.writer(open("controlled-flows.csv","w"), delimiter=',',quoting=csv.QUOTE_ALL)
    out.writerow('source_ip,destination_ip,source_port,destination_port,protocol,tcp_flags,duration,packets,bytes'+"\n")
    i =0
    with open('features-flows-2017-12-05.csv', 'rU') as f:
        reader = csv.reader(f)
        for rec in csv.reader(f, delimiter=','):
            print(i)
            i = i +1
            with open('clustered-aggregated-features-flows-2017-12-05.csv', 'rU') as f1:
                reader1 = csv.reader(f1)
                for rec1 in csv.reader(f1, delimiter=','):
                    temp = rec1[0] 
                    temp = temp[1:]
                    temp = temp[:len(temp)-1]
                    if temp== rec[0]:
                        out.writerow(rec)
                        print(rec)
                       
            f1.close()            
    f.close()
    out.close()
 
def generate_scanners():
    ip_addresses = []
    destinations = []
    src_ports = [] 
    destn_ports = []
    tcp = []
    udp = []
    avg_bytes = []
    next = 0
    while len(ip_addresses) <100000:
        rang = random.randint(50,100)       
        for i in range(rang):
            ip_addresses.append(next)
        next = next+1
    while len(destinations) <100000:
        rang = random.randint(3,15)       
        for i in range(rang):
            destinations.append(next)
        next = next+1
    while len(src_ports) <100000:
        rang = random.randint(5,10)       
        for i in range(rang):
            src_ports.append(next)
        next = next+1
    while len(destn_ports) <100000:
        rang = random.randint(1,5)       
        for i in range(rang):
            destn_ports.append(next)
        next = next+1
    while len(avg_bytes) <100000:
        rang = random.randint(10,100)       
        for i in range(rang):
            destn_ports.append(rang)        
        
    return ip_addresses, destinations, src_ports, destn_ports, avg_bytes
            
    
controlled_setting()   
