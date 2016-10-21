from bs4 import BeautifulSoup
import requests
import lxml
import time

def business():
    """
    반환 : [{'business_name':업종 이름, 'event':종목 이름, 'code':종목코드, 'price':종목 현재가, 'change':등락률 }, ....]
    기타 업종 제외.
    """
    base_url="http://finance.daum.net/quote/upjong_sub.daum?stype=P"
    html_doc = requests.get(base_url)
    html = BeautifulSoup(html_doc.text, 'lxml')
    business_html = html.find('table', {'id':'bizBody1'}).find_all('tr')
    event_set = []
    for business in business_html:
        try:
            name = business.find('td', {'class':'txt'}).text
            number = business.find('td', {'class':'txt'}).a.get('href')[-2:]
        except:
            continue
        page = 0
        while(1):
            page += 1
            url = "http://finance.daum.net/quote/upjong_detail_sub.daum?stype=P&col=pchgrate&order=desc"
            html_doc = requests.get(url, params={'seccode':number,'page':page})
            html = BeautifulSoup(html_doc.text, 'lxml')
            events_html = html.find_all('tr')
            for event_html in events_html:
                try:
                    event = event_html.find('td', {'class':'txt'}).text
                    code = event_html.find('td', {'class':'txt'}).a.get('href')[-6:]
                    price = event_html.find_all('td', {'class':'cUp'})[0].text
                    change = event_html.find_all('td', {'class':'cUp'})[1].text
                except:
                    continue
                else:
                    event_set.append({'business_name':name, 'event':event, 'code':code, 'price':price, 'change':change})
            try:
                if page%10 == 0:
                        html.find('span', {'class':'jumpNext'}).a.text
                elif page%10 == 1:
                        html.find('a', {"href":"javascript:goPage(\'"+str(page+1)+"\');"}).text
                else:
                    html.find('a', {"href":"javascript:goPage(\'"+str(page+1)+"\');"}).text
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
