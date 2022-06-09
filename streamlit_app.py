
import streamlit as st
import pandas as pd

st.title("Let's open a Diner")

st.header("What's on the menu?")
st.text("🥣 🥗 🐔 🍞 Sausages, bacon and 3 eggs --sunny side up")
st.text("Kale and 🥑")

st.header("Any fruits?")
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
selected_fruits = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Grapes', 'Strawberries', 'Cantaloupe'])

st.dataframe(my_fruit_list.loc[selected_fruits])

