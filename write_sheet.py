import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('json/servicecred.json', scope)
client = gspread.authorize(creds)
title = "cs skins"
spreadsheet = client.open(title)
worksheet = spreadsheet.get_worksheet(0)


def fix_data(given_data):
    givenItemData = given_data[0]
    giveSalesData = given_data[1]
    newData = []

    for item in givenItemData:
        for sale in giveSalesData:
            if item["market_hash_name"] == sale["market_hash_name"]:
                tempDict = {
                    "market_hash_name": item["market_hash_name"],
                    "min_price": item["min_price"],
                    "median_price": item["median_price"],
                    "max_price": item["max_price"],
                    "quantity": item["quantity"],
                    "min": sale["last_24_hours"]["min"],
                    "max": sale["last_24_hours"]["max"],
                    "avg": sale["last_24_hours"]["avg"],
                    "median": sale["last_24_hours"]["median"],
                    "volume": sale["last_24_hours"]["volume"]
                }
                newData.append(tempDict)
    return newData


def find_purchases(given_data):
    total_purchases = 0

    for transaction in given_data["data"]:
        if transaction["type"] == "purchase" and transaction["status"] == "complete":
            for item in transaction["items"]:
                print(item)
                total_purchases += 1

    print(total_purchases)


def find_skin_data(skin, item_data, sales_data):
    foundItems = []
    foundSales = []

    if len(item_data) > 0:
        for i in item_data:
            for v in skin:
                if v == i["market_hash_name"]:
                    # newCSV = open("testCSV.csv", "w")
                    # newCSV.write(str(
                    # i["market_hash_name"] + "," + str(i["min_price"]) + "," + str(i["median_price"]) + "," + str(
                    # i["max_price"])) + str())
                    foundItems.append(i)
    if len(sales_data) > 0:
        for i in sales_data:
            for v in skin:
                if v == i["market_hash_name"]:
                    foundSales.append(i)

    return [foundItems, foundSales]


def write_skin(passed_data, start_column_index, start_row_index, use_live_data):
    cell_list = []
    beginning_column_index = start_column_index

    currTime = time.ctime(time.time())
    timeCell = gspread.cell.Cell(1, 1, "Time Updated: " + currTime)
    cell_list.append(timeCell)

    dataBoolCell = gspread.cell.Cell(1, 11, "Live Data?: " + str(use_live_data))
    cell_list.append(dataBoolCell)

    for item in passed_data:
        for attribute in item:
            newCell = gspread.cell.Cell(start_row_index, start_column_index, item[attribute])
            cell_list.append(newCell)
            start_column_index += 1
        start_row_index += 1
        start_column_index = beginning_column_index

    worksheet.update_cells(cell_list, value_input_option="user_Entered")
