
import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


def get_fruityvice_data(selected_fruit):
  fr_response = requests.get("https://fruityvice.com/api/fruit/" + str(selected_fruit))
  fr_norm = pd.json_normalize(fr_response.json())
  return fr_norm

def get_connection():
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  return my_cnx

def get_fruit_load_list():
  my_cnx = get_connection()
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
def insert_row_snowflake(row_val, table):
  my_cnx = get_connection()
  with my_cnx.cursor() as my_cur:
    my_cur.execute(f"insert into {table} values ('{row_val}')")
    return f"Thanks for adding {row_val} to table \t\t{table}"
  


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



if st.button("Get fruit load list"):
  my_data_rows = get_fruit_load_list()
  st.header("The fruit list:")
  st.dataframe(my_data_rows)

fruit_choice_add = st.text_input('What fruit would you like to add?', 'pineapple')
if st.button("Add a fruit to the list"):
  response = insert_row_snowflake(fruit_choice_add, 'fruit_load_list')
  st.text(response)
 # st.write('Thanks for adding', fruit_choice_add)

 # my_cur.execute("insert into fruit_load_list values ('from streamlit')")
