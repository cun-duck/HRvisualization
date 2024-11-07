import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv('HRDataset_v14.csv')

# Set up Streamlit page
st.set_page_config(page_title="HR Dashboard", layout="wide")

st.title("HR Dashboard")
st.sidebar.header("Select Visualization")

# Visualization 1: Doughnut Chart - Employees by Gender
if st.sidebar.checkbox("Show Employees by Gender"):
    fig_gender = px.pie(df, names='Sex', title='Distribution of Employees by Gender', hole=0.4)
    st.plotly_chart(fig_gender)

# Visualization 2: Geographic Map - Employees by State
if st.sidebar.checkbox("Show Employees by State"):
    state_counts = df['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Count']
    fig_state = px.choropleth(
        state_counts, locations='State', locationmode="USA-states",
        scope="usa", title="Employee Distribution by State",
        color='Count', color_continuous_scale="Viridis"
    )
    fig_state.update_layout(height=600, width=1200, title_x=0.5)
    st.plotly_chart(fig_state)

# Visualization 3: Bar Chart - Employees by Position
if st.sidebar.checkbox("Show Employees by Position"):
    fig_position = px.bar(df, x=df['Position'].value_counts().index,
                          y=df['Position'].value_counts().values,
                          title='Employee Count by Position')
    st.plotly_chart(fig_position)

# Add other visualizations similarly
