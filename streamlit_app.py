
import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


def get_fruityvice_data(selected_fruit):
  fr_response = requests.get("https://fruityvice.com/api/fruit/" + str(selected_fruit))
  fr_norm = pd.json_normalize(fr_response.json())
  return fr_norm


st.title("Let's open a Diner")

st.header("What's on the menu?")
st.text("🥣 🥗 🐔 🍞 Sausages, bacon and 3 eggs --sunny side up")
st.text("Kale and 🥑")

st.header("Any fruits?")
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
selected_fruits = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Grapes', 'Strawberries', 'Cantaloupe'])

st.dataframe(my_fruit_list.loc[selected_fruits])

#Fruityvice response
st.header('Fruityvice Request')
try:
  fruit_choice = st.text_input('What fruit would you like info about?', 'kiwi')
  if not fruit_choice:
    st.error("Please, select a fruit to get info")
  else:
    st.write('User entered', fruit_choice)
    fr_norm = get_fruityvice_data(fruit_choice)
    st.dataframe(fr_norm)
except URLError as e:
  st.error()


# debug
st.stop()


my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
st.text("Hello from Snowflake:")
st.text(my_data_row)

my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("The fruit list:")
st.dataframe(my_data_rows)


fruit_choice_add = st.text_input('What fruit would you like to add?', 'pineapple')
st.write('Thanks for adding', fruit_choice_add)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
