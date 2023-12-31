import requests
from bs4 import BeautifulSoup
import json

with open('bulk_links.txt', 'r') as file:
    links = file.read().splitlines()

for link in links:

    # Send a GET request to the webpage and parse the HTML content
    response = requests.get(link.strip())
    soup = BeautifulSoup(response.content, 'html.parser')

    book_title = soup.find('h1').contents[0].strip()

    json_file = f'cookbooks/{book_title}.json'

    # Initialize a list to store the extracted data
    data = []

    # Iterate through each page until there is no next button
    while True:
        # Find all recipes
        recipes = soup.find_all('a', class_='RecipeTitleExp')
        recipe_titles = [recipe.text.strip().replace('-', ' ').title()
                         for recipe in recipes]

        # Iterate over each recipe element and extract the title, categories, and ingredients
        for i, info in enumerate(recipes):
            # Get the page description
            page_description = info.find_next('i', class_='PageNoExp')
            if page_description:
                page_number = page_description.text.strip()
            else:
                page_number = ""

            # Find all ingredients and categories
            ingredients_and_categories = info.find_next('ul', class_='meta')

            categories = ingredients_and_categories.find(
                'b', string='Categories:').next_sibling.strip()
            categories = ";".join(categories.split("; ")).title()

            ingredients = ingredients_and_categories.find(
                'b', string='Ingredients:').next_sibling.strip()
            ingredients = ";".join(ingredients.split("; ")).title()

            full_recipe = {
                "name": recipe_titles[i],
                "recipeCategory": categories.split(";"),
                "recipeIngredient": ingredients.split(";"),
                "description": book_title + ' ' + page_number
            }
            data.append(full_recipe)

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

    # Convert the data to a JSON string
    json_data = json.dumps(data, indent=4, separators=(",", ": "))

    # Write the JSON data to a file
    with open(json_file, "w") as file:
        file.write(json_data)

    print(f'Successfully saved {json_file[10:-5]}')
