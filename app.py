import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state
if 'cases' not in st.session_state:
    st.session_state.cases = []
    st.session_state.case_id_counter = 1

st.title('Litigation WIP Management System')

# Sidebar for adding new cases
st.sidebar.header('Add New Case')
task_subject = st.sidebar.text_input('Task/Subject')
responsible_persons = st.sidebar.text_input('Responsible Persons')
deadline = st.sidebar.date_input('Deadline')
status_notes = st.sidebar.text_area('Status/Notes')

if st.sidebar.button('Add Case'):
    new_case = {
        'id': st.session_state.case_id_counter,
        'task_subject': task_subject,
        'responsible_persons': responsible_persons,
        'deadline': str(deadline),
        'status_notes': status_notes
    }
    st.session_state.cases.append(new_case)
    st.session_state.case_id_counter += 1
    st.sidebar.success('Case added successfully!')

# Main area for displaying and managing cases
df = pd.DataFrame(st.session_state.cases)

st.subheader('Current Cases')
st.dataframe(df)

# Edit and Delete functionality
st.subheader('Edit or Delete Case')
case_id = st.number_input('Enter Case ID to Edit/Delete', min_value=1, step=1)
action = st.radio('Choose Action', ['Edit', 'Delete'])

if action == 'Edit':
    case = next((case for case in st.session_state.cases if case['id'] == case_id), None)
    if case:
        task_subject = st.text_input('New Task/Subject', case['task_subject'])
        responsible_persons = st.text_input('New Responsible Persons', case['responsible_persons'])
        deadline = st.date_input('New Deadline', datetime.strptime(case['deadline'], '%Y-%m-%d').date())
        status_notes = st.text_area('New Status/Notes', case['status_notes'])
        
        if st.button('Update Case'):
            case.update({
                'task_subject': task_subject,
                'responsible_persons': responsible_persons,
                'deadline': str(deadline),
                'status_notes': status_notes
            })
            st.success('Case updated successfully!')
            st.experimental_rerun()
    else:
        st.warning('Case not found')

elif action == 'Delete':
    if st.button('Delete Case'):
        st.session_state.cases = [case for case in st.session_state.cases if case['id'] != case_id]
        st.success('Case deleted successfully!')
        st.experimental_rerun()
