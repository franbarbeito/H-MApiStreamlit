import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import numpy as np 

headers = {'Accept': 'application/json'}

api_url = "https://api-dot-tfg-bi.oa.r.appspot.com/api/v1/"
total_customers = "customers"
total_articles = "articles"
total_transactions = "transactions"

def set_api_key(api_key):
    headers = {'Accept': 'application/json', 'X-API-KEY': api_key}
    return headers

def make_request(main_url, service_url, api_key):
    headers = set_api_key(api_key)
    response = requests.get(f"{main_url}{service_url}", headers=headers)
    response_json = response.json()
    return response_json

def load_json_to_dataframe(response_json):
    target_json = response_json["result"]
    try:
        df = pd.json_normalize(target_json)
    except Exception as e:
        print(e)
    return df 

def load_data(api_url, service_url, api_key):
    headers = {'Accept': 'application/json', 'X-API-KEY': api_key}
    response = requests.get(f"{api_url}{service_url}", headers=headers)
    response_json = response.json()
    df = load_json_to_dataframe(response_json)
    return response_json, df

api_key = st.text_input('API key')


if st.button('Login'):
    try:
        response_json1, customers_df = load_data(api_url, total_customers, api_key)
        response_json2, articles_df = load_data(api_url, total_articles, api_key)
        response_json3, transaction_sample_df = load_data(api_url, total_transactions, api_key)
       

    except requests.exceptions.RequestException:
        st.error('Failed to connect to the API. Please check the API key and try again.')
    else:
        response_json1, customers_df = load_data(api_url, total_customers,api_key)
        response_json2, articles_df = load_data(api_url, total_articles,api_key)
        response_json3, transaction_sample_df = load_data(api_url, total_transactions,api_key)
       




       

        # Merge the data from the tables into a single DataFrame
        merged_df = pd.merge(transaction_sample_df, articles_df, on='article_id')

        merged_df = pd.merge(merged_df, customers_df, on='customer_id')
        print(merged_df)
        # Define the filters
        filter1 = st.sidebar.multiselect('Product Type', merged_df['product_type_name'].unique())
        filter2 = st.sidebar.multiselect('Department', merged_df['department_name'].unique())
        filter3 = st.sidebar.multiselect('Sales Channel', merged_df['sales_channel_id'].unique())
        filter4 = st.sidebar.multiselect('Customer Club Status', merged_df['club_member_status'].unique())

        # Apply the filters
        if filter1:
            merged_df = merged_df[merged_df['product_type_name'].isin(filter1)]
        if filter2:
            merged_df = merged_df[merged_df['department_name'].isin(filter2)]
        if filter3:
            merged_df = merged_df[merged_df['sales_channel_id'].isin(filter3)]
        if filter4:
            merged_df = merged_df[merged_df['club_member_status'].isin(filter4)]

        # Define the KPIs with filtered data
        kpi1 = transaction_sample_df['price'].sum()
        kpi2 = transaction_sample_df['price'].mean()
        kpi3 = transaction_sample_df['customer_id'].nunique()
        kpi4 = transaction_sample_df['article_id'].nunique()
        kpi5 = merged_df.groupby('product_type_name')['price'].sum().reset_index()
        kpi6 = merged_df.groupby('department_name')['price'].sum().reset_index()
        kpi7 = merged_df.groupby('sales_channel_id')['price'].sum().reset_index()
        kpi8 = merged_df.groupby('club_member_status')['price'].sum().reset_index()

        # Display the KPIs
        st.write('**KPI 1 - Total Revenue:** $', kpi1)
        st.write('**KPI 2 - Average Revenue per Transaction:** $', kpi2)
        st.write('**KPI 3 - Number of Unique Customers:**', kpi3)
        st.write('**KPI 4 - Number of Unique Products Sold:**', kpi4)

        # Display the new KPIs on graphs
        st.write('**KPI 5 - Total Revenue by Product Type:**')
        if not kpi5.empty:
            fig1 = st.bar_chart(kpi5.set_index('product_type_name'))
        else:
            st.write('No data available with selected filters.')

        st.write('**KPI 6 - Total Revenue by Department:**')
        if not kpi6.empty:
            fig2 = st.bar_chart(kpi6.set_index('department_name'))
        else:
            st.write('No data available with selected filters.')

        st.write('**KPI 7 - Total Revenue by Sales Channel:**')
        fig3 = px.pie(kpi7, values='price', names='sales_channel_id')
        st.plotly_chart(fig3)

        st.write('**KPI 8 - Total Revenue by Customer Club Status:**')
        fig4 = px.pie(kpi8, values='price', names='club_member_status')
        st.plotly_chart(fig4)


