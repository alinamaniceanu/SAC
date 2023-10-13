from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import AddItem, AddItemProperty, SetItemValues, ListItems
from recombee_api_client.exceptions import APIException
import pandas as pd

client = RecombeeClient(
  'sac-lab-prod', 
  'wioGEAohYvYtY3cJMsP7euqHcTStawevElTkvB2gRyHyrsSzkiA3EEv2SAsIwXG4', 
  region=Region.EU_WEST
)

df = pd.read_csv('./mindfactory_done.csv', usecols=["name", "price_eur", "display_inch", "weight_kg"])
ITEM_PROPERTIES = [('name', 'string'), ('price_eur', 'double'), ('display_inch', 'double'), ('weight_kg', 'double')]


def add_item_properties():
    for prop_name, prop_type in ITEM_PROPERTIES:
        client.send(AddItemProperty(prop_name, prop_type))

def add_items():
    for index, row in df.iterrows():
        item_id = str(index)
        try:
            client.send(AddItem(item_id))
            print(f"Item: {item_id} added")
        except APIException as e:
            print(f"Error adding item {item_id}: {e}")

    for index, row in df.iterrows():
        name = row['name']
        price_eur = row['price_eur']
        display_inch = row['display_inch']
        weight_kg = row['weight_kg']

        item_data = {
            'name': name,
            'price_eur': price_eur,
            'display_inch': display_inch,
            'weight_kg': weight_kg,
        }
        client.send(SetItemValues(str(index), item_data))

def print_items():
    result = client.send(ListItems(return_properties=True))
    print(result)

# add_item_properties()
# add_items()
print_items()
