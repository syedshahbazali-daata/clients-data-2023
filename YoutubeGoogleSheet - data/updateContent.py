from database import *


def update_content():
    while True:
        try:
            df = pd.read_csv('data.csv')
            # upload the csv file to google sheets

            df = df.drop_duplicates(subset=['Date', 'Time', 'Video Title'], keep='last')
            df = df.fillna('NA')

            sheet = client.open_by_url(sheet_url).worksheet("CONTENT")
            sheet.clear()
            column_names_upper = [str(x.upper()) for x in df.columns.values.tolist()]
            sheet.update([column_names_upper] + df.values.tolist())

            print("Updated Content Data")

            # make column bold with 10 size and other data nunito font but with 9 size
            sheet.format('A1:Z1', {'textFormat': {'bold': True, 'fontSize': 10}})

            break
        except:
            print("Error in updating content")
            time.sleep(10)
            continue
