import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load CSS file
with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

# Load dataset
df = pd.read_csv('HRDataset_v14.csv')

# Set up Streamlit page
st.set_page_config(page_title="Interactive HR Dashboard", layout="wide")

# Dashboard title
st.title("Interactive HR Dashboard")
st.sidebar.header("Filter Options")

# Summary metrics
st.markdown("## Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Employees", len(df))
col2.metric("Average Salary", f"${df['Salary'].mean():,.2f}")
col3.metric("Departments", df['Department'].nunique())

# Filter by Department
department = st.sidebar.selectbox("Select Department", options=["All"] + list(df['Department'].unique()))
filtered_df = df if department == "All" else df[df['Department'] == department]

# Visualization 1: Doughnut Chart - Employees by Gender
if st.sidebar.checkbox("Show Employees by Gender"):
    fig_gender = px.pie(filtered_df, names='Sex', title='Distribution of Employees by Gender', hole=0.4)
    st.plotly_chart(fig_gender)

# Visualization 2: Geographic Map - Employees by State
if st.sidebar.checkbox("Show Employees by State"):
    state_counts = filtered_df['State'].value_counts().reset_index()
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
    position_counts = filtered_df['Position'].value_counts().reset_index()
    position_counts.columns = ['Position', 'Count']
    fig_position = px.bar(position_counts, x='Position', y='Count', title='Employee Count by Position')
    st.plotly_chart(fig_position)

# Visualization 4: Bar Chart - Employees by Department
if st.sidebar.checkbox("Show Employees by Department"):
    department_counts = filtered_df['Department'].value_counts().reset_index()
    department_counts.columns = ['Department', 'Count']
    fig_department = px.bar(department_counts, x='Department', y='Count', title='Employee Count by Department')
    st.plotly_chart(fig_department)

# Visualization 5: Average Salary by Position with Benchmark Line
if st.sidebar.checkbox("Show Average Salary by Position"):
    avg_salary_position = filtered_df.groupby('Position')['Salary'].mean().reset_index()
    avg_salary_position.columns = ['Position', 'Average Salary']
    fig_salary = px.bar(avg_salary_position, x='Position', y='Average Salary', title='Average Salary by Position')
    overall_avg_salary = df['Salary'].mean()
    fig_salary.add_hline(y=overall_avg_salary, line_dash="dash", line_color="red", 
                         annotation_text="Overall Average Salary", annotation_position="top left")
    st.plotly_chart(fig_salary)

# Visualization 6: Top 10 Absences in a Bar Chart
if st.sidebar.checkbox("Show Top 10 Absences"):
    absences_top10 = filtered_df.nlargest(10, 'Absences')[['Employee_Name', 'Absences']]
    fig_absences = px.bar(absences_top10, x='Employee_Name', y='Absences', title='Top 10 Absences')
    st.plotly_chart(fig_absences)

# Interactive Data Table
if st.sidebar.checkbox("Show Data Table for Selected Department"):
    st.dataframe(filtered_df)

# Download Data
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Filtered Data as CSV", data=csv, file_name='filtered_data.csv', mime='text/csv')
