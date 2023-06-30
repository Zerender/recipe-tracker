import csv
import json


def csv_to_json(csv_file, json_file):
    # Open the CSV file for reading
    with open(csv_file, 'r') as file:
        # Create a CSV reader object
        reader = csv.DictReader(file)

        # Initialize an empty list to store the rows
        rows = []

        # Iterate over each row in the CSV file
        for row in reader:
            # Split categories and ingredients by semicolon and convert them to lists
            categories = row['Categories'].split(';')
            ingredients = row['Ingredients'].split(';')

            # Create a new row dictionary with separated categories and ingredients
            new_row = {
                'Recipe': row['Recipe'],
                'Categories': categories,
                'Ingredients': ingredients
            }

            # Append the new row to the list
            rows.append(new_row)

    # Open the JSON file for writing
    with open(json_file, 'w') as file:
        # Write the rows to the JSON file
        json.dump(rows, file, indent=4)


# Provide the path to your CSV file
csv_file = 'cookbooks/Plenty.csv'

# Provide the desired path and name for the output JSON file
json_file = 'output.json'

# Call the function to convert CSV to JSON
csv_to_json(csv_file, json_file)
