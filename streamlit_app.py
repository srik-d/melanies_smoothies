# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw: ")
st.write(
  """ Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie ")
st.write("Your name on Smoothie will be: ", name_on_order)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
options = [r['FRUIT_NAME'] for r in session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()]

ingredients_list = st.multiselect('Choose up to 5 ingredients: ', options,max_selections=5)
if ingredients_list:
    ingredients_string = ",".join(ingredients_list)
    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
                        values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ' + name_on_order, icon="✅")

import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
#st.text(smoothiefroot_response)
sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

