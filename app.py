import streamlit as st
import plotly.express as px
import pandas as pd

# Set page config at the start
st.set_page_config(page_title="Interactive HR Dashboard", layout="wide")

# Load Data
df = pd.read_csv("HRDataset_v14.csv")

# CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Layout settings
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Sidebar section
with st.sidebar:
    st.header("Select Dimensions")
    gender_option = st.checkbox("Gender Distribution")
    state_option = st.checkbox("State Distribution")
    # Additional sidebar options as needed

# Content section
with st.container():
    if gender_option:
        fig_gender = px.pie(df, names="Sex", title="Employees by Gender", hole=0.4)
        st.plotly_chart(fig_gender, use_container_width=True)

    if state_option:
        fig_state = px.choropleth(df, locations="State", locationmode="USA-states", color="State",
                                  scope="usa", title="Employees by State")
        st.plotly_chart(fig_state, use_container_width=True)

# Close the main container div
st.markdown('</div>', unsafe_allow_html=True)
