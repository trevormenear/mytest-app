from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os, boto3
from boto3.dynamodb.conditions import Key

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
TABLE_NAME = os.environ["DDB_TABLE_NAME"]

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)

app = FastAPI(title="Quotes API")

# Allow your CloudFront site to call this API.
# If you don't have a custom domain yet, this still allows calls from your CloudFront URL.
allowed_origins = [
    # e.g. https://quotes.yourdomain.com (add later when you have it)
    "https://d2gu23ntxcq9oe.cloudfront.net",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"ok": True, "msg": "App Runner is alive"}

@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/api/health")
async def api_health():
    return {"ok": True}

# ---------- Quotes ----------
class CreateQuoteBody(BaseModel):
    client_id: str = Field(..., description="Your client UUID or slug")
    quote_id: str = Field(..., description="Your internal quote id")
    dwelling_coverage: int
    price: float
    name: str
    address: str

@app.post("/api/quote")
def create_quote(body: CreateQuoteBody):
    item = {
        "pk": f"CLIENT#{body.client_id}",
        "sk": f"QUOTE#{body.quote_id}",
        "dwelling_coverage": int(body.dwelling_coverage),
        "price": float(body.price),
        "client_name": body.name,
        "client_address": body.address,
    }
    try:
        table.put_item(Item=item)
        return {"ok": True, "stored": item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/quotes/{client_id}")
def list_quotes(client_id: str):
    try:
        resp = table.query(KeyConditionExpression=Key("pk").eq(f"CLIENT#{client_id}"))
        return {"ok": True, "items": resp.get("Items", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
