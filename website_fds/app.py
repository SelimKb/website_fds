from urllib import response
import pandas as pd
import requests
import streamlit as st
import io

# from PIL import Image

from website_fds.params import BUCKET_NAME, CLEAN_DATA_STORAGE_LOCATION

from DS_similar_to.knn_players import KnnPlayers



url = 'https://footballscouting-qpmhphei7q-ew.a.run.app/get_close_players'

header = st.container()
user_input = st.container()
output_graphs = st.container()
other_players = st.container()
author_credits = st.container()


with header:
    st.title("Bienvenue sur la page du projet Deep Scouting")
    st.markdown("""
    #### Par: [Selim Kebaier](https://www.linkedin.com/in/selim-kebaier-7b009073/) et [Morgan Godard](https://www.linkedin.com/in/morgan-godard-97aa1a194/)


    Cette application web présente les 5 joueurs les plus proches, en terme de statistiques de jeu réels, d'un joueur sélectionné par l'utilisateur.

    """)

#df = pd.read_csv(f'gs://{BUCKET_NAME}/{CLEAN_DATA_STORAGE_LOCATION}players_streamlit.csv')
df = pd.read_csv("website_fds/data/players_streamlit.csv")
df_secours = pd.read_csv("website_fds/data/players_base.csv")
#df_secours = pd.read_csv(
#    f'gs://{BUCKET_NAME}/{CLEAN_DATA_STORAGE_LOCATION}players_base.csv')

with user_input:
    st.sidebar.header('Choix du joueur')

    # Generating the list for states
    trad_post = {"Attaquant":"Forward","Défenseur":"Defender", "Milieu":"Midfield"}
    years_list = []
    trad_leagues = {
        "Première League (Angleterre)": "English Premier League",
        "Ligue 1 (France)": "French Ligue 1",
        "Bundesliga (Allemagne)": "German 1. Bundesliga",
        "Liga (Espagne)": "Spain Primera Division",
        "Serie A (Italie)":"Italian Serie A"
        }

    squads_list =[]


    position = st.sidebar.selectbox('Choisis un poste :',

                                 trad_post.keys())
    position =trad_post[position]


    if position.lower() == "defender":
        df_pos=df[df['is_df']==1].copy()
    elif position.lower() =="forward":
        df_pos= df[df['is_fw'] == 1].copy()
    elif position.lower() =="midfield":
        df_pos= df[df['is_mf'] == 1].copy()

    years_list = df_pos.season_year.unique()
    years_list.sort()

    year = st.sidebar.selectbox(
        'Choisis une saison :', years_list)  # We define the season variable

    df_pos=df_pos[df_pos["season_year"]==year]

    leagues_list = df_pos.new_league_name.unique()
    leagues_list.sort()


    league = st.sidebar.selectbox('Choisis une ligue :',

                                trad_leagues.keys())  # We define the county variable


    league=trad_leagues[league]

    df_pos=df_pos[df_pos["new_league_name"]==league]

    squads_list = df_pos.squad.unique()
    squads_list.sort()


    squad = st.sidebar.selectbox('Choisis une équipe :',
                                squads_list)  # We define the squad variable

    df_pos=df_pos[df_pos["squad"]==squad]

    players_list = df_pos.player_name.unique()
    players_list.sort()


    player = st.sidebar.selectbox("Et enfin, le joueur dont le profil t'intéresse :",
                                players_list)  # We define the player variable



    # Summary Table
if st.sidebar.button("Who's the MPG king now?"):
    with output_graphs:
        # print is visible in the server output, not in the page
        st.title("Profil recherché :")
        df_player=df[df["player_name"]==player].copy()
        df_player = df_player[df_player["season_year"]==year]
        image_player=df_player["photo"].tolist()
        image_flag=df_player["flag"].tolist()
        req = requests.get(image_player[0])
        image_player = io.BytesIO(req.content)
        req = requests.get(image_flag[0])
        image_flag = io.BytesIO(req.content)
        age=df_player["age"].tolist()[0]
        MP=df_player["MP"].tolist()[0]
        goals = int(df_player["goals"].tolist()[0])

        col1, col2, col3 = st.columns((1,2,2))

        col1.image(image_player,use_column_width=True)
        col2.header(player)
        col2.markdown(f"<h4 style='text-align: left; color: black;font-size:15px'>En {year} :</h4>", unsafe_allow_html=True)
        col2.text('')
        col2.text(f'Age : {int(df_player["age"].to_list()[0])}')
        if df_player["value"].tolist()[0]==-1:
            col2.text(f'Valeur : Non disponible')
        else:
            col2.text(f'Valeur : {df_player["value"].to_list()[0]/1000_000} M€')

        col3.text('')
        col3.image(image_flag,width=40)
        col3.text(f'Matchs joués : {int(df_player["MP"].to_list()[0])}')
        col3.text(f'Buts : {int(df_player["goals"].to_list()[0])}')
        col3.text(f'Passes décisives : {int(df_player["assists"].to_list()[0])}')

    with other_players:

        st.title("Joueurs suggérés :")
        #params = {'position': position, 'player_name': player, 'season_year': year}
        #response = requests.get(url, params).json()
        response = KnnPlayers(position).predict(player_name=player, season=year)

        output_df = pd.DataFrame()
        for key, value in response.items():
            for id, joueur in value.items():
                output_df.loc[id, key] = joueur


        image_list=[]
        flag_list=[]
        for i in output_df["player_name"]:
            # if i in df[df["season_year"]=="2020-21"]["player_name"].tolist():
            df_player=df[df["player_name"]==i].copy()
            df_player = df_player[df_player["season_year"]=="2020-21"]
            if df_player['photo'].tolist()==[]:
                req_p = requests.get(
                    "https://cdn.sofifa.com/players/notfound_0_60.png")
                req_f = requests.get(
                    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Olympic_flag.svg/1920px-Olympic_flag.svg.png"
                )
            else:
                img_p=df_player["photo"].tolist()
                img_f=df_player["flag"].tolist()
                req_p = requests.get(img_p[0])
                req_f = requests.get(img_f[0])

            image_list.append(io.BytesIO(req_p.content))
            flag_list.append(io.BytesIO(req_f.content))

        list_contain=[]
        for i in range(5):
            list_contain.append(st.container())
            with list_contain[i]:
                c1,c2,c3 = st.columns((1, 2, 2))
                c1.image(image_list[i],use_column_width=True)
                c2.header(output_df["player_name"].iloc[i])
                c2.markdown(f"<h4 style='text-align: left; color: black;font-size:15px'>En 2020-21 :</h4>", unsafe_allow_html=True)
                c2.text('')

                if output_df['player_name'].iloc[i] in df.loc[
                        df['season_year'] ==
                        '2020-21',:]["player_name"].tolist():
                    player_found = df[df['player_name']==output_df['player_name'].iloc[i]].loc[df['season_year']=='2020-21',:]
                    c2.text(f'Age : {int(player_found["age"].to_list()[0])}')
                    c2.text(f'Equipe : {player_found["squad"].tolist()[0]}')

                    c3.text('')
                    c3.image(flag_list[i],width=40)
                    c3.text(
                        f'Matchs joués : {int(player_found["MP"].to_list()[0])}'
                    )
                    c3.text(f'Buts : {int(player_found["goals"].to_list()[0])}')
                    c3.text(
                        f'Passes décisives : {int(player_found["assists"].to_list()[0])}'
                    )
                    c3.text(
                        f'Valeur : {player_found["value"].to_list()[0]/1000_000} M€')

                else:
                    player_found = df_secours[df_secours['player_name'] ==
                                      output_df['player_name'].iloc[i]].loc[
                                          df_secours['season_year'] == '2020-21', :]
                    c2.text(f'Age : {int(player_found["age"].to_list()[0])}')
                    c2.text(f'Equipe : {player_found["squad"].tolist()[0]}')

                    c3.text('')
                    c3.image(flag_list[i],width=40)
                    c3.text(
                        f'Matchs joués : {int(player_found["MP"].to_list()[0])}'
                    )
                    c3.text(
                        f'Buts : {int(player_found["goals"].to_list()[0])}')
                    c3.text(
                        f'Passes décisives : {int(player_found["assists"].to_list()[0])}'
                    )
                    c3.text(f'Valeur : Non disponible')








    # col5.image(image_list[1], use_column_width=True)
    # col6.image(image_list[2], use_column_width=True)
    # col7.image(image_list[3], use_column_width=True)
    # col8.image(image_list[4], use_column_width=True)
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

with author_credits:
    st.header(f'Credits')
    st.markdown("""
    **Thank you for using our application!**

    The datasets used to feed this application are provided by [FBref](https://fbref.com/en/) and [sofifa](https://sofifa.com/).\n
    This application uses the Streamlit package library.
    """)
