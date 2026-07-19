import os
from urllib.parse import quote_plus

import streamlit as st
from pandas import DataFrame

import pymongo


#data = pd.read_csv("data.csv")
mongo_username = os.environ["MONGO_USERNAME"]
mongo_password = os.environ["MONGO_PASSWORD"]
mongo_host = os.getenv("MONGO_HOST", "localhost")
mongo_database = os.getenv("MONGO_DATABASE", "docstreaming")
mongo_uri = (
    f"mongodb://{quote_plus(mongo_username)}:{quote_plus(mongo_password)}"
    f"@{mongo_host}:27017/{mongo_database}?authSource=admin"
)

myclient = pymongo.MongoClient(mongo_uri)
mydb = myclient[mongo_database]
mycol = mydb["invoices"]


# Below the fist chart add a input field for the invoice number
cust_id = st.sidebar.text_input("CustomerID:")
#st.text(inv_no)  # Use this to print out the content of the input field

# if enter has been used on the input field
if cust_id:

    myquery = {"CustomerID": cust_id}
    # only includes or excludes
    mydoc = mycol.find( myquery , { "_id": 0, "StockCode": 0, "Description": 0, "Quantity": 0, "Country": 0, "UnitPrice": 0})

    # create dataframe from resulting documents to use drop_duplicates
    df = DataFrame(mydoc)

    # drop duplicates, but keep the first one
    df.drop_duplicates(subset ="InvoiceNo", keep = 'first', inplace = True)

    # Add the table with a headline
    st.header("Output Customer Invoices")
    table2 = st.dataframe(data=df)


# Below the fist chart add a input field for the invoice number
inv_no = st.sidebar.text_input("InvoiceNo:")
#st.text(inv_no)  # Use this to print out the content of the input field

# if enter has been used on the input field
if inv_no:

    myquery = {"InvoiceNo": inv_no}
    mydoc = mycol.find( myquery, { "_id": 0, "InvoiceDate": 0, "Country": 0, "CustomerID": 0 })

    # create the dataframe
    df = DataFrame(mydoc)

    # reindex it so that the columns are order lexicographically
    reindexed = df.reindex(sorted(df.columns), axis=1)

    # Add the table with a headline
    st.header("Output by Invoice ID")
    table2 = st.dataframe(data=reindexed)
