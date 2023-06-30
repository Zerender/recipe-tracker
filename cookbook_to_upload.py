import requests
from bs4 import BeautifulSoup
import json

API_URL = 'http://localhost:80/api/recipe/'
AUTH_TOKEN = 'tda_c88c6a5f_8cd6_4380_843e_8dfcf6d5d29e'

with open('bulk_links.txt', 'r') as file:
    links = file.read().splitlines()

added_cookbooks = []
with open('added_cookbooks.txt', 'a+') as added_cookbooks_file:
    added_cookbooks_file.seek(0)
    added_cookbooks = added_cookbooks_file.read().splitlines()

    for link in links:
        # Send a GET request to the webpage and parse the HTML content
        response = requests.get(link.strip())
        soup = BeautifulSoup(response.content, 'html.parser')

        book_title = soup.find('h1').contents[0].strip()

        # Check if the cookbook has already been logged
        if book_title in added_cookbooks:
            print(
                f'Cookbook "{book_title}" has already been logged. Skipping...')
            continue

        added_cookbooks_file.write(book_title + '\n')
        added_cookbooks.append(book_title)

        # Initialize a list to store the extracted data
        data = []

        # Iterate through each page until there is no next button
        while True:
            # Find all recipes
            recipes = soup.find_all('a', class_='RecipeTitleExp')

            # Iterate over each recipe element and extract the title, categories, and ingredients
            for recipe in recipes:
                recipe_title = recipe.text.strip().replace('-', ' ').title()

                # Find the recipe description
                recipe_description = recipe.find_next('i', class_='PageNoExp')
                if recipe_description:
                    page_number = recipe_description.text.strip()
                else:
                    page_number = ""

                # Find all ingredients and categories
                ingredients_and_categories = recipe.find_next(
                    'ul', class_='meta')

                categories = ingredients_and_categories.find(
                    'b', string='Categories:')
                if categories:
                    categories = [category.strip().title(
                    ) for category in categories.next_sibling.strip().split(";")]
                else:
                    categories = []

                ingredients = ingredients_and_categories.find(
                    'b', string='Ingredients:')
                if ingredients:
                    ingredients = [ingredient.strip().title(
                    ) for ingredient in ingredients.next_sibling.strip().split(";")]
                else:
                    ingredients = []

                recipe_data = {
                    'name': recipe_title,
                    'internal': True,
                    'description': book_title + ' ' + page_number,
                    'keywords': [{'name': category} for category in categories],
                    'steps': [
                        {
                            'ingredients': [
                                {
                                    'food': {'name': ingredient},
                                    'unit': None,
                                    'amount': ''
                                }
                                for ingredient in ingredients
                            ]
                        }
                    ]
                }
                data.append(recipe_data)

                # Send a POST request to the API endpoint
                headers = {'Authorization': f'Bearer {AUTH_TOKEN}'}
                response = requests.post(
                    API_URL, json=recipe_data, headers=headers)

                if response.status_code == 201:
                    print(f'Successfully uploaded recipe: {recipe_title}')
                else:
                    print(f'Failed to upload recipe: {recipe_title}')

            # Find the next button
            next_button = soup.find('a', class_='page-next')

            if next_button:
                # Find the URL of the next page
                next_page_url = next_button['href']

                # Send a GET request to the next page and update the soup object
                response = requests.get(next_page_url)
                soup = BeautifulSoup(response.content, 'html.parser')
            else:
                break
