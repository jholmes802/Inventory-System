import gspread
import dataio
import string
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np 

def g_backup():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Dev Backup")
    sheet_inst = sheet.get_worksheet(0)
    fields, results = dataio.items.get_all()
    update = []
    update.append(fields)
    for x in results:
        update.append(x)
    update = np.array(update)
    cols_len = string.ascii_uppercase[len(fields)]
    rows_len = len(results)
    sheet_inst.update("A2:" + cols_len + str(rows_len+2), update.tolist())

if __name__ == "__main__":
    g_backup()




