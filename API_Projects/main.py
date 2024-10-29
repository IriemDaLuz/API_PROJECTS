import requests
from dataclass_wizard import fromdict
from models.api_response import APIResponse
from interfaz import cargarProducto

def main():
    response = requests.get('https://dummyjson.com/products')
    data_dict = response.json()
    product_list = fromdict(APIResponse, data_dict)
    cargarProducto(product_list)

if __name__ == "__main__":
    main()
