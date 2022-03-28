import requests
import sql
from bs4 import BeautifulSoup as BS

def get_response(url):
    response = requests.get(url)
    return response.text

def get_links(html):
    links = []
    soup = BS(html, "html.parser")
    main_content = soup.find("div", {"class": "bg_section"})
    product_content = main_content.find("div", {"class": "catalog_list_home bx_blue"})
    product_title = product_content.find_all("a")
    for product in product_title:
        href = product.get("href")
        ready_link = f"https://megastore.kg{href}"
        links.append(ready_link)
    return links


def get_product_data(html):
    soup = BS(html, "html.parser")
    main_content = soup.find("main")
    product_info = main_content.find("div", {"class": "emarket-catalog-detail"})
    product_name = product_info.find("h1").text.strip() #название
    product_desc_table = product_info.find("div", {"class": "col-sm-6 col-xs-12"})
    product_desc = product_desc_table.find("p").text.strip() #описание
    product_price = product_info.find("div", {"class": "price"}).text.strip() #цена
    available_tab = product_info.find("ul", {"id": "c_store_amount"})
    available_info = available_tab.find_all("li")
    available_list = []
    for info in available_info:
        label = info.find("a").text.strip()
        value = info.find("span").text.strip()
        available_list.append(f"{label}- {value}")
    available_ready_text = f"""{available_list[0]}, 
{available_list[1]}, 
{available_list[2]}"""


    data = {"name": product_name,
            "description": product_desc,
            "price": product_price,
            "available_info": available_ready_text,
            }
    return data

def get_mouse_data(URL):
    html = get_response(URL)
    links = get_links(html)
    for link in links:
        prodict_html = get_response(link)
        data = get_product_data(prodict_html)
        sql.update_mouses_data(data=data)

def get_keyboard_data(URL):
    html = get_response(URL)
    links = get_links(html)
    for link in links:
        prodict_html = get_response(link)
        data = get_product_data(prodict_html)
        sql.update_keyboards_data(data=data)

def get_headphones_data(URL):
    html = get_response(URL)
    links = get_links(html)
    for link in links:
        prodict_html = get_response(link)
        data = get_product_data(prodict_html)
        try:
            sql.update_headphones_data(data=data)
        except:
            print("html код отличается от стандартного вида!!!")

get_mouse_data('https://megastore.kg/catalog/vse_komp/kompyuternye_myshi/?SHOWALL_1=1')
get_keyboard_data('https://megastore.kg/catalog/vse_komp/klaviatury/?SHOWALL_1=1')
get_headphones_data('https://megastore.kg/catalog/naushnikii/?SHOWALL_1=1')
