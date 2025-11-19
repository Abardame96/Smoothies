# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

st.title(":cup_with_straw: Customize Your Smoothie!")
st.write("Choose the fruits you want in your custom Smoothie")

# Input pour le nom
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Mapping pour savoir si la commande est remplie
users_map = {
    "Kevin": False,
    "Divya": True,
    "Xi": True
}

# Connexion Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Table des fruits
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()

# Multiselect pour choisir les fruits
ingredients_list = st.multiselect(
    'Choose up the 5 fruits:',
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

if ingredients_list and name_on_order:
    # Créer la chaîne de fruits
    ingredients_string = ' '.join(ingredients_list)
    
    # Récupérer automatiquement la valeur filled pour ce nom
    order_filled = users_map.get(name_on_order, False)
    filled_str = 'TRUE' if order_filled else 'FALSE'
    
    # Afficher les informations nutritionnelles
    for fruit_chosen in ingredients_list:
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for', fruit_chosen, 'is', search_on)
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        st.dataframe(smoothiefroot_response.json(), use_container_width=True)
    
    # Créer la requête SQL correctement
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order, filled)
    VALUES ('{ingredients_string}', '{name_on_order}', {filled_str})
    """
    
    # Bouton pour envoyer la commande
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        st.write("Executed SQL:", my_insert_stmt)
