from bs4 import BeautifulSoup
import requests
import lxml
import time

def all_event():
    page = 0
    url = "http://finance.daum.net/quote/marketvalue.daum"
    event_set = []
    while(1):
        page += 1
        html_doc = requests.get(url, params={'page':page})
        html = BeautifulSoup(html_doc.text, 'lxml')
        events = html.find_all('td', {'class':'txt'})
        for event in events:
            """
            event 모델을 장고에서 만들면 해당 데이터로 레코드를 만든다
            """
            event_set.append({})
            event_set[len(event_set)-1]['event'] = event.a.text
            event_set[len(event_set)-1]['code'] = event.a.get('href').split('=')[1]
        try:
            if page%10 == 0:
                    html.find('span', {'class':'jumpNext'}).a.text
            elif page%10 == 1:
                    html.find('span', {'class':'on'}).b.text
            else:
                html.find('a', {"href":"javascript:getPage(\'"+str(page+1)+"\');"}).text
        except:
            break
    return event_set

def graph_url(code):
    """
    종목에 대한 그래프 url은 똑같은듯함.
    """
    code = '005930'
    url = 'http://finance.daum.net/item/main.daum?nil_profile=vsearch&nil_src=stock'
    html_doc = requests.get(url, params={'code':code})
    html = BeautifulSoup(html_doc.text, 'lxml')
    graphs = html.find('div', {'id':'stockGraph'}).find_all('img')
    graph_img = []
    for graph in graphs:
        src = graph.get('src')
        graph_img.append(src)
    return graph_img

def time_quote(code):
    now = time.localtime()
    time_index = "%d%d%d%d%d" %(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min) # 년도 월 일 시 분
    url = "http://finance.naver.com/item/sise_time.nhn?code="+code+"&thistime="+time_index
    return url

def day_quote(code):
    url = "http://finance.naver.com/item/sise_day.nhn?code="+code
    return url

def stock_data(code):
    url = "http://finance.naver.com/item/sise.nhn"
    html_doc = requests.get(url, params={'code':code})
    html = BeautifulSoup(html_doc.text, 'lxml')
    stock_html = html.tbody.find_all('tr')
    stock_datas = []
    for stock_data in stock_html:
        stock_datas.append({})
        if stock_data.find('td', {'bgcolor':'#E1E1E1'}):
            continue
        th = stock_data.find_all('th')
        td = stock_data.find_all('td')
        stock_datas[len(stock_datas)-1] = {'name':th[0].text,'quote':td[0].text.replace('\t', '').replace('\n', '')}
        stock_datas.append({})
        stock_datas[len(stock_datas)-1] = {'name':th[1].text,'quote':td[1].text.replace('\t', '').replace('\n', '')}
    return stock_datas
