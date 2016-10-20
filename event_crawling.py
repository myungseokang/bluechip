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
    graph_img.pop()
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
    """
    ex code = 005930
    """
    url = "http://finance.daum.net/item/main.daum"
    html_doc = requests.get(url, params={'code':code})
    html = BeautifulSoup(html_doc.text, 'lxml')
    stock_html = html.find('div', {'id':'stockContent'}).find_all('dl')
    stock_datas=[]
    for stock in stock_html:
        name = stock.dt.text
        quote = stock.dd.text.replace('\t', '').replace('\n', '')
        if (name=='전일' or name=='고가' or name=='저가' or name=='시가' or name=='상한가' or name=='하한가'):
            stock_datas.append({'name':name, 'quote':quote})
            if (name=='하한가'):
                break
    return stock_datas
