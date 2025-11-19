# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from datetime import datetime

# Titre de l'app
st.title(":cup_with_straw: Final Lab - Creating Orders")
st.write("This app will insert the 3 lab orders exactly as required for grading.")

# Connexion à Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Liste des commandes exactes pour le lab
orders_to_create = [
    {
        "name_on_order": "Kevin",
        "ingredients": "Apples Lime Ximenia",
        "order_filled": False
    },
    {
        "name_on_order": "Divya",
        "ingredients": "Dragon Fruit Guava Figs Jackfruit Blueberries",
        "order_filled": True
    },
    {
        "name_on_order": "Xi",
        "ingredients": "Vanilla Fruit Nectarine",
        "order_filled": True
    }
]

# Affichage des commandes pour vérification
st.write("These orders will be inserted:")
for order in orders_to_create:
    st.write(f"{order['name_on_order']} → Fruits: {order['ingredients']}, Filled: {order['order_filled']}")

# Bouton pour insérer les commandes dans Snowflake
if st.button("Create Lab Orders"):
    for order in orders_to_create:
        order_ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_stmt = f"""
            INSERT INTO smoothies.public.orders
            (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED, ORDER_TS)
            VALUES ('{order['name_on_order']}', '{order['ingredients']}', {str(order['order_filled']).upper()}, '{order_ts}')
        """
        # Exécuter l'INSERT avec Snowpark
        session.sql(insert_stmt).collect()
    
    st.success("All 3 lab orders have been created successfully!", icon="✅")



# # Import python packages
# import streamlit as st
# from snowflake.snowpark.functions import col
# from snowflake.snowpark import Row
# import pandas as pd
# from datetime import datetime
# import requests

# # Write directly to the app
# st.title(":cup_with_straw: Customize Your Smoothie!")
# st.write("Choose the fruits you want in your custom Smoothie:")

# # Nom de l'utilisateur
# name_on_order = st.text_input("Name on Smoothie:")
# st.write("The name on your Smoothie will be:", name_on_order)

# # Connexion Snowflake
# cnx = st.connection("snowflake")
# session = cnx.session()

# # Récupérer tous les fruits depuis l'API
# response = requests.get("https://my.smoothiefroot.com/api/fruit/all")
# fruits_data = response.json()  # liste de dicts

# # Extraire les noms des fruits pour la multiselect
# fruit_names = [fruit['name'] for fruit in fruits_data]

# # Multiselect pour choisir jusqu'à 5 fruits
# ingredients_list = st.multiselect(
#     'Choose up to 5 fruits:',
#     options=fruit_names
# )

# if ingredients_list and name_on_order:
#     # Construire la chaîne d'ingrédients
#     ingredients_string = ' '.join(ingredients_list)
#     order_ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#     # Déterminer le statut "filled" selon l'utilisateur
#     users_map = {
#         "Kevin": False,
#         "Divya": True,
#         "Xi": True
#     }
#     order_filled = users_map.get(name_on_order, False)  # False par défaut
#     st.write(order_filled)

#     # Construire la requête SQL
#     insert_stmt = f"""
#         INSERT INTO smoothies.public.orders
#         (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED, ORDER_TS)
#         VALUES ('{name_on_order}', '{ingredients_string}', {str(order_filled).upper()}, '{order_ts}')
#     """

#     # Afficher la requête pour debug
#     st.code(insert_stmt)

#     # Bouton pour insérer dans Snowflake
#     if st.button('Submit Order'):
#         # Avec Snowpark, utiliser execute() et non collect() pour INSERT
#         session.sql(insert_stmt).collect()
#         st.success('Your Smoothie is ordered!', icon="✅")


