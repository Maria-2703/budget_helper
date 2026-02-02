from flask import Flask, render_template, request
from dotenv import load_dotenv
import cohere
import json
import pandas as pd
import os

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(api_key=api_key)
    
def classify(data):
    transactions = data.to_dict(orient="records")
    prompt = f"""
    You are a financial transaction classification assistant.
    Your task is to analyze the bank statement uploaded by the user and classify EACH transaction into ONE of the following categories:

    Categories:
    - Shopping
    - Technology
    - Bills (utilities, phone, internet, insurance, credit cards, etc.)
    - Rent
    - Groceries
    - Eating Out (restaurants, cafes, fast food, delivery apps)
    - Entertainment (concerts, shows, movies, bowling, amusement parks, events, tickets, games)
    - Transportation (bus, train, metro, taxi, rideshare, gas, parking, tolls)
    - Trips (flights, hotels, Airbnb, travel agencies, vacation expenses)
    - Subscriptions (Netflix, Spotify, Apple, Google, SaaS, recurring memberships)
    - Pets (pet food, vet, grooming, pet supplies)
    - Income (salary, reimbursements, deposits)
    - Others (anything that does not clearly fit the above)

    Rules:
    1. Assign exactly ONE category per transaction.
    2. Use the merchant name, description, and context to infer the best category.
    3. If a transaction could belong to multiple categories, choose the MOST specific and relevant one.
    4. If the category is unclear or unknown, classify it as "Others".
    5. Do NOT invent transactions or amounts.

    Input format:
    A list of transactions, each containing:
    - Date
    - Description / Merchant
    - Amount

    Output format:
    Return the results as a structured JSON array. Each item must include:
    - date
    - description
    - amount
    - category

    Now classify the following bank statement transactions:
    {json.dumps(transactions, indent=2)}
    
    IMPORTANT:
    - Your output must be a valid JSON array.
    - Do NOT include any explanations, notes, or extra text.
    - Do NOT add commas outside the array, comments, or Markdown formatting.
    - The JSON must start with [ and end with ].

    Example of the Output:
    {{
        "date": "2024-11-03",
        "description": "Netflix.com",
        "amount": -15.99,
        "category": "Subscriptions"
    }}
    ]
    Return your result exactly in the format shown above.
    """
    
    # send prompt to cohere
    response = co.chat(
        model="command-nightly",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.message.content[0].text
    return result

@app.route("/budgeting", methods=["GET","POST"])
def budgeting():
    if request.method == "POST":
        # if there isn't a file
        if "file" not in request.files:
            return {"error" : "No file uploaded"}

        # get file user uploads
        file = request.files["file"]
        data = pd.read_csv(file)

        # send data to ai
        classified = classify(data)
        print(classified)

        # json to df
        classified = json.loads(classified)
        data_result = pd.DataFrame(classified)

        return render_template("home.html", table=data_result.to_html(index=False))
    return render_template("home.html", table=None)

if __name__ == "__main__":
    app.run(debug = True, host = "localhost", port  = 5000)