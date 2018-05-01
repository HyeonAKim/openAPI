import urllib.parse
import urllib.request
import pandas as pd
import xml.etree.ElementTree as ET


#input service key
serviceKey = 'YZcQLTgDdOz202rWWtWRqavCqSSphiAMZEqmS8x%2BDSmI4K7WZcIOFJ%2ByGsUHpsjYwVMJcZiSsGgStcJxhxWbpA%3D%3D'

# create url of BaseInfoSearch
# BaseInfoSearch = 'http://apis.data.go.kr/B552015/NpsBplcInfoInqireService/getBassInfoSearch'
# queryParams = '?serviceKey=' + serviceKey +'&'+ urllib.parse.urlencode({ urllib.parse.quote_plus('wkpl_nm') : '위세아이텍', urllib.parse.quote_plus('numOfRows') : '30' })

#request BaseInfoSearch data
# request = urllib.request.Request(BaseInfoSearch + queryParams)
# request.get_method = lambda: 'GET'
# response_body = urllib.request.urlopen(request).read()

# write xml file
#basefile = open("C:\\Users\\HyunA\\Desktop\\basefile.xml","wb")
#basefile.write(response_body)
#basefile.close()

# read xml file
#basefile = open("C:\\Users\\HyunA\\Desktop\\basefile.xml","wb")
#basefile.write(response_body)
doc = ET.parse("C:\\Users\\HyunA\\Documents\\myproject\openAPI\\basefile.xml")
root = doc.getroot()

# extract xml text
baseDataCrtYm = []
baseSeq = []
for dataCrtYm in root.findall("./body/items/item/dataCrtYm") :
    baseDataCrtYm.append(dataCrtYm.text)

for seq in root.findall("./body/items/item/seq") :
    baseSeq.append(seq.text)

# create key list
keyList = []
for i in range(0,len(baseDataCrtYm)-1) :
    keyList.append([baseDataCrtYm[i],baseSeq[i]])

# create url of DetailInfoSearch
DetailInfo = 'http://apis.data.go.kr/B552015/NpsBplcInfoInqireService/getDetailInfoSearch'

# 데이터프레임만들기
dfcol = ['seq', 'jnngpCnt', 'crrmmNtcAmt']
df_detailInfo = pd.DataFrame(columns=dfcol)
i = '1'
for company_seq in baseSeq :

    queryParams = '?serviceKey=' + serviceKey + '&' + urllib.parse.urlencode({urllib.parse.quote_plus('seq'): company_seq })

    # request BaseInfoSearch data
    request = urllib.request.Request(DetailInfo + queryParams)
    request.get_method = lambda: 'GET'

    #xml 파일 파싱하기
    parseString = ET.parse( urllib.request.urlopen(request))

    #정보제대로 가져오는지 확인
    root = parseString.getroot()
    resultcode = root.find('header/resultCode')
    result_msg = '1st_code ' +resultcode.text
    num_seq = i+'.'+company_seq
    print(num_seq)
    print(result_msg)

    if resultcode.text == '99' :
        # 데이터 재요청
        request = urllib.request.Request(DetailInfo + queryParams)
        request.get_method = lambda: 'GET'
        parseString = ET.parse(urllib.request.urlopen(request))
        root = parseString.getroot()
        resultcode = root.find('header/resultCode')
        result_msg = '2nd_code ' + resultcode.text
        jnngpCnt = root.find('body/item/jnngpCnt')
        crrmmNtcAmt = root.find('body/item/crrmmNtcAmt')
        print(result_msg)
    else :
        jnngpCnt = root.find('body/item/jnngpCnt')
        crrmmNtcAmt = root.find('body/item/crrmmNtcAmt')

    # 예외처리하기 - 데이터가 없는 경우가 존재
    try :
        #데이터프레임에 데이터입력하기
        df_detailInfo = df_detailInfo.append(pd.Series([company_seq,jnngpCnt.text, crrmmNtcAmt.text],index=dfcol),ignore_index=True)
    except :
        error_msg =  company_seq + " sequence number error"
        print(error_msg)

    i = i+1

print(df_detailInfo)

df_detailInfo.to_csv("C:\\Users\\HyunA\\Documents\\myproject\\openAPI\\detail_info.csv", sep=',', encoding='utf-8')