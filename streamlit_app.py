import streamlit as st
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Final Lab - Creating Orders")

cnx = st.connection("snowflake")
session = cnx.session()

orders_to_create = [
    {"name": "Kevin", "fruits": ["Apples", "Lime", "Ximenia"], "filled": False},
    {"name": "Divya", "fruits": ["Dragon Fruit", "Guava", "Figs", "Jackfruit", "Blueberries"], "filled": True},
    {"name": "Xi", "fruits": ["Vanilla Fruit", "Nectarine"], "filled": True}
]

st.write("These orders will be inserted:")
for order in orders_to_create:
    st.write(f"{order['name']} → Fruits: {', '.join(order['fruits'])}, Filled: {order['filled']}")

if st.button("Create Lab Orders"):
    for order in orders_to_create:
        ingredients_string = ' '.join(order['fruits'])
        filled_str = 'TRUE' if order['filled'] else 'FALSE'
        
        insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order, filled)
        VALUES ('{ingredients_string}', '{order['name']}', {filled_str})
        """
        
        session.sql(insert_stmt).execute()  # <-- utiliser execute() ici
        
    st.success("All 3 lab orders have been created successfully!", icon="✅")



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
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'), col('ORDER_FILLED'))
# # st.dataframe(data=my_dataframe, use_container_width=True)
# # st.stop()

# pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# # st.stop()

# # ingredients_list = st.multiselect(
# #     'Choose up the 5 fruits:'
# #     , my_dataframe
# #     , max_selections = 5
# # )
# # if ingredients_list:
# #     # st.write(ingredients_list)
# #     # st.text(ingredients_list)

# #     ingredients_string = ''
# #     for fruit_chosen in ingredients_list:
# #       ingredients_string += fruit_chosen + ' '
# #       search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
# #       st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
# #       st.subheader(fruit_chosen + 'Nutrition Information')
# #       smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
# #       if name_on_order == "Kevin" :
# #         order_filled = False
# #       if name_on_order == "Divya" :
# #         order_filled = True
# #       if name_on_order == "Xi" :
# #         order_filled = False
# #       st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

# #     my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order, order_filled)
# #             values ('{ingredients_string}', '{name_on_order}', {order_filled})"""

    
# #     time_to_insert = st.button('Submit Order')
# #     if time_to_insert:
# #         # session.sql(my_insert_stmt).collect()
# #         # st.success('Your Smoothie is ordered!', icon="✅")
# #       st.write(my_insert_stmt)
# #     st.stop()
