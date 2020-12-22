import json
from filters import olx_year_values as year

ENDPOINT = "https://sc.olx.com.br/florianopolis-e-regiao/autos-e-pecas/carros-vans-e-utilitarios"

PRICE_MIN_FILTER = "ps="
PRICE_MAX_FILTER = "pe="
KM_MAX_FILTER = "me="
KM_MIN_FILTER = "ms="
YEAR_MAX_FILTER = "re="
YEAR_MIN_FILTER = "rs="
DESCRIPTION_FILTER = "q="


def get_request_data():
    request_data = []
    filters = load_filters()
    for filter in filters:
        data = {
            "manufacterer": filter["marca"],
            "model": filter["modelo"],
            "description": filter["descricao"],
            "link": build_url(filter)
        }
        # print(data["link"])
        request_data.append(data)
    return request_data


def load_filters():
    with open("filters/filters.json") as json_file:
        return json.load(json_file)


def build_url(filter):
    link_builder = []
    link_builder.append(ENDPOINT)
    link_builder.append("/")
    link_builder.append(filter["marca"])
    link_builder.append("/")
    link_builder.append(filter["modelo"])
    link_builder.append("?")
    link_builder.append(KM_MAX_FILTER + filter["quilometragem"][1])
    link_builder.append("&")
    link_builder.append(KM_MIN_FILTER + filter["quilometragem"][0])
    link_builder.append("&")
    link_builder.append(PRICE_MAX_FILTER + filter["preco"][1])
    link_builder.append("&")
    link_builder.append(PRICE_MIN_FILTER + filter["preco"][0])
    link_builder.append("&")
    link_builder.append(YEAR_MAX_FILTER + year.values[filter["ano"][1]])
    link_builder.append("&")
    link_builder.append(YEAR_MIN_FILTER + year.values[filter["ano"][0]])
    return ''.join(link_builder)