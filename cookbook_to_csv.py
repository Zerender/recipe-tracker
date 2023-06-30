import requests
from bs4 import BeautifulSoup
import csv

# URL of the webpage
base_url = 'https://www.eatyourbooks.com/library/176418/all-under-heaven-recipes-from'

# Send a GET request to the webpage and parse the HTML content
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

book_title = soup.find('h1').contents[0].strip()

csv_file = f'cookbooks/{book_title}.csv'

# Initialize a list to store the extracted data
data = []

# Iterate through each page until there is no next button
while True:
    # Find all recipes
    recipes = soup.find_all('a', class_='RecipeTitleExp')
    recipe_titles = [recipe.text.strip().replace('-', ' ').title()
                     for recipe in recipes]

    # Find all ingredients and categories
    ingredients_and_categories = soup.find_all('ul', class_='meta')

    # Iterate over each recipe element and extract the title, categories, and ingredients
    for i, info in enumerate(ingredients_and_categories):
        categories = info.find('b', string='Categories:').next_sibling.strip()
        categories = ";".join(categories.split("; ")).title()

        ingredients = info.find(
            'b', string='Ingredients:').next_sibling.strip()
        ingredients = ";".join(ingredients.split("; ")).title()

        full_recipe = (recipe_titles[i], categories, ingredients)
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

# Write the extracted data to a CSV file
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)

    # Write each tuple as a row in the CSV file
    writer.writerows(data)

print(f'Successfully saved {csv_file[10:-4]}')
