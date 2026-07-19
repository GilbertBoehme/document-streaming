from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import json 

from pydantic import BaseModel

from datetime import datetime
from kafka import KafkaProducer

# create class (schema) for the JSON
class InvoiceItem(BaseModel):
    InvoiceNo: int
    StockCode: str
    Description: str
    Quantity: int
    InvoiceDate: str
    UnitPrice: float
    CustomerID: int
    Country: str

app = FastAPI()

# base url
@app.get("/")
async def root():
    return {"message": "This is the Kafka Invoice API."}

# add new invoice
@app.post("/invoiceitem")
async def post_invoice_item(item: InvoiceItem):
    print("Message received.")
    try:
        # Evaluate the timestamp and parse it to datetime object you can work with
        date = datetime.strptime(item.InvoiceDate, "%d/%m/%Y %H:%M")

        print('Found a timestamp: ', date)

        # Replace strange date with new datetime
        # Use strftime to parse the string in the right format (replace / with - and add seconds)
        item.InvoiceDate = date.strftime("%d-%m-%Y %H:%M:%S")
        print("New item date:", item.InvoiceDate)

        # parse item back to json
        json_of_item = jsonable_encoder(item)

        # dump json out as string
        json_as_string = json.dumps(json_of_item)

        # send to kafka
        producer = KafkaProducer(bootstrap_servers='kafka:9092',acks=1)
        # Write the string as bytes
        producer.send('ingestion-topic', bytes(json_as_string, 'utf-8'))
        producer.flush() 

        # Encode the created customer item if successful into a JSON and return it to the client with 201
        return JSONResponse(content=json_of_item, status_code=201)
    except ValueError:
        return JSONResponse(content=jsonable_encoder(item), status_code=400)