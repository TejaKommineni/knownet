#!/usr/bin/python
#from feature_extractors import syn
#from nfml import get_features
import os
import sys
import json
import shutil
#import MySQLdb
from sklearn import datasets
from sklearn.datasets.samples_generator import make_blobs
import time
import numpy as np
from sklearn.preprocessing import scale
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import csv
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from matplotlib.gridspec import GridSpec
from sklearn import preprocessing
from sklearn.preprocessing import FunctionTransformer
from scipy.stats import boxcox
from sklearn.preprocessing import MinMaxScaler
#from docx import Document
#from docx.shared import Inches
from scipy.spatial import distance
from munkres import Munkres,print_matrix
from scipy.spatial.distance import cdist, pdist

def temp_cluster_to_file(file_name):
    centres1,set1,avg = cluster(file_name)
    centres = []
    print(centres1.tolist())
    data = {}	  
    file_name = file_name.split('-')     
    file_name = file_name[5].split('.')[0]+'/'+file_name[4]+'/'+file_name[3]	
    data[file_name] = []
    data[file_name].append({
	'cluster_centers' : centres1.tolist(),
	'cluster_sizes'   : set1,
	'cluster_averages': avg
    })    
    with open('../output/data.txt', 'w') as outfile:  
	    json.dump(data, outfile)
			
# Input : Number of Clusters
# Output : clustered.csv file in output folder that has each record and it's cluster number.
# Processing : We send the data through log transformation and then do min max scaling to bring all features between 0 to 1 and run clustering algorithm with specified number of clusters. The output is stored back in a file.
def cluster(file_name):
    start_time = time.time()
    f = open("../output/"+file_name)
    feature_set=[]
    featured_set=[]
    flag =False
    with open('../output/'+file_name, 'rU') as f:
         reader = csv.reader(f)
         for rec in csv.reader(f, delimiter=','):
          if flag == True and float(rec[13]) >1 and float(rec[9]) <10000  and rec[1]!='155.98.32.70' and rec[1]!= '155.98.33.74':
            if flag == True:		 		
                     tempd_list=[rec[0],int(rec[1]),int(rec[2]),int(rec[3]),int(rec[4]),int(rec[6]),int(rec[7]),float(rec[11]),float(rec[12]),float(rec[13])]
                     featured_set.append(tempd_list)
            if flag== True and int(rec[6])==0:
                    rec[6]=1
                    rec[1]=int(rec[1])+1
            if flag== True and int(rec[7])==0:
                    rec[7]=1
                    rec[1]=int(rec[1])+1
            if flag== True and float(rec[12])==0:    	    
                    rec[12]=1                
            if flag==True:
                    temp_list=[int(rec[1]),int(rec[2]),int(rec[3]),int(rec[4]),int(rec[6]),int(rec[7]),float(rec[12])]
                    feature_set.append(temp_list)
            else:
                  flag=True
    print('I am feature set and my size is ', len(feature_set)) 	
    a=np.array(feature_set,dtype=int)
    transformer = FunctionTransformer(np.log10)
    a = transformer.transform(a)
    a = MinMaxScaler(feature_range=(0, 1),copy=True).fit_transform(a)
    #wss = []
    #x_axis=[]
    #for k in range(1,31):
	#x_axis.append(k)
	#km = KMeans(n_clusters=k).fit(a)
	#centers = km.cluster_centers_
	#i =0
        #ss = 0
        #for x in np.nditer(km.labels_):
	    #center = centers[x]
	    #record = feature_set[i]
            #dist = cdist([center],[record])		    
	    #ss = ss + sum(dist**2)
 	#print(wss)	
       	#wss.append(ss)
    
    #plt.plot(x_axis,wss)
    #plt.show()	    	
    km = KMeans(n_clusters=7)
    km.fit(a)
    labeled_data=[]
    clusters={}
    for x in np.nditer(km.labels_):
        value =x.tolist()
        if value in clusters:
           clusters[value]+=1
        else:
           clusters[value]=1
        labeled_data.append(value)
    print(clusters)
    f1= open("../output/clustered-"+file_name,'w+')
    f1.write("source,total_flows,unique_destinations,unique_source_ports,unique_destination_ports,tcp_flows,udp_flows,total_bytes,avg_bytes,total_packets,cluster"+"\n")
    print(len(feature_set))
    print(len(labeled_data))
    i=0
    writer=csv.writer(f1)
    avg = {}
    for j in range(7):
	       avg[j]	= [0,0,0,0,0,0,0]
    for record in featured_set:
        record.append(labeled_data[i])
        avg[labeled_data[i]] =  [x + y for x, y in zip(avg[labeled_data[i]],record[1:])]
        writer.writerow(record)
        i=i+1
    f1.close()
    print("--- %s execution time of method cluster in seconds ---" % (time.time() - start_time))
    print(avg)
    print(list(km.cluster_centers_))
    print(clusters)
    for k,v in clusters.items():
	       avg[k]=[x /v for x in avg[k]]
    print(avg)
    with open('../output/data.txt') as json_file:
        data = json.load(json_file)
      
    file_name = file_name.split('-')
    file_name = file_name[5].split('.')[0]+'/'+file_name[4]+'/'+file_name[3]
    data[file_name] = []
    data[file_name].append({
        'cluster_centers' : km.cluster_centers_.tolist(),
        'cluster_sizes'   : clusters,
        'cluster_averages': avg
    })
    with open('../output/data.txt', 'w+') as outfile:
            json.dump(data, outfile)
		
    return km.cluster_centers_ , clusters, avg

# Before calling this method we have to create the knownet database, features table and create index for this table using srcip. Then insert features.csv into the table
# Output: aggregated.csv file is created in output folder.
# Processing: The code in this method executes a query that gives different aggregated values needed for our experiment.
#===============================================================================
# def features_to_aggregated_features(file_name):
#     #shutil.move('../output/features.csv','/var/lib/mysql-files/features.csv')
#     db = MySQLdb.connect("localhost","root","password","knownet")
#     cursor =db.cursor()    
#     sql = "SELECT DISTINCT sourceip  FROM features"
#     cursor.execute(sql)
#     results = cursor.fetchall()
#     start_time=time.time()
#     f= open("../output/aggregated-"+file_name,'w+')
#     f.write('source,total_flows,unique_destinations,unique_source_ports,unique_destination_ports,count_syn_flags,tcp_flows,udp_flows,icmp_flows,total_duration,avg_duration,total_bytecount,avg_bytecount,total_packets,avg_packets'+"\n")
#     for row in results:
#         second_cursor = db.cursor()
#         source_ip="'"+row[0]+"'"
#         second_cursor.execute("""SELECT
#         COUNT(sourceip) AS dist_src_ip,
#         COUNT(DISTINCT destinationip) AS dist_dest_ip,
#         COUNT(DISTINCT sourceport) AS dist_src_port,
#         COUNT(DISTINCT destinationport) AS dist_dest_port,
#         SUM(IF(flags='....S.',1,0)) AS count_syn,
#         SUM(IF(protocol='TCP',1,0)) AS count_tcp,
#         SUM(IF(protocol='UDP',1,0)) AS count_udp,
#         SUM(IF(protocol='ICMP',1,0)) AS count_icmp,
#         SUM(duration) AS sum_duration,
#         SUM(bytes) AS sum_bytecount,        
#         SUM(packets) AS sum_packets
#         FROM features where sourceip="""+source_ip)
#         distinct_count = second_cursor.fetchall()
# #        print(distinct_count[0][0])
#         avg_duration=distinct_count[0][8]/distinct_count[0][0]
#         avg_bytecount=distinct_count[0][9]/distinct_count[0][0]
#         avg_packets=distinct_count[0][10]/distinct_count[0][0]
#         f.write(source_ip+","+str(distinct_count[0][0])+","+str(distinct_count[0][1])+","+str(distinct_count[0][2])+","+str(distinct_count[0][3])+","+str(distinct_count[0][4])+","+str(distinct_count[0][5])+","+str(distinct_count[0][6])+","+str(distinct_count[0][7])+","+str(distinct_count[0][8])+","+str(avg_duration)+","+str(distinct_count[0][9])+","+str(avg_bytecount)+","+str(distinct_count[0][10])+","+str(avg_packets)+"\n")
#     f.close()
#     cursor.execute('drop table features;')
#     print("--- %s execution time of method features_to_aggregated_features in seconds ---" % (time.time() - start_time))
#     db.commit()
#     db.close()
#===============================================================================

#===============================================================================
# def csv_to_database(file_name):
#         start_time=time.time()
# 	db = MySQLdb.connect("localhost","root","password","knownet",local_infile=1)
# 	cursor =db.cursor()
# 	sql = """CREATE TABLE features(sourceip varchar(20),destinationip varchar(20),sourceport varchar(20),destinationport varchar(20),protocol varchar(20),
# flags varchar(20),duration float,packets float, bytes float);"""
# 	cursor.execute(sql)	
# 	sql = "LOAD DATA LOCAL INFILE '/proj/knownet/teja/knownet/output/"+file_name+"'INTO TABLE features FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 2 LINES;"
# 
# 	print(sql)	
# 	cursor.execute(sql)
# 	cursor.execute('create index source on features(sourceip);')
#         print("--- %s execution time of method csv_to_database in seconds ---" % (time.time() - start_time))	
# 
# # Input : This method takes in the netflow file name as input.
# # Output: A file named features.csv is generated and placed in output folder.
# # Processing: It picks only the required data from the netflow csv file and writes it to features file.
# def flows_to_features(file_name):
# 	start_time=time.time()
# 	f  = open('../input/'+file_name)
# 	f1 = open('../output/features-'+file_name, 'w+')
# 	f1.write("source_ip,destination_ip,source_port,destination_port,protocol,tcp_flags,duration,packets,bytes"+"\n")
# 	i =0
# 	try:
#         	for line in f:
# 			record=line.strip().split(',')
#              #   	print(i)
# 			i=i+1 
# 			f1.write(record[3]+","+record[4]+","+record[5]+","+record[6]+","+record[7]+","+record[8]+","+record[2]+","+record[11]+","+record[12]+"\n")
# 		f.close()
# 		f1.close()					
# 	except Exception:
# 		print('There was an exception at the end of the file')
# 	print("--- %s execution time of method flows_to_features in seconds ---" % (time.time() - start_time))
#===============================================================================
