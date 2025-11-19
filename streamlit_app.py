# Import Python packages
import streamlit as st
from snowflake.snowpark.functions import col
from datetime import datetime

# Title
st.title(":cup_with_straw: Final Lab - Insert Clean Orders")

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

st.write("This will insert the 3 lab orders exactly as required.")

# Define the orders
orders_to_insert = [
    {"name_on_order": "Kevin", "ingredients": "Apples Lime Ximenia", "order_filled": False},
    {"name_on_order": "Divya", "ingredients": "Dragon Fruit Guava Figs Jackfruit Blueberries", "order_filled": True},
    {"name_on_order": "Xi", "ingredients": "Vanilla Fruit Nectarine", "order_filled": True}
]

# Show the orders for confirmation
for order in orders_to_insert:
    st.write(f"{order['name_on_order']} → Fruits: {order['ingredients']}, Filled: {order['order_filled']}")

# Button to insert orders
if st.button("Insert Lab Orders"):
    # Optional: truncate table first to start fresh
    session.sql("TRUNCATE TABLE smoothies.public.orders").collect()

    # Insert each order
    for order in orders_to_insert:
        ingredients_clean = " ".join(order["ingredients"].split())  # remove extra spaces
        order_filled_str = "TRUE" if order["order_filled"] else "FALSE"
        order_ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        insert_stmt = f"""
            INSERT INTO smoothies.public.orders (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED, ORDER_TS)
            VALUES ('{order['name_on_order']}', '{ingredients_clean}', {order_filled_str}, '{order_ts}')
        """
        session.sql(insert_stmt).collect()
    
    st.success("All 3 lab orders have been inserted successfully!", icon="✅")
