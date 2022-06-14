import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title ('My Parents New Healthy Diner')

streamlit.header ('Breakfast Favorites')
streamlit.text ('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text ('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text ('🐔 Hard-Boiled Free-Range Egg')
streamlit.text ('🥑🍞 Avocado Toast')

streamlit.header ('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# my fruit pick list code and import pandas

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

#New Section to Display Fruityvice API Response
streamlit.header('Fruityvice Fruit Advice')
fruit_choice = streamlit.text_input('What fruit would you liek information about?','Kiwi')
streamlit.write('The user entered', fruit_choice)


fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)


# this will take the json version of the reponse and normalize it to look like a nice table
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output it the screen as a table
streamlit.dataframe(fruityvice_normalized)

# don't run anything past here while we troubleshoot
streamlit.stop()



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list containts:")
streamlit.dataframe(my_data_rows)

# allow the users to add more fruit to the list with a new data box

add_my_fruit = streamlit.text_input('What fruit would you add?', 'jackfruit')
streamlit.text ('Thanks for adding ' + add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
