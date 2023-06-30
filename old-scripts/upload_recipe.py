import requests

url = 'http://localhost:80/api/recipe/'

headers = {
    'Authorization': 'Bearer tda_c88c6a5f_8cd6_4380_843e_8dfcf6d5d29e',
}


payload = {
    'name': 'Poached Baby Vegetables With Caper Mayonnaise',
    'internal': True,
    'description': 'Plenty (page 12)',
    "keywords": [
            {
                "name": "Side Dish"
            },
        {
                "name": "Vegetarian"
            }
    ],
    'steps': [
        {
            'ingredients': [
                {
                    'food': {'name': 'burger'},
                    'unit': None,
                    "amount": ""
                },
                {
                    'food': {'name': 'burger2'},
                    'unit': None,
                    'amount': ''
                }
            ]
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
# if response.status_code == 200:
#     print('Recipe created successfully!')
# else:
#     print('Failed to create recipe. Status code:', response.status_code)
