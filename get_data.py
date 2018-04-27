import urllib.parse
import urllib.request
import urlopen
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
# detailfile = open("C:\\Users\\HyunA\\Desktop\\detailInfo.xml","ab")
for company_seq in baseSeq :
    queryParams = '?serviceKey=' + serviceKey + '&' + urllib.parse.urlencode({urllib.parse.quote_plus('seq'): company_seq })
    # request BaseInfoSearch data
    request = urllib.request.Request(DetailInfo + queryParams)
    request.get_method = lambda: 'GET'
    response_body = urllib.request.urlopen(request).read()
    root = response_body.getroot()
    root.findall("./body/item")
    print(response_body)
    # write xml file
    # detailfile.write(response_body)
# detailfile.close()

#for data in root.iter("row") :
#    if data.findtext("LINE_NUM").find(LINE_NUM) != -1 :
#        if data.findtext("SUB_STA_NM").find(subName) != -1 :
#            string = "승차 : {0}"\n"하차 : {1}".format(data.findtext("RIDE_PASGR_NUM"), data.findtext("ALIGHT_PASGR_NUM"))
#            return string


