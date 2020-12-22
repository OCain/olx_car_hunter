import csv
from get_results import get_page_results

def save_results():
    car_list = get_page_results()
    keys = car_list[0].keys()
    file_name = 'olx_cars.csv'
    with open(file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        writer.writerows(car_list)
    print(f"Resultados salvos em: {file_name}")

