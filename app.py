import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import os

# Auth0 Credentials (Replace with your Auth0 App details)
AUTH0_DOMAIN = "dev-jyu3bfhckum44bfk.eu.auth0.com"
CLIENT_ID = "yTs0oQV1FHv8z2gK9z10qtCVOxY8LtNE"
CLIENT_SECRET = "tZiFo00tHzZvf6wgcwC198UTC_x2vLg3_VeEmB3mnjqK0QqGgQywMWEkkEVMif72"
REDIRECT_URI = "https://vergiasistan--test-eoi7uvyjszyxkn4fzwdkwr.streamlit.app/"

# Auth0 Endpoints
AUTHORIZATION_URL = f"https://{AUTH0_DOMAIN}/authorize"
TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
USER_INFO_URL = f"https://{AUTH0_DOMAIN}/userinfo"

# Initialize OAuth2 session
oauth = OAuth2Session(
    CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope="openid profile email"
)

def login():
    authorization_url, state = oauth.create_authorization_url(AUTHORIZATION_URL)
    st.markdown(f'<a href="{authorization_url}" target="_self">Login with Auth0</a>', unsafe_allow_html=True)

def logout():
    st.session_state.pop("user_info", None)
    st.experimental_rerun()

def callback():
    params = st.query_params.to_dict()
    if "code" in params:
        token = oauth.fetch_token(TOKEN_URL, authorization_response=REDIRECT_URI, client_secret=CLIENT_SECRET)
        user_info = oauth.get(USER_INFO_URL).json()
        st.session_state["user_info"] = user_info
        st.experimental_rerun()

if "user_info" not in st.session_state:
    if "code" not in st.query_params:
        login()
    else:
        callback()
else:
    st.success(f"Welcome, {st.session_state['user_info']['name']}!")
    st.image(st.session_state['user_info']['picture'])
    if st.button("Logout"):
        logout()
