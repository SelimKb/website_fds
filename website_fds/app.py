import pandas as pd
import io
import requests
import streamlit as st

from website_fds.params import BUCKET_NAME, CLEAN_DATA_STORAGE_LOCATION

header = st.container()
user_input = st.container()
input_summary = st.container()
output_graphs = st.container()
author_credits = st.container()

with header:
    st.title("Welcome to the football data scouting project")
    st.markdown("""
    #### By: [Marco Cerrato](https://www.linkedin.com/in/marcocerratofontecha/)

    Welcome to the football data scouting project. This web application displays current information on the total number of Covid-19 cases reported in your selected county. With this application, you can get concise information on the number of total cases, deaths, and daily cases.

    """)

# Fetch Dataset from the New York Times Github Repository
# url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
# s = requests.get(url).content
# df = pd.read_csv(io.StringIO(s.decode('utf-8')),
#                  parse_dates=True,
#                  index_col='date')

df = pd.read_csv(f'gs://{BUCKET_NAME}/{CLEAN_DATA_STORAGE_LOCATION}players_streamlit.csv')
url = 'https://footballscouting-qpmhphei7q-ew.a.run.app/get_close_players'


with user_input:
    st.sidebar.header('Player selection')

    # Generating the list for states
    position_list = ["Defender", "Forward", "Midfield"]
    years_list = []
    leagues_list=[]
    squads_list =[]

    position_list.sort()

    position = st.sidebar.selectbox('Select your position:',
                                 position_list)  # We define the position variable

    if position.lower() == "defender":
        df_pos=df[df['is_df']==1].copy()
    elif position.lower() =="forward":
        df_pos= df[df['is_fw'] == 1].copy()
    elif position.lower() =="midfield":
        df_pos= df[df['is_mf'] == 1].copy()

    years_list = df_pos.season_year.unique()
    years_list.sort()

    year = st.sidebar.selectbox(
        'Select your season:', years_list)  # We define the season variable

    df_pos=df_pos[df_pos["season_year"]==year]

    leagues_list = df_pos.new_league_name.unique()
    leagues_list.sort()


    league = st.sidebar.selectbox('Select your league:',
                                leagues_list)  # We define the league variable


    df_pos=df_pos[df_pos["new_league_name"]==league]

    squads_list = df_pos.squad.unique()
    squads_list.sort()


    squad = st.sidebar.selectbox('Select your squad:',
                                squads_list)  # We define the squad variable

    df_pos=df_pos[df_pos["squad"]==squad]

    players_list = df_pos.player_name.unique()
    players_list.sort()


    player = st.sidebar.selectbox('Select your player:',
                                players_list)  # We define the player variable
    



with input_summary:

    params = {'position':position,'player_name':player,'season_year':year}
    response = requests.get(url, params).json()
    
    player_selected = df[df['player_name']==player].loc[df['season_year']==year,:]

    col1, col2, col3 = st.columns((1,2,2))
    # photo_req = requests.get(player_selected['photo'].to_list()[0])
    # photo_player = io.BytesIO(photo_req.content)
    # flag_req = requests.get(player_selected['flag'].to_list()[0])
    # flag_player = io.BytesIO(flag_req.content)
    # col1.image(photo_player,use_column_width=True)
    col2.header(player)
    col2.text(year)
    col2.text(f'Age : {int(player_selected["age"].to_list()[0])}')
    col2.text(f'Valeur : {int(player_selected["value"].to_list()[0])}')
    col3.text('')
    # c3.image(flag_player,width=40)
    col3.text(f'Matchs joués cette saison : {int(player_selected["MP"].to_list()[0])}')
    col3.text(f'Buts : {int(player_selected["goals"].to_list()[0])}')
    col3.text(f'Passes décisives : {int(player_selected["assists"].to_list()[0])}')

    output_df = pd.DataFrame()

    with output_graphs:
        st.title('Joueurs suggérés:')
        for key, value in response.items():
            for id,player in value.items():
                output_df.loc[id,key] = player

        st.table(output_df)

        col_list = st.columns(5)
        i = 0
        for col in col_list:
            player_found = df[df['player_name']==output_df['player_name'][i]].loc[df['season_year']=='2020-21',:]
            col.header(output_df['player_name'][i])
            # col.image(a compléter)
            # col.text(f'Ligue :{player_found['squad'].tolist()[0])


            i+=1


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
