from fastapi import FastAPI, Query
from pymongo import MongoClient
from urllib.parse import quote
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import resend
from pydantic import BaseModel



app = FastAPI()

# CORS setup (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# resend.api_key = "re_ftfFRKSw_9vG9apweW71WYWjPPZMje4dJ"

resend.api_key = "re_E61uXPTX_5Zi2UeD4YFoqcXDVgpVjxoWd"
class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str
    image: str
    name: str


# MongoDB connection
public_key = "ErnestGaisie"
private_key = "ErnestGaisie"
encoded_private_key = quote(private_key)

MONGO_URI = (
    f"mongodb+srv://{public_key}:{encoded_private_key}"
    "@meenai0.vn5dz.mongodb.net/?retryWrites=true&w=majority&tls=true"
)

client = MongoClient(MONGO_URI)
db = client["furniture_store"]
collection = db["furniture_collection"]

@app.get("/")
def root():
    return {"message": "Furniture API is live!"}

@app.get("/furniture")
def get_filtered_furniture(
    brand: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    limit: int = Query(10, gt=0, le=100),  # default 10, max 100
    skip: int = Query(0, ge=0)             # default 0, can't be negative
):
    query = {}

    if brand:
        query["brand"] = brand

    if category:
        query["category"] = category

    try:
        cursor = collection.find(query, {"_id": 0}).skip(skip).limit(limit)
        furniture = list(cursor)
        return {
            "results": furniture,
            "count": len(furniture),
            "limit": limit,
            "skip": skip
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/email")
def send_email(payload: EmailRequest):
    try:
        params: resend.Emails.SendParams = {
        "from": "miniture@resend.dev",
        "to": ["kwaku@meenaai.com"],
        "subject": payload.subject,
        "html": f"""<html>
                    <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Furniture Sale</title>
                    </head>
                    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f9f9f9;">
                    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                        <!-- Header -->
                        <tr>
                        <td style="padding: 24px 32px; background-color: #fffbeb;">
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                                <td>
                                <p style="margin: 0; font-size: 24px; font-weight: 700; color: #92400e;">MINITURE</p>
                                </td>
                                <td align="right">
                                <p style="margin: 0; font-size: 14px; color: #b45309;">Quality Furniture</p>
                                </td>
                            </tr>
                            </table>
                        </td>
                        </tr>

                        <!-- Main Content -->
                        <tr>
                        <td style="padding: 24px 32px; background-color: #ffffff;">
                            <!-- Title -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 32px;">
                            <tr>
                                <td align="center">
                                <h1 style="margin: 0 0 8px 0; font-size: 30px; font-weight: 700; color: #1e293b;">Summer Sale Event</h1>
                                <p style="margin: 0; color: #64748b;">Limited time offer on our premium collection</p>
                                </td>
                            </tr>
                            </table>

                            <!-- Product Image -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 40px;">
                            <tr>
                                <td>
                                <div style="position: relative;">
                                    <img src="{payload.image}" alt="Oslo Sectional Sofa" style="width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />
                                    <div style="position: absolute; top: 16px; right: 16px; background-color: #d97706; color: white; padding: 8px 16px; font-weight: 700; border-radius: 9999px; font-size: 18px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                                    40% OFF
                                    </div>
                                </div>
                                </td>
                            </tr>
                            </table>

                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 40px;">
                            <tr>
                                <td align="center" style="padding-bottom: 24px;">
                                <h2 style="margin: 0; font-size: 24px; font-weight: 700; color: #1e293b;">Elevate Your Living Space</h2>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding-bottom: 40px;">
                                <!-- Two Column Layout for Desktop -->
                                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                    <tr>
                                    <!-- Left Column - Image -->
                                    <td style="width: 48%; padding-right: 2%; vertical-align: top;">
                                        <img src="https://meena-storage.s3.us-east-1.amazonaws.com/temp-output/Modular+Bondi.jpg" alt="Modern sofa" style="width: 100%; height: auto; border-radius: 8px; display: block;" />
                                    </td>
                                    <!-- Right Column - Content -->
                                    <td style="width: 48%; padding-left: 2%; vertical-align: top;">
                                        <h3 style="margin: 0 0 8px 0; font-size: 20px; font-weight: 700; color: #1e293b;">Modular Bondi Latte 2-Seater Sofa in Rose Quartz</h3>
                                        <p style="margin: 0 0 16px 0; color: #64748b; line-height: 1.5;">
                                        Transform your living room with our bestselling Modular Bondi Latte 2-Seater Sofa in Rose Quartz. Crafted with premium materials and designed for both comfort and style.
                                        </p>
                                        <table cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 16px;">
                                        <tr>
                                            <td style="padding-right: 12px;">
                                            <span style="font-size: 20px; font-weight: 700; color: #1e293b;">$999</span>
                                            </td>
                                            <td style="padding-right: 12px;">
                                            <span style="font-size: 18px; text-decoration: line-through; color: #94a3b8;">$1,273</span>
                                            </td>
                                            <td>
                                            <span style="display: inline-block; background-color: #ffedd5; color: #c2410c; padding: 4px 8px; border-radius: 4px; font-size: 14px; font-weight: 500;">40% OFF</span>
                                            </td>
                                        </tr>
                                        </table>
                                        <a href="https://your-website.com/shop?utm_source=email&utm_medium=summer_sale&utm_campaign=furniture" style="display: block; background-color: #0f766e; color: white; padding: 12px 16px; text-align: center; text-decoration: none; border-radius: 4px; font-weight: 500;">Shop Now</a>
                                    </td>
                                    </tr>
                                </table>
                                </td>
                            </tr>
                            </table>

                            <!-- CTA Box -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 32px; background-color: #fffbeb; border: 1px solid #fef3c7; border-radius: 8px;">
                            <tr>
                                <td style="padding: 24px;" align="center">
                                <h3 style="margin: 0 0 12px 0; font-size: 20px; font-weight: 700; color: #1e293b;">Sale Ends in 5 Days!</h3>
                                <p style="margin: 0; color: #64748b;">
                                    Don't miss out on these incredible savings. Use code <span style="font-weight: 700;">SUMMER40</span> at checkout.
                                </p>
                                </td>
                            </tr>
                            </table>
                        </td>
                        </tr>

                        <!-- Shipping Info -->
                        <tr>
                        <td style="padding: 16px 32px; border-top: 1px solid #e2e8f0;">
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                                <td align="center">
                                <table cellpadding="0" cellspacing="0" border="0">
                                    <tr>
                                    <td style="padding: 0 16px;">
                                        <p style="margin: 0 0 4px 0; font-weight: 500; color: #1e293b;">Free Shipping</p>
                                        <p style="margin: 0; font-size: 14px; color: #64748b;">On orders over $999</p>
                                    </td>
                                    <td style="padding: 0 16px;">
                                        <p style="margin: 0 0 4px 0; font-weight: 500; color: #1e293b;">Easy Returns</p>
                                        <p style="margin: 0; font-size: 14px; color: #64748b;">30-day money back</p>
                                    </td>
                                    </tr>
                                </table>
                                </td>
                            </tr>
                            </table>
                        </td>
                        </tr>

                        <!-- Footer -->
                        <tr>
                        <td style="padding: 24px 32px; background-color: #92400e; color: white;" align="center">
                            <p style="margin: 0 0 16px 0;">© 2024 Modern Living Furniture. All rights reserved.</p>
                            
                            <table cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 16px;">
                            <tr>
                                <td style="padding: 0 8px;">
                                <a href="#" style="color: white; text-decoration: none;">Shop</a>
                                </td>
                                <td style="padding: 0 8px;">
                                <a href="#" style="color: white; text-decoration: none;">About</a>
                                </td>
                                <td style="padding: 0 8px;">
                                <a href="#" style="color: white; text-decoration: none;">Contact</a>
                                </td>
                                <td style="padding: 0 8px;">
                                <a href="#" style="color: white; text-decoration: none;">Unsubscribe</a>
                                </td>
                            </tr>
                            </table>
                            
                            <p style="margin: 0; font-size: 14px; color: #fef3c7;">123 Furniture Lane, Design District, CA 90210</p>
                        </td>
                        </tr>
                    </table>
                    </body>
                    </html>""",
        }
        email: resend.Email = resend.Emails.send(params)
        return email
    except Exception as e:
        return {"status": "error", "message": str(e)}
