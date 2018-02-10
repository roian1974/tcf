import urllib.request

# https://wayhome25.github.io/python/2017/07/15/naver-search-api/
# 검색어 : ‘파이썬’ (query)
# 검색결과는 3개 출력 (display=3)
# 정렬 옵션 : 판매량순 (sort=count)

client_id = "MY_CLIENT_ID"  # 애플리케이션 등록시 발급 받은 값 입력
client_secret = "MY_CLIENT_SECRET"  # 애플리케이션 등록시 발급 받은 값 입력

encText = urllib.parse.quote("파이썬")
url = "https://openapi.naver.com/v1/search/book?query=" + encText + "&display=3&sort=count"
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

response = urllib.request.urlopen(request)
rescode = response.getcode()

if (rescode == 200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)