# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie")
st.write("Your name on Smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

# Create pd_df from Snowflake table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True) # Un-comment to see raw data
# st.stop() # Un-comment to focus only on data loading

# Convert Snowpark Dataframe to Pandas Dataframe
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df) # Un-comment to verify pd_df
# st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'],
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        # 1. Grab the search value (Keeping it hidden from UI)
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        
        # We removed the st.write line that was showing the search value here

        st.subheader(fruit_chosen + ' Nutrition Information')
        
        # Using the search_on value for the API call
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Building the insert statement
    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        # 2. This will now show the success message clearly after the tables
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
