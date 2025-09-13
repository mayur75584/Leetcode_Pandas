'''
3451. Find Invalid IP Addresses
Solved
Hard
Topics
premium lock icon
Companies
SQL Schema
Pandas Schema
Table:  logs

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| log_id      | int     |
| ip          | varchar |
| status_code | int     |
+-------------+---------+
log_id is the unique key for this table.
Each row contains server access log information including IP address and HTTP status code.
Write a solution to find invalid IP addresses. An IPv4 address is invalid if it meets any of these conditions:

Contains numbers greater than 255 in any octet
Has leading zeros in any octet (like 01.02.03.04)
Has less or more than 4 octets
Return the result table ordered by invalid_count, ip in descending order respectively. 

The result format is in the following example.

 

Example:

Input:

logs table:

+--------+---------------+-------------+
| log_id | ip            | status_code | 
+--------+---------------+-------------+
| 1      | 192.168.1.1   | 200         | 
| 2      | 256.1.2.3     | 404         | 
| 3      | 192.168.001.1 | 200         | 
| 4      | 192.168.1.1   | 200         | 
| 5      | 192.168.1     | 500         | 
| 6      | 256.1.2.3     | 404         | 
| 7      | 192.168.001.1 | 200         | 
+--------+---------------+-------------+
Output:

+---------------+--------------+
| ip            | invalid_count|
+---------------+--------------+
| 256.1.2.3     | 2            |
| 192.168.001.1 | 2            |
| 192.168.1     | 1            |
+---------------+--------------+
Explanation:

256.1.2.3 is invalid because 256 > 255
192.168.001.1 is invalid because of leading zeros
192.168.1 is invalid because it has only 3 octets
The output table is ordered by invalid_count, ip in descending order respectively.
'''

import pandas as pd

def find_invalid_ips(logs: pd.DataFrame) -> pd.DataFrame:
    logs["split"] = logs["ip"].str.split(".")
    # print(logs)
    # lst = list(logs["split"])
    logs["lst"] = list(logs["split"])
    # print(logs["lst"])
    invalid_log_id = []
    for index,row in logs.iterrows():
        # print(str(row["lst"][0])[0])
        
        if len(row["lst"])!=4 or str(row["lst"][0])[0]=="0" or str(row["lst"][1])[0]=="0" or str(row["lst"][2])[0]=="0" or str(row["lst"][3])[0]=="0" or int(row["lst"][0])>255 or int(row["lst"][1])>255 or int(row["lst"][2])>255 or int(row["lst"][3])>255:
            invalid_log_id.append(row["log_id"])
    # print(invalid_log_id) 
    # print(logs)
    logs = logs[logs["log_id"].isin(invalid_log_id)]
    # print(logs)
    logs = logs.groupby("ip").size().reset_index(name="invalid_count")
    logs = logs.sort_values(["invalid_count","ip"],ascending=[False,False])
    # print(logs)
    return logs
        

    