from bs4 import BeautifulSoup
import requests
import lxml

def event_crawling():
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
