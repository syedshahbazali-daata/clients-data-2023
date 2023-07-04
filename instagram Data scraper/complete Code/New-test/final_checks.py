import requests
import time
from database_connection import *

########################################################################################################################
#      DO NOT CHANGE ANYTHING BELOW THIS LINE
########################################################################################################################
import gspread
from oauth2client.service_account import ServiceAccountCredentials

sheet_url = 'https://docs.google.com/spreadsheets/d/1Lid5x1Qfk_ME5h-YHKE70nkJmlsbB2MbC_lHNlzZTu4/edit?usp=sharing'

########################################################################################################################
#      DO NOT CHANGE ANYTHING BELOW THIS LINE
########################################################################################################################
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds_sheet = ServiceAccountCredentials.from_json_keyfile_name(
    r"connection_api.json", scope)
client = gspread.authorize(creds_sheet)
sheet = client.open_by_url(sheet_url).sheet1


def get_coordinates(address) -> dict or bool:
    """
    :param address: Address of the location
    :return: Coordinates of the location
    """
    try:
        YOUR_KEY = "AIzaSyD51L_tG0jpLr2mHAZQ73TnQED_e8xzVYo"
        new_address = f'{address}' + ", Australia"
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={new_address}&key={YOUR_KEY}"
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        response = response.json()["results"][0]["geometry"]["location"]

        return response
    except:
        return False


def get_url(address: str) -> list:
    try:
        res = requests.get(
            f"https://www.planning.vic.gov.au/property-dashboard/street_suggestions.json?extraQuery=amendment-id&profile=amendment-id&partial_query={address}")
        result = res.json()[0]
        get_suggested_address = result['text']
        get_suggested_key = result['key']
        url = f"https://www.planning.vic.gov.au/schemes-and-amendments/planning-report?property={get_suggested_address},{get_suggested_key}"
        print(url)

        query_key = f'https://www.planning.vic.gov.au/property-dashboard/get_street_key.json?query={get_suggested_key}'
        res = requests.get(query_key)
        pfi = res.json()['pfi']

        page_url = f'https://www.planning.vic.gov.au/property-dashboard/get_datareporter.json?query={pfi}&inputSearchType=property'
        print(page_url)
        res = requests.get(page_url)
        data = res.json()
    except:
        pass
    try:
        zone_code = str(data[0]['value']['features'][0]['attributes']['ZONE_CODE'])

    except:
        zone_code = ""

    try:
        parent_zone_code = str(data[0]['value']['features'][0]['attributes']['CODE_PARENT'])

    except:
        parent_zone_code = ""

    try:
        overlays = []
        overlay_code = data[1]['value']['features']
        for overlay in overlay_code:
            overlays.append(overlay['attributes']['ZONE_CODE'])
            overlays.append(overlay['attributes']['CODE_PARENT'])
        overlays = list(set(overlays))

        overlay_code = ", ".join(overlays)

    except:
        overlay_code = ""

    return [parent_zone_code, zone_code, overlay_code]


cursor.execute("SELECT * FROM ScrapersData")
data = list(cursor.fetchall())

for index, row in enumerate(data):
    print(index, row)
    if row[3 + 1] == "" and row[4 + 1] == "":
        print(row[1])

        coordinates = get_coordinates(row[2])
        print(coordinates)

        if not coordinates:
            continue

        update_coordinates(lat_x=coordinates['lat'], lon_y=coordinates['lng'], row_id=row[0])
        print("Updated Coordinates")

    if row[7 + 1] == '' and row[8 + 1] == '':
        data_result = get_url(row[2])
        print(data_result)

        update_zones((data_result[0], data_result[1], data_result[2]), row[0])
        print("Updated Zones")

query = "SELECT * FROM ScrapersData"
cursor.execute(query)
result = cursor.fetchall()
print(result)
records = []
for single_row in result:

    row = list(single_row)[1:]
    # 5 element of the row will be .title(): 'Council'
    row[5] = row[5].title()
    if str(row[6]).strip() == '':
        row[6] = 'EMPTY'
    if str(row[-1]).strip() == '':
        row[-1] = 'EMPTY'

    if str(row[4]).strip() == '' or str(row[3]).strip() == '':
        continue

    records.append(row)

final_records = []
for record in records:
    if len(str(record[1]).strip()) < 5 or len(str(record[2]).strip()) < 5:
        continue

    record[2] = str(record[2]).replace('"', "")
    record[2] = str(record[2]).replace("'", "")
    record[2] = str(record[2]).replace("\n", " ")
    record[2] = str(record[2]).replace("\r", " ")
    record[2] = str(record[2]).replace("\t", " ")

    final_records.append(record)


def delete_row():
    print("Deleting Rows")
    try:
        sheet.delete_rows(2, sheet.row_count)
    except:
        pass


def add_row():
    print("Adding Rows")
    while True:
        try:
            sheet.add_rows(len(final_records))
            break
        except:
            pass


delete_row()
time.sleep(5)
add_row()
time.sleep(5)

while True:
    try:
        # delete sheets after 2nd row
        # Application Number	Primary Property Address	Description	Lat	Lon	Council	Project Type	Parent Zone	Main Zone	Overlays

        sheet.insert_rows(final_records, 2)

        break
    except Exception as e:
        print(e)
        time.sleep(5)
