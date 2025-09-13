'''
3657. Find Loyal Customers
Solved
Medium
premium lock icon
Companies
SQL Schema
Pandas Schema
Table: customer_transactions

+------------------+---------+
| Column Name      | Type    | 
+------------------+---------+
| transaction_id   | int     |
| customer_id      | int     |
| transaction_date | date    |
| amount           | decimal |
| transaction_type | varchar |
+------------------+---------+
transaction_id is the unique identifier for this table.
transaction_type can be either 'purchase' or 'refund'.
Write a solution to find loyal customers. A customer is considered loyal if they meet ALL the following criteria:

Made at least 3 purchase transactions.
Have been active for at least 30 days.
Their refund rate is less than 20% .
Return the result table ordered by customer_id in ascending order.

The result format is in the following example.

 

Example:

Input:

customer_transactions table:

+----------------+-------------+------------------+--------+------------------+
| transaction_id | customer_id | transaction_date | amount | transaction_type |
+----------------+-------------+------------------+--------+------------------+
| 1              | 101         | 2024-01-05       | 150.00 | purchase         |
| 2              | 101         | 2024-01-15       | 200.00 | purchase         |
| 3              | 101         | 2024-02-10       | 180.00 | purchase         |
| 4              | 101         | 2024-02-20       | 250.00 | purchase         |
| 5              | 102         | 2024-01-10       | 100.00 | purchase         |
| 6              | 102         | 2024-01-12       | 120.00 | purchase         |
| 7              | 102         | 2024-01-15       | 80.00  | refund           |
| 8              | 102         | 2024-01-18       | 90.00  | refund           |
| 9              | 102         | 2024-02-15       | 130.00 | purchase         |
| 10             | 103         | 2024-01-01       | 500.00 | purchase         |
| 11             | 103         | 2024-01-02       | 450.00 | purchase         |
| 12             | 103         | 2024-01-03       | 400.00 | purchase         |
| 13             | 104         | 2024-01-01       | 200.00 | purchase         |
| 14             | 104         | 2024-02-01       | 250.00 | purchase         |
| 15             | 104         | 2024-02-15       | 300.00 | purchase         |
| 16             | 104         | 2024-03-01       | 350.00 | purchase         |
| 17             | 104         | 2024-03-10       | 280.00 | purchase         |
| 18             | 104         | 2024-03-15       | 100.00 | refund           |
+----------------+-------------+------------------+--------+------------------+
Output:

+-------------+
| customer_id |
+-------------+
| 101         |
| 104         |
+-------------+
Explanation:

Customer 101:
Purchase transactions: 4 (IDs: 1, 2, 3, 4) 
Refund transactions: 0
Refund rate: 0/4 = 0% (less than 20%) 
Active period: Jan 5 to Feb 20 = 46 days (at least 30 days) 
Qualifies as loyal 
Customer 102:
Purchase transactions: 3 (IDs: 5, 6, 9) 
Refund transactions: 2 (IDs: 7, 8)
Refund rate: 2/5 = 40% (exceeds 20%) 
Not loyal 
Customer 103:
Purchase transactions: 3 (IDs: 10, 11, 12) 
Refund transactions: 0
Refund rate: 0/3 = 0% (less than 20%) 
Active period: Jan 1 to Jan 3 = 2 days (less than 30 days) 
Not loyal 
Customer 104:
Purchase transactions: 5 (IDs: 13, 14, 15, 16, 17) 
Refund transactions: 1 (ID: 18)
Refund rate: 1/6 = 16.67% (less than 20%) 
Active period: Jan 1 to Mar 15 = 73 days (at least 30 days) 
Qualifies as loyal 
The result table is ordered by customer_id in ascending order.
'''


import pandas as pd

def find_loyal_customers(customer_transactions: pd.DataFrame) -> pd.DataFrame:
    df_cnt_total = customer_transactions.groupby("customer_id").size().reset_index(name="leng")
    df_date = customer_transactions.groupby("customer_id").agg({"transaction_date":["min","max"]})
    df_date.columns=["min","max"]
    df_date=df_date.reset_index()
    df_date["min"]=pd.to_datetime(df_date["min"])
    df_date["max"]=pd.to_datetime(df_date["max"])
    df_date["diff"]=df_date["max"]-df_date["min"]
    # print(df_cnt_total)
    # print(df_date)
    customer_transactions = pd.merge(customer_transactions,df_cnt_total,on="customer_id")
    customer_transactions = pd.merge(customer_transactions,df_date,on="customer_id").drop(["min","max"],axis=1)
    customer_transactions = customer_transactions[customer_transactions["diff"]>="30 days"]
    # df_purchase = customer_transactions[customer_transactions["transaction_type"]=="purchase"].groupby("customer_id").size().reset_index(name="leng_purchase")
    df_purchase = customer_transactions.groupby("customer_id").size().reset_index(name="leng_purchase")
    # print(df_purchase)
    # print(customer_transactions)
    df_refund = customer_transactions.groupby("customer_id").agg(refund_count=("transaction_type",lambda x:(x=="refund").sum())).reset_index()
    # print(df_refund)
    df_purchase = pd.merge(df_purchase,df_refund,on="customer_id").reset_index()
    # print(df_purchase)
    df_purchase["refund_rate"] = round(df_purchase["refund_count"]*100/df_purchase["leng_purchase"],2)
    # print(df_purchase)
    customer_transactions = pd.merge(customer_transactions,df_purchase,on="customer_id").drop(["refund_count"],axis=1)
    df_purchase_3 = customer_transactions.groupby("customer_id").agg(purchase_3=("transaction_type",(lambda x:(x=="purchase").sum()))).reset_index()
    # print(df_purchase_3)
    df_purchase_3 = df_purchase_3[df_purchase_3["purchase_3"]>=3]
    customer_transactions = customer_transactions[customer_transactions["refund_rate"]<20.00]
    customer_transactions = pd.merge(customer_transactions,df_purchase_3,on="customer_id")
    # print(customer_transactions,customer_transactions.columns)
    customer_transactions = pd.DataFrame(customer_transactions["customer_id"].unique(),columns=["customer_id"])
    # print(customer_transactions)
    return customer_transactions



    