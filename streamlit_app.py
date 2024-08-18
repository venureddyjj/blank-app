import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

def search_and_extract_table(stixeye_attack_capec, search_word):
    # Apply a mask to find rows containing the search word
    mask = stixeye_attack_capec.apply(lambda x: x.astype(str).str.contains(search_word, case=False)).any(axis=1)
    count = mask.sum()  # Count the number of matching rows

    # Extract the matching rows
    search_rows = stixeye_attack_capec[mask]
    search_capec_execution_flow_attack = pd.DataFrame(search_rows['x_capec_execution_flow'])

    # Function to extract table from HTML string
    def extract_table(html_str):
        if pd.isna(html_str):  # Check if the value is NaN
            return ''
        soup = BeautifulSoup(html_str, 'html.parser')
        table = soup.find('table')
        return str(table)

    # Apply the extract_table function to the 'x_capec_execution_flow' column
    search_capec_execution_flow_attack['x_capec_execution_flow_table'] = search_capec_execution_flow_attack['x_capec_execution_flow'].apply(extract_table)

    return search_capec_execution_flow_attack, count

# Streamlit app
def main():
    st.title("Search and Extract Tables from DataFrame")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        stixeye_attack_capec = pd.read_csv(uploaded_file)

        # Search word input
        search_word = st.text_input("Enter the search word")

        if search_word:
            # Perform search and extract tables
            search_capec_execution_flow_attack, count = search_and_extract_table(stixeye_attack_capec, search_word)

            # Display the results
            st.write(f"Number of matching rows: {count}")
            
            # Display the extracted tables
            for index, row in search_capec_execution_flow_attack.iterrows():
                st.markdown(f"### Row {index}")
                st.markdown(row['x_capec_execution_flow_table'], unsafe_allow_html=True)

if __name__ == "__main__":
    main()
