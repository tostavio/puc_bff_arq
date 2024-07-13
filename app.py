from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from schemas import *
from flask_cors import CORS
import requests

info = Info(title="BFF API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# tags
home_tag = Tag(name="Documentação",
               description="Choose your documentation: Swagger, Redoc or RapiDoc")
bff_tag = Tag(
    name="BFF", description="Add and update addresses")


@app.get('/', tags=[home_tag])
def home():
    """Redirect to /openapi, the page that allows you to choose the documentation style.
    """
    return redirect('/openapi')


@app.post('/address', tags=[bff_tag],
          responses={"200": AddressSchema, "400": ErrorSchema, "409": ErrorSchema})
def add_address(query: AddessGetQuerySchema):
    """Add a new address to the database

    """
    try:
        full_address_response = requests.get(
            f'https://viacep.com.br/ws/{query.zip_code}/json/')

        full_address = full_address_response.json()

        data = {
            "zip_code": full_address["cep"],
            "street": full_address["logradouro"],
            "complement": full_address["complemento"],
            "neighborhood": full_address["bairro"],
            "city": full_address["localidade"],
            "state": full_address["uf"],
            "ibge_code": full_address["ibge"],
            "gia_code": full_address["gia"],
            "ddd_code": full_address["ddd"],
            "siafi_code": full_address["siafi"],
            "user_id": query.user_id
        }

        response = requests.post('http://localhost:5000/address', data=data)

        print(response.json())
        return response.json(), 200

    except Exception as e:
        # Check if the request was successful
        if full_address_response.status_code != 200:
            return {"message": f"Request failed with status code {full_address_response.status_code}"}, full_address_response.status_code
        return {"message": "An error occurred while trying to add the address"}, response.status_code


@app.put('/address', tags=[bff_tag],
         responses={"200": AddressSchema, "400": ErrorSchema, "409": ErrorSchema})
def update_adress(query: AddessUpdateQuerySchema):
    """Update an address in the database

    Return updated address or error message.
    """
    try:
        full_address_response = requests.get(
            f'https://viacep.com.br/ws/{query.zip_code}/json/')

        full_address = full_address_response.json()

        data = {
            "zip_code": full_address["cep"],
            "street": full_address["logradouro"],
            "complement": full_address["complemento"],
            "neighborhood": full_address["bairro"],
            "city": full_address["localidade"],
            "state": full_address["uf"],
            "ibge_code": full_address["ibge"],
            "gia_code": full_address["gia"],
            "ddd_code": full_address["ddd"],
            "siafi_code": full_address["siafi"],
        }

        print("data", data)

        response = requests.put(
            f'http://localhost:5000/address?address_id={query.address_id}', data=data)

        print(response.json())
        return response.json(), 200

    except Exception as e:
        # Check if the request was successful
        if full_address_response.status_code != 200:
            return {"message": f"Request failed with status code {full_address_response.status_code}"}, full_address_response.status_code
        return {"message": "An error occurred while trying to update the address"}, response.status_code
