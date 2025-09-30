
#  src/config.py


import os
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv

# Load local .env if running locally
load_dotenv()

# For Streamlit Cloud, use secrets
SUPABASE_URL = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
