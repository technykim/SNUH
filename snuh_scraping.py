#import unicodedata
import csv
import requests
#import pandas as pd
#import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys
import io

# VSCODE OUTPUT창에 한글이 깨져 나와서 추가함
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

page = 1  # 게시판 형태 페이지
results = []  # 크롤링정보를 담을 리스트
headers = ['페이지', 'NO']  # 해당페이지, 검사항목수에 대항하는 해더
count = 1  # 항목count
target_url1 = "http://www.snuhlab.org/checkup/check_list.aspx?page="
target_url2 = "&ins_class_code=L30&searchfield=TOTAL&searchword="

for page in range(1, 10, 1):
    print("Start Get ViewPage data from Page Number " + str(page))
    res = requests.get(target_url1+str(page)+target_url2)
    soup = BeautifulSoup(res.content, "html.parser")
    div = soup.find("div", class_="board_sec jw_bh")
    # 해당 요소 내에는 ul형태로 되어 있고 ul 내에 데이터가 있으므로 ul의 자식 요소인 li를 for loop함.
    lists = div.ul.find_all("thead")

    for thead in lists:
        data = {}
        data['페이지'] = page
        data['NO'] = count
        # 해당 li에는 또 다시 child를 가지는데 첫 번째는 헤더, 두 번째는 원하는 데이터임
        trs = thead.find_all("tr")
        for tr in trs:
            # 해당하는 헤더가 만약 기존의 헤더 리스트에 없는 헤더면 새로 추가함.(엑셀 임포트 할 때 사옹)
            header = tr.th.contents[0]
            if header not in headers:
                headers.append(header)
            # 없는 데이터면 공백 문자 사용하도록 분기
            content = ""
            if len(tr.td) > 0:
                content = tr.td.contents[0]
    #        print("header="+header+" & content="+content)
            # header를 Key로 해서 데이터를 저장함.(나중에 불러오기 편함)
            data[header] = content
        count = count+1
        results.append(data)

print("Finished to Get ViewPage data from Page Number " + str(page))

# 가져온 데이터들을 CSV 형태로 저장한다
f = open('output.csv', 'w+t', newline='')
wr = csv.writer(f)
# 첫 번째 행은 헤더로 만든다.
wr.writerow(headers)

# 데이터를 전부 csv 형태로 해서 넣는다.
for datas in results:
    row = []
    selected_values = [datas[a] for a in headers]

    for value in selected_values:
        if len(str(value)) > 0:
            row.append(value)
        else:
            row.append("")
    wr.writerow(row)
f.close()
