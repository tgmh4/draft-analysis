import requests
import streamlit as st

@st.cache_data
def get_match_data(match_id):
    url = f"https://api.opendota.com/api/matches/{match_id}"
    return requests.get(url).json()

@st.cache_data
def get_hero_stats():
    url = "https://api.opendota.com/api/heroes"
    return {hero['id']: hero for hero in requests.get(url).json()}


# url = "https://api.opendota.com/api/herostats"