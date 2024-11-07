import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set up Streamlit page configuration
st.set_page_config(page_title="Interactive HR Dashboard", layout="wide")

# Load CSS file
with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

# Load dataset
df = pd.read_csv('HRDataset_v14.csv')

# Sidebar for filtering
st.sidebar.header("Filter Options")
department = st.sidebar.selectbox("Select Department", options=["All"] + list(df['Department'].unique()))
filtered_df = df if department == "All" else df[df['Department'] == department]

# Layout with two columns: left for controls, right for displaying data
left_col, right_col = st.columns([1, 3])

# Left column content
with left_col:
    st.sidebar.header("Dashboard Options")
    show_gender = st.sidebar.checkbox("Show Employees by Gender")
    show_state = st.sidebar.checkbox("Show Employees by State")
    show_position = st.sidebar.checkbox("Show Employees by Position")
    show_department = st.sidebar.checkbox("Show Employees by Department")
    show_salary_benchmark = st.sidebar.checkbox("Show Average Salary by Position")
    show_absences = st.sidebar.checkbox("Show Top 10 Absences")
    show_data_table = st.sidebar.checkbox("Show Data Table for Selected Department")

# Right column content for visualizations and data
with right_col:
    st.title("Interactive HR Dashboard")

    # Visualization 1: Doughnut Chart - Employees by Gender
    if show_gender:
        fig_gender = px.pie(filtered_df, names='Sex', title='Distribution of Employees by Gender', hole=0.4)
        st.plotly_chart(fig_gender, use_container_width=True)

    # Visualization 2: Geographic Map - Employees by State
    if show_state:
        state_counts = filtered_df['State'].value_counts().reset_index()
        state_counts.columns = ['State', 'Count']
        fig_state = px.choropleth(
            state_counts, locations='State', locationmode="USA-states",
            scope="usa", title="Employee Distribution by State",
            color='Count', color_continuous_scale="Viridis"
        )
        fig_state.update_layout(height=600, width=1200, title_x=0.5)
        st.plotly_chart(fig_state, use_container_width=True)

    # Visualization 3: Bar Chart - Employees by Position
    if show_position:
        position_counts = filtered_df['Position'].value_counts().reset_index()
        position_counts.columns = ['Position', 'Count']
        fig_position = px.bar(position_counts, x='Position', y='Count', title='Employee Count by Position')
        st.plotly_chart(fig_position, use_container_width=True)

    # Visualization 4: Bar Chart - Employees by Department
    if show_department:
        department_counts = filtered_df['Department'].value_counts().reset_index()
        department_counts.columns = ['Department', 'Count']
        fig_department = px.bar(department_counts, x='Department', y='Count', title='Employee Count by Department')
        st.plotly_chart(fig_department, use_container_width=True)

    # Visualization 5: Average Salary by Position with Benchmark Line
    if show_salary_benchmark:
        avg_salary_position = filtered_df.groupby('Position')['Salary'].mean().reset_index()
        avg_salary_position.columns = ['Position', 'Average Salary']
        fig_salary = px.bar(avg_salary_position, x='Position', y='Average Salary', title='Average Salary by Position')
        overall_avg_salary = df['Salary'].mean()
        fig_salary.add_hline(y=overall_avg_salary, line_dash="dash", line_color="red", 
                             annotation_text="Overall Average Salary", annotation_position="top left")
        st.plotly_chart(fig_salary, use_container_width=True)

    # Visualization 6: Top 10 Absences in a Bar Chart
    if show_absences:
        absences_top10 = filtered_df.nlargest(10, 'Absences')[['Employee_Name', 'Absences']]
        fig_absences = px.bar(absences_top10, x='Employee_Name', y='Absences', title='Top 10 Absences')
        st.plotly_chart(fig_absences, use_container_width=True)

    # Interactive Data Table
    if show_data_table:
        st.subheader(f"Data Table for Department: {department}")
        st.dataframe(filtered_df)

    # Download Data
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Filtered Data as CSV", data=csv, file_name='filtered_data.csv', mime='text/csv')
