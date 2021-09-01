import pandas as pd
import matplotlib.pyplot as plt
import io
import requests
import openpyxl
import streamlit as st

from website_fds.params import BUCKET_NAME, CLEAN_DATA_STORAGE_LOCATION

header = st.beta_container()
user_input = st.beta_container()
output_graphs = st.beta_container()
author_credits = st.beta_container()

with header:
    st.title("Welcome to the football data scouting project")
    st.markdown("""
    #### By: [Marco Cerrato](https://www.linkedin.com/in/marcocerratofontecha/)

    Welcome to the football data scouting project. This web application displays current information on the total number of Covid-19 cases reported in your selected county. With this application, you can get concise information on the number of total cases, deaths, and daily cases.
    **Note:** If you don't see the "User Selection" sidebar, please press the `>` icon on the top left side of your screen.

    """)

# Fetch Dataset from the New York Times Github Repository
# url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
# s = requests.get(url).content
# df = pd.read_csv(io.StringIO(s.decode('utf-8')),
#                  parse_dates=True,
#                  index_col='date')

df = pd.read_csv(f'gs://{BUCKET_NAME}/{CLEAN_DATA_STORAGE_LOCATION}players_streamlit.csv')



with user_input:
    st.sidebar.header('Player selection')

    # Generating the list for states
    position_list = ["Defender", "Forward", "Midfield"]
    years_list = []
    leagues_list=[]
    squads_list =[]

    position_list.sort()

    position = st.sidebar.selectbox('Select your position:',
                                 position_list)  # We define the state variable

    if position.lower() == "defender":
        df_pos=df[df['is_df']==1].copy()
    elif position.lower() =="forward":
        df_pos= df[df['is_fw'] == 1].copy()
    elif position.lower() =="midfield":
        df_pos= df[df['is_mf'] == 1].copy()

    years_list = df_pos.season_year.unique()
    years_list.sort()

    year = st.sidebar.selectbox(
        'Select your season:', years_list)  # We define the county variable

    df_pos=df_pos[df_pos["season_year"]==year]

    leagues_list = df_pos.new_league_name.unique()
    leagues_list.sort()


    league = st.sidebar.selectbox('Select your league:',
                                leagues_list)  # We define the county variable


    df_pos=df_pos[df_pos["new_league_name"]==league]

    squads_list = df_pos.squad.unique()
    squads_list.sort()


    squad = st.sidebar.selectbox('Select your squad:',
                                squads_list)  # We define the county variable

    df_pos=df_pos[df_pos["squad"]==squad]

    players_list = df_pos.player_name.unique()
    players_list.sort()


    player = st.sidebar.selectbox('Select your player:',
                                players_list)  # We define the county variable



    # table_days = st.sidebar.slider(
    #     'Select the number of days you want to be display in the Summary Table. ',
    #     min_value=3,
    #     max_value=15,
    #     value=5,
    #     step=1)

    # moving_average_day = st.sidebar.slider(
    #     'How many days to consider for the moving average? ',
    #     min_value=5,
    #     max_value=14,
    #     value=7,
    #     step=1)

    # # Creating the dataframe for the county
    # df_county = df[(df.county == county) & (df.state == state)].copy()

    # #Create a new column with new cases
    # df_county['new_cases'] = df_county.loc[:, 'cases'].diff()

    # #Create a new column for 7-day moving average
    # df_county['moving_average'] = df_county.loc[:, 'new_cases'].rolling(
    #     window=moving_average_day).mean()

    # #Create a

# with output_graphs:

#     # Summary Table

#     st.header(f'Summary Table for the last {table_days} days.')

#     st.markdown(
#         """ This table includes the number of cases, deaths, new cases and moving average for your selection."""
#     )

#     #st.write(df_county.iloc[-table_days:,-4:])

#     a = df_county.iloc[-table_days:, -4:]

#     my_table = st.table(a)

#     # Total Cases Graph

#     st.header(f'Total Cases for {county},{state}.')

#     total_cases_chart = df_county['cases']

#     st.line_chart(total_cases_chart)

#     st.markdown(
#         """**Note:** You can zoom on this graph if you are in front of a Desktop or Laptop by using your scrolling wheel on your mouse. You can also point on the line to get more information."""
#     )

#     # Moving Average Graph

#     st.header(f'{moving_average_day} moving average for {county},{state}.')

#     moving_average_chart = df_county['moving_average']

#     st.line_chart(moving_average_chart)

#     st.markdown(
#         """**Note:** You can zoom on this graph if you are in front of a Desktop or Laptop by using your scrolling wheel on your mouse. You can also point on the line to get more information."""
#     )

#     # Death Graph

#     st.header(f'Total Deaths for {county},{state}.')

#     total_deaths_chart = df_county['deaths']

#     st.line_chart(total_deaths_chart)

#     st.markdown(
#         """**Note:** You can zoom on this graph if you are in front of a Desktop or Laptop by using your scrolling wheel on your mouse. You can also point on the line to get more information."""
#     )

# with author_credits:
#     st.header(f'Credits')
#     st.markdown("""
#     **Thank you for using my application!**

#     The dataset used to feed this application is provided by [New York Times Covid-19 Github Repository](https://github.com/nytimes/covid-19-data).
#     This application uses the Streamlit package library. You can learn more about me and my other projects by visiting my website [Not A Programmer] (https://notaprogrammer.com) or [my Github Repo] (https://github.com/cerratom).
#     """)
