from urllib.error import URLError

import altair as alt    #import der versch. libaries
import pandas as pd     #geben eines kürzels, für späteren zugriff
import streamlit as st

#die daten aus der csv datei werden importiert und mit einer variable versehen. Hier "df" 
#Pandas Funktion -> Read -> Trennungszeichen festlegen (sep="..") 
@st.cache_data
def get_data():     # 'def' ist eine definition
    df = pd.read_csv(
        "https://opendata.luebeck.de/bereich/1.102/statistik/bevoelkerung/"
        "einwohner-stadtteile/einwohner-stadtteile.csv",
        sep=";",
    )
#Umwandlung der Textfelder einerseits in Datum, andererseits in eine einfache Zahl
    df = df.set_index("stadtteil_name")
    df["stichtag"] = pd.to_datetime(df["stichtag"])
    df["einwohner"] = pd.to_numeric(df["einwohner"])
    return df


try:
    df = get_data()

    stadtteile = st.multiselect(
        label="Wähle Stadtteile",
        options=list(df.index.unique()),
        default=["Innenstadt"],
    )

    if not stadtteile:
        st.error("Wähle mindestens einen Stadtteil, du Hund!")
    else:
        df = df.loc[stadtteile]     #Hier wird gefiltert 
        df = df.reset_index()

        chart = (
            alt.Chart(df)
            .mark_line()
            .encode(
                x=alt.X("stichtag", title="Stichtag"),
                y=alt.Y("einwohner", title="Einwohner"),
                color=alt.Color("stadtteil_name", title="Stadtteil"),
            )
        )

        st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(f"Daten konnten nicht geladen werden: {e.reason}")
