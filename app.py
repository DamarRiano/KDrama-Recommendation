import streamlit as st
import pickle
import pandas as pd
import requests

kdramas_list = pickle.load(open('kdramas_dict.pkl', 'rb'))
kdramas = pd.DataFrame(kdramas_list)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.set_page_config(layout="wide")
def fetch_poster_page(kdrama_id):
    response = requests.get(
        'https://api.themoviedb.org/3/tv/{}?api_key=d8968ab0457bc4f68c4f5fc9af6ec500&language=en-US'.format(kdrama_id))
    data = response.json()
    print(data)

    if 'poster_path' in data and data['poster_path'] is not None:
        poster_url = "https://image.tmdb.org/t/p/original" + data['poster_path']
    else:
        poster_url = "no-poster.jpg"

    if 'homepage' in data and data['homepage'] is not None:
        homepage_url = data['homepage']
    else:
        homepage_url = "no-poster.jpg"

    return poster_url, homepage_url


def recommend(kdrama_selected):
    kd_index = kdramas[kdramas['title'] == kdrama_selected].index
    if len(kd_index) == 0:
        st.error("Kdrama not found!")
        return [], [], []

    kd_index = kd_index[0]
    if kd_index >= len(similarity):
        st.error("Invalid kdrama index!")
        return [], [], []

    distances = similarity[kd_index]
    kd_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_kdramas = []
    recommend_kdramas_poster = []
    recommend_kdramas_homepage = []
    for i in kd_list:
        kdrama_id = kdramas.iloc[i[0]].id
        recommend_kdramas.append(kdramas.iloc[i[0]].title)
        poster, homepage = fetch_poster_page(kdrama_id)
        recommend_kdramas_poster.append(poster)
        recommend_kdramas_homepage.append(homepage)
    return recommend_kdramas, recommend_kdramas_poster, recommend_kdramas_homepage


st.title('KFlix')
kdrama_selected = st.selectbox(
    'Select a Kdrama you have watched', kdramas['title'])

if st.button('Recommend'):
    names,posters,homepage = recommend(kdrama_selected)

    # Create two columns
    col1, col2, col3,col4,col5 = st.columns(5)

    # In col1, display the image with a URL
    with col1:
        st.text(names[0])
        if homepage[0] is not None and posters[0] is not None:
            st.markdown('<a href="'+homepage[0]+'"><img src="'+posters[0]+'" width="200" ></a>', unsafe_allow_html=True)

    # In col2, display the image with a URL
    with col2:
        st.text(names[1])
        if homepage[1] is not None and posters[1] is not None:
            st.markdown('<a href="'+homepage[1]+'"><img src="'+posters[1]+'" width="200" ></a>', unsafe_allow_html=True)

    # In col3, display the image with a URL
    with col3:
        st.text(names[2])
        if homepage[2] is not None and posters[2] is not None:
            st.markdown('<a href="'+homepage[2]+'"><img src="'+posters[2]+'" width="200" ></a>', unsafe_allow_html=True)
        
    # In col4, display the image with a URL
    with col4:
        st.text(names[3])
        if homepage[3] is not None and posters[3] is not None:
            st.markdown('<a href="'+homepage[3]+'"><img src="'+posters[3]+'" width="200" ></a>', unsafe_allow_html=True)
        
    # In col5, display the image with a URL
    with col5:
        st.text(names[4])
        if homepage[4] is not None and posters[4] is not None:
            st.markdown('<a href="'+homepage[4]+'"><img src="'+posters[4]+'" width="200" ></a>', unsafe_allow_html=True)
        