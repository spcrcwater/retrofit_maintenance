import requests
import time
import datetime
import pygsheets

current_time=int(time.time())

durationSec = 1*60*60

prev_time = current_time - durationSec

node_list = ['PH02-70', 'PH03-70', 'PH04-70', 'PH04-71', 'PR00-70', 'PL00-70', 'PL00-71', 'BB04-70', 'BB04-71', 
             'KB04-70', 'KB04-71', 'KB04-72', 'KB04-73', 'VN04-70', 'VN04-71']
node_ = ['Nodes', 'PH02-70', 'PH03-70', 'PH04-70', 'PH04-71', 'PR00-70', 'PL00-70', 'PL00-71', 'BB04-70', 'BB04-71', 
             'KB04-70', 'KB04-71', 'KB04-72', 'KB04-73', 'VN04-70', 'VN04-71']

url="https://onem2m.iiit.ac.in:443/~/in-cse"

def sheet_append(date_time, node_, reading, status):

    # path = 'E:\\IIIT-H\\Retrofit Maintenance Dashboard\\service_file.json'
    path = '/service_file.json'
    gc = pygsheets.authorize(service_account_file=path)
    # Open spreadsheet and then worksheet
    # sh = gc.open('Retrofit_Node_Status')
    # sh.open_by_link('https://docs.google.com/spreadsheets/d/1_vNFNYNTGUyq5FGJLndEUEmyjmtS6rJmt_Xx1JfKSM0/edit?usp=sharing')
    sh = gc.open_by_key('1_vNFNYNTGUyq5FGJLndEUEmyjmtS6rJmt_Xx1JfKSM0')
    wks = sh[0]

    # update the sheet with array
    # wks.update_col(1, df['Node'].tolist())
    # wks.update_col(2, df['Reading'].tolist())
    # wks.update_col(3, df['Status'].tolist())
    wks.update_col(1, date_time)
    wks.update_col(2, node_)
    wks.update_col(3, reading)
    wks.update_col(4, status)

def main():
    # while(True):
    status = []
    reading = []
    date_time = []
    date_time.append("Timestamp")
    reading.append("Last Reading")
    status.append("Status")
    for i in range(0,len(node_list)):
        res=requests.get(url='http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WM/WM-WF/WM-WF-'+str(node_list[i])+'/Data/la',
                        headers={'X-M2M-Origin':'guest:guest','Accept':'application/json'})
        try:
          print(res)
        except:
          print("No data")
          continue
        timestamp=(res.json()['m2m:cin']['con'].replace(']','').replace('[','').split(',')[0])
        data_time = int(timestamp)
        last_datetime = datetime.datetime.fromtimestamp(data_time)
        date_time.append(str(last_datetime))
        print(last_datetime)
        result=(res.json()['m2m:cin']['con'].replace(']','').replace('[','').split(',')[2])
        node_1=(res.json()['m2m:cin']['lbl'][1])
        ree=float(result)
        print(ree)
        reading.append(ree)

        m=f'{node_1} is working'
        for i in result:
            if ree==0.00 or data_time<prev_time:
                m=(node_1+" "+"is Not Working ")
            else:
                m=(node_1+" "+"is Working ")
        status.append(m[17:])
        print(m)
    # print("start appending")
    # print(date_time)
    sheet_append(date_time, node_, reading, status)
    # print("done appending")
    # time.sleep(durationSec)


if __name__=="__main__":
    main()
