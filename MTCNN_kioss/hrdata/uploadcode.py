import time
from csv import reader, DictWriter
from json import dumps, loads, dump

from requests import ConnectionError, HTTPError
from requests import get, post
from datetime import datetime
import requests

url = 'https://api-vietthan-hr.systemkul.com/v1/'

def call_json():
    url = 'https://api-vietthang-hr.systemkul.com/v1/'
    r = get(url + 'NhanVien?page_size=50&page_number=' + str(1), headers={'Content-Type': 'application/json',})
    data1 = loads(r.text)['data']
    for i in range(2, 16):
        r = get(url + 'NhanVien?page_size=50&page_number=' + str(i), headers={'Content-Type': 'application/json',})
        for j in range(0, 50):
            try:
                nhavienx = loads(r.text)['data'][j]
                data1.append(nhavienx)
            except:
                break
    with open('data/data5.json', 'w') as f:
        dump(data1, f)  

def post_data():
    with open('data/recognization.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        # try:
        for row in csv_reader:
            name_student_recognite = row[0]
            date = row[1]
            idptChamCong = 2
            tempt_student = row[2]
            uuid_device = "a22049f1-0682-3c90-af23-dd497e2a063d" 
            data_request = {'maNhanVien': name_student_recognite, 'ngayGioChamCong': date, 'idPhuongThucChamCong': idptChamCong, "nhietDo": tempt_student, "maThietBi": uuid_device}
            print(data_request)
            try:
                r = post(url + "ChamCong", timeout=10, data=dumps(data_request), headers={'Content-Type': 'application/json', })
                print(r.status_code)
                try:
                    r.raise_for_status()
                except requests.exceptions.HTTPError as errh:
                    print ("Http Error:",errh.response.text)
                except requests.exceptions.ConnectionError as errc:
                    print ("Error Connecting:",errc)
                except requests.exceptions.Timeout as errt:
                    print ("Timeout Error:",errt)
                except requests.exceptions.RequestException as err:
                    print ("OOps: Something Else",err)

            except ConnectionError:
                print("No internet connection available.")
                return
        with open ("data/recognization.csv", mode = "w") as re_csv_file:
            fieldnames = ['ID', 'Date', 'Temperature']
            writer = DictWriter(re_csv_file, fieldnames=fieldnames)
        # except:
        #     print("hello")

if __name__ == "__main__":
    timeconut = 21600
    start = datetime.now()
    try:
        call_json()
        time.sleep(10)
    except:
        print("dont't having internet")
    while True:
        post_data()
        time.sleep(5)
        try:    
            now = datetime.now()
            if (now - start).total_seconds() > timeconut:
                call_json()
                start = now
        except:
            print("hello")
            pass
