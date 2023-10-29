from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import AddItem, AddItemProperty, SetItemValues, ListItems, AddUser, AddDetailView, RecommendItemsToUser
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

def add_users(user_ids):
    for user_id in user_ids:
        try:
            client.send(AddUser(user_id))
            print(f"User: {user_id} added")
        except APIException as e:
            print(f"Error adding user {user_id}: {e}")	

def add_interactions(user_ids, item_ids):
    for user_id in user_ids:
        for item_id in item_ids:
            try:
                client.send(AddDetailView(user_id, item_id))
                print(f"User {user_id} viewed item {item_id}")
            except APIException as e:
                print(f"Error adding view interaction: {e}")

def get_recommendations(user_id, num_recommendations):
    recommendations = client.send(RecommendItemsToUser(user_id, num_recommendations))
    recommended_items = [item['id'] for item in recommendations['recomms']]
    return recommended_items


# add_item_properties()
# add_items()
print_items()

# user_ids = ["user1", "user2", "user3"]
# add_users(user_ids)

# user_ids = ["user1", "user2"]
# item_ids = ["77", "268"]
# add_interactions(user_ids, item_ids)

user_id = "user3"
num_recommendations = 5
recommended_items = get_recommendations(user_id, num_recommendations)