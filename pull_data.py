import json
import requests
import base64
import brotli

itemData = []
salesData = []
transactionData = []


def get_skinport_secrets():
    with open("json/skinport_secrets.json", "rb") as file:
        data = json.load(file)

    formatted_secrets = data["client_id"]+":"+data["client_secret"]
    encoded_secrets = str(base64.b64encode(formatted_secrets.encode("utf-8")), "utf-8")
    authorization = f"Basic {encoded_secrets}"
    return


def pull_items(use_live_data):
    global itemData

    if use_live_data:
        print("Fetching skinport item data")

        params = {
            "app_id": 730,
            "currency": "USD",
        }
        header = {
            "Accept-Encoding": "br",
        }

        r = requests.get("https://api.skinport.com/v1/items", params=params, headers=header)

        if r.status_code == 200:
            itemData = r.json()
            saveData = json.dumps(itemData, indent=2)

            with open("json/items.json", "w") as outfile:
                outfile.write(saveData)
            return itemData
        else:
            print("Failed to load skinport API")


def pull_sales(use_live_data):
    global salesData

    if use_live_data:
        print("Fetching skinport sales data")

        params = {
            "app_id": 730,
            "currency": "USD",
        }
        header = {
            "Accept-Encoding": "br",
        }

        r = requests.get("https://api.skinport.com/v1/sales/history", params=params, headers=header)

        if r.status_code == 200:
            salesData = r.json()
            saveData = json.dumps(salesData, indent=2)

            with open("json/sales.json", "w") as outfile:
                outfile.write(saveData)
            return salesData
        else:
            print("Failed to load skinport API")


def pull_transaction_history(use_live_data):
    global transactionData

    if use_live_data:
        print("Fetching skinport transaction data")

        r = requests.get("https://api.skinport.com/v1/account/transactions", headers={
            "authorization": get_skinport_secrets()
        }, params={
            "page": 1,
            "limit": 100,
            "order": "desc"
        })

        if r.status_code == 200:
            transactionData = r.json()
            transactionData = json.dumps(transactionData, indent=2)

            with open("json/transactions.json", "w") as outfile:
                outfile.write(transactionData)
            return transactionData
        else:
            print("Failed to load skinport API")
    else:
        print("Failed to load skinport API")




