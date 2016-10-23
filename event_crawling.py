from bs4 import BeautifulSoup
import requests
import lxml
import time


def business():
    """
    반환 : [{'business':업종 이름, 'title':종목 이름, 'code':종목코드, 'price':종목 현재가, 'change':등락률:소수로 형변환 }, ....]
    """
    url="http://finance.daum.net/quote/all.daum?nil_profile=stockprice&nil_menu=siseleftmenu23"
    html_doc = requests.get(url)
    html = BeautifulSoup(html_doc.text, 'lxml')
    table_tag = html.find_all('table', {'class':'gTable'})
    h4_tag = html.find_all('h4', {'class':'fl_le'})
    business_list = []
    for i in range(len(h4_tag)):
        business_name = h4_tag[i].text.split('|')[0]
        stock_html = table_tag[i].find_all('tr')
        for stocks in stock_html:
            try:
                error = stocks.find('td',{'class':'txt'}).txt
            except:
                print('error1')
                continue
            stock = stocks.find_all('td')
            txt = stocks.find_all('td',{'class':'txt'})
            code = txt[0].a.get('href')[-6:]
            business_list.append({'business':business_name, 'title':stock[0].text, 'price':stock[1].text.replace(',',''), 'change':float(stock[2].text.replace('%', '')), 'code':code})
            try:
                code = txt[1].a.get('href')[-6:]
                business_list.append({'business':business_name, 'title':stock[3].text, 'price':stock[4].text.replace(',',''), 'change':float(stock[5].text.replace('%','')), 'code':code})
            except:
                print('error2')
                continue
    return business_list

#for i in a:
#    Stock.objects.create(business=i['business'], title=i['title'], price=i['price'], code=i['code'])

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
    url = "http://finance.daum.net/item/main.daum"
    html_doc = requests.get(url, params={'code':code})
    html = BeautifulSoup(html_doc.text, 'lxml')
    stock_html = html.find('div', {'id':'stockContent'}).find_all('dl')
    stock_datas=[]
    for stock in stock_html:
        name = stock.dt.text
        quote = stock.dd.text.replace('\t', '').replace('\n', '').replace(',', '').replace('-','')
        if (name=="전일"):
            stock_datas.append({'yesterday_price':int(quote)})
        elif(name=='고가'):
            stock_datas.append({'high_price':int(quote)})
        elif(name=='저가'):
            stock_datas.append({'low_price':int(quote)})
        elif(name=='시가'):
            stock_datas.append({'today_start_price':int(quote)})
        elif(name=='상한가'):
            stock_datas.append({'max_price':int(quote)})
        elif(name=='하한가'):
            stock_datas.append({'min_price':int(quote)})
            break
    return stock_datas
