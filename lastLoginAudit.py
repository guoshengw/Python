# -*- coding: utf-8 -*-
"""
Created on Tue April 12 12:00:12 2019

@author: gw2389
"""

import glob,re,datetime, pyodbc, sys
try:
    ls = []
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=MSSQLPRODTS01\CUITSQLDBATS;'
                      'Database=DB_Inventory;'
                      'Trusted_Connection=yes;')
    
    cursor = conn.cursor()
    cursor.execute("SELECT shortservername, ErrorLogDirectory FROM t0t1_serverList where enabled='true'")
    
    for row in cursor:
        ls.append(row)
    sdic ={}
    
    for item in ls:
        serverName =item[0]
        print(serverName)
        udic ={}
        if len(glob.glob(item[1]))==0:
            raise RuntimeError('The error log files cannot be found in ' + item[1])
        for file in glob.glob(item[1]): 
            with open(file,encoding='utf-16') as f:
                for line in f:
                    m = re.match(".*(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d).*Login succeeded for user '(.*?)'.*\[CLIENT: (.*)\].*",line)
                    if m:
                        ls_1 = []
                        ls_1.append(m.group(1))
                        ls_1.append(m.group(3))
                        if m.group(2) in udic.keys():
                            if datetime.datetime.strptime(m.group(1), '%Y-%m-%d %H:%M:%S.%f') > datetime.datetime.strptime(udic[m.group(2)][0], '%Y-%m-%d %H:%M:%S.%f'):
                                
                                udic[m.group(2)][0] = m.group(1)
                                udic[m.group(2)][1] = m.group(3)
                        else:
                            udic[m.group(2)] = ls_1
        sdic[serverName]=udic
    ##print(sdic)
    cursor.execute('TRUNCATE TABLE t0t1_LastLogin;')
    conn.commit()
        
    for key, value in sdic.items():
        for key1, value1 in value.items():
            cursor.execute("INSERT INTO t0t1_LastLogin VALUES (?,?,?,?)",key,key1,value1[0],value1[1])
            conn.commit()
        
except Exception as e:
    print(e)
    sys.exit(-1)
finally:
    conn.close()