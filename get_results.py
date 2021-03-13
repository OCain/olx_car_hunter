from bs4 import BeautifulSoup as soup
from urllib.request import Request as request, urlopen
import urls

UL_MAIN_CLASS = "sc-1fcmfeb-0 FBZzf"
CREATION_DATE_SPAN_CLASS = "wlwg1t-1 fsgKJO sc-ifAKCX eLPYJb"


def get_request_data():
    return urls.get_request_data()


def get_page_results():
    request_data = get_request_data()
    cars = []
    for data in request_data:
        car_li_elements = get_car_li_elements(data)
        if (len(car_li_elements) > 0):
            cars.extend(get_car_list(car_li_elements, data))
    return cars


def get_html_page(data):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
    try:
        page_request = request(data["link"], headers=headers)
        document = urlopen(page_request)
        html_page = soup(document.read(), "html.parser")
        document.close()
        return html_page
    except:
        print("Falha de conexão.")

def get_car_li_elements(data):
    page = get_html_page(data)
    car_ul = page.findAll("div", {"class": UL_MAIN_CLASS})
    car_li_elements = []
    descricao_carro = data["manufacterer"] + " " + data["model"] + " " + data["description"] 
    try:
        print(f"Buscando anúncios de {descricao_carro}...")
        li_elements = get_li_elements(car_ul)
        for li in li_elements:
            if(li.a):
                car_li_elements.append(li)
    except:
        print(f"Não foram encontrados anúncios para {descricao_carro}.")
    return car_li_elements

def get_li_elements(car_ul):
    return car_ul[0].ul.findAll("li")


def get_car_list(car_li_elements, data):
    cars = []
    for li_tag in car_li_elements:
        spans = li_tag.a.div.findAll("span")
        car = {
            "manufacterer": data["manufacterer"],
            "model": data["model"],
            "link": li_tag.a["href"],
            "title": li_tag.a["title"],
            "price": get_price(spans),
            "creation_date": get_created_date(spans)
        }
        if (data["description"] in car["title"]):
            cars.append(car)
    return cars

def get_price(span_elements):
    for span in span_elements:
        text = span.text
        if (text.startswith("R$")):
            return text

def get_created_date(span_elements):
    date = ''
    for span in span_elements:
        if span['class'] == CREATION_DATE_SPAN_CLASS.split(" "):
            date += span.text + " "
    return date