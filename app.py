from fastapi import FastAPI
import os, boto3
from boto3.dynamodb.conditions import Key

app = FastAPI()

@app.get("/")
def root():
    return {"ok": True, "msg": "App Runner is alive"}

@app.post("/quote")
def create_quote(client_id: str, quote_id: str, dwelling_coverage: int, price: float, name: str, address: str):
    table = boto3.resource("dynamodb", region_name=os.environ.get("AWS_REGION", "us-east-1")) \
                 .Table(os.environ["DDB_TABLE_NAME"])
    item = {
        "pk": f"CLIENT#{client_id}",
        "sk": f"QUOTE#{quote_id}",
        "dwelling_coverage": dwelling_coverage,
        "price": float(price),
        "client_name": name,
        "client_address": address
    }
    table.put_item(Item=item)
    return {"ok": True, "stored": item}

@app.get("/quotes/{client_id}")
def list_quotes(client_id: str):
    table = boto3.resource("dynamodb", region_name=os.environ.get("AWS_REGION", "us-east-1")) \
                 .Table(os.environ["DDB_TABLE_NAME"])
    resp = table.query(KeyConditionExpression=Key("pk").eq(f"CLIENT#{client_id}"))
    return {"ok": True, "items": resp.get("Items", [])}
