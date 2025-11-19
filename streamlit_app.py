# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark import Row
import pandas as pd
from datetime import datetime
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!")
st.write("Choose the fruits you want in your custom Smoothie:")

# Nom de l'utilisateur
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Connexion Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Récupérer tous les fruits depuis l'API
response = requests.get("https://my.smoothiefroot.com/api/fruit/all")
fruits_data = response.json()  # liste de dicts

# Extraire les noms des fruits pour la multiselect
fruit_names = [fruit['name'] for fruit in fruits_data]

# Multiselect pour choisir jusqu'à 5 fruits
ingredients_list = st.multiselect(
    'Choose up to 5 fruits:',
    options=fruit_names,
    max_selections=5
)

if ingredients_list and name_on_order:
    # Construire la chaîne d'ingrédients
    ingredients_string = ' '.join(ingredients_list)
    order_ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Déterminer le statut "filled" selon l'utilisateur
    users_map = {
        "Kevin": False,
        "Divya": True,
        "Xi": True
    }
    order_filled = users_map.get(name_on_order, False)  # False par défaut

    # Construire la requête SQL
    insert_stmt = f"""
        INSERT INTO smoothies.public.orders
        (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED, ORDER_TS)
        VALUES ('{name_on_order}', '{ingredients_string}', {str(order_filled).upper()}, '{order_ts}')
    """

    # Afficher la requête pour debug
    st.code(insert_stmt)

    # Bouton pour insérer dans Snowflake
    if st.button('Submit Order'):
        # Avec Snowpark, utiliser execute() et non collect() pour INSERT
        session.sql(insert_stmt).execute()
        st.success('Your Smoothie is ordered!', icon="✅")



# # Import python packages
# import streamlit as st
# from snowflake.snowpark.functions import col
# import requests

# # Write directly to the app
# st.title(":cup_with_straw: Customize Your Smoothie!")
# st.write(
#   """Choose the fruits you want in your custom Smoothie
#   """
# )

# name_on_order = st.text_input("Name on Smoothie:")
# st.write("The name on your Smoothie will be: ", name_on_order)

# users_map = {
#   "Kevin" : False,
#   "Divya" : True,
#   "Xi": True
# }

# cnx = st.connection("snowflake")
# session = cnx.session()
# my_dataframe = session.table("smoothies.public.orders").select(col('NAME_ON_ORDER'), col('INGREDIENTS'), col('ORDER_FILLED'))
# # st.dataframe(data=my_dataframe, use_container_width=True)
# # st.stop()
# smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/all")
# st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
# st.write(st_df['name'])

# ingredients_list = st.multiselect(
#     'Choose up the 5 fruits:'
#     , fruits
#     , max_selections = 5
# )
# if ingredients_list:
#     # st.write(ingredients_list)
#     # st.text(ingredients_list)
#     pd_df = my_dataframe.to_pandas()
#     st.dataframe(pd_df)
#     ingredients_string = ''
#     for fruit_chosen in ingredients_list:
#       ingredients_string += fruit_chosen + ' '
#       order_ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#       # search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
#       # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
#       st.subheader(fruit_chosen + 'Nutrition Information')
#       # smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
#       if name_on_order == "Kevin" :
#         order_filled = False
#       if name_on_order == "Divya" :
#         order_filled = True
#       if name_on_order == "Xi" :
#         order_filled = False
#       # st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

#       insert_stmt = f"""
#                       INSERT INTO smoothies.public.orders (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED, ORDER_TS)
#                       VALUES ('{name_on_order}', '{ingredients_string}', {str(order_filled).upper()}, '{order_ts}')
#                   """

#     st.write(insert_stmt)
#     time_to_insert = st.button('Submit Order')
#     if time_to_insert:
#         session.sql(insert_stmt).collect()
#         st.success('Your Smoothie is ordered!', icon="✅")
      
#     st.stop()
