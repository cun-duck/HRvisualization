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
    position_counts = df['Position'].value_counts().reset_index()
    position_counts.columns = ['Position', 'Count']
    fig_position = px.bar(position_counts, x='Position', y='Count', title='Employee Count by Position')
    st.plotly_chart(fig_position)

# Visualization 4: Bar Chart - Employees by Department
if st.sidebar.checkbox("Show Employees by Department"):
    department_counts = df['Department'].value_counts().reset_index()
    department_counts.columns = ['Department', 'Count']
    fig_department = px.bar(department_counts, x='Department', y='Count', title='Employee Count by Department')
    st.plotly_chart(fig_department)

# Visualization 5: Average Salary by Position with Benchmark Line
if st.sidebar.checkbox("Show Average Salary by Position"):
    # Menghitung rata-rata gaji per posisi
    avg_salary_position = df.groupby('Position')['Salary'].mean().reset_index()
    avg_salary_position.columns = ['Position', 'Average Salary']
    
    # Membuat bar chart dengan rata-rata gaji per posisi
    fig_salary = px.bar(avg_salary_position, x='Position', y='Average Salary', title='Average Salary by Position')
    
    # Menghitung rata-rata gaji keseluruhan untuk dijadikan garis benchmark
    overall_avg_salary = df['Salary'].mean()
    
    # Menambahkan garis benchmark ke grafik
    fig_salary.add_hline(y=overall_avg_salary, line_dash="dash", line_color="red", 
                         annotation_text="Overall Average Salary", annotation_position="top left")
    
    st.plotly_chart(fig_salary)

# Visualization 6: Top 10 Absences in a Bar Chart
if st.sidebar.checkbox("Show Top 10 Absences"):
    absences_top10 = df.nlargest(10, 'Absences')[['Employee_Name', 'Absences']]
    fig_absences = px.bar(absences_top10, x='Employee_Name', y='Absences', title='Top 10 Absences')
    st.plotly_chart(fig_absences)
