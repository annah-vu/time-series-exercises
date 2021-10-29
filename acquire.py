import pandas as pd
import os
import requests

def new_items():
    '''
    returns dataframe of all items
    '''
    items_list = []

    response = requests.get('https://python.zach.lol/api/v1/items')
    data = response.json()
    n = data['payload']['max_page']

    for i in range(1,n+1):
        url = 'https://python.zach.lol/api/v1/items?page='+str(i)
        response = requests.get(url)
        data = response.json()
        page_items = data['payload']['items']
        items_list += page_items
        
    return pd.DataFrame(items_list)
    

def get_items():
    '''
    returns dataframe of all items from items.csv, or creates items.csv for you
    '''
    if os.path.isfile('items.csv'):
        df = pd.read_csv('items.csv')
    else:
        df = new_items()
        df.to_csv('items.csv', index=False)
        
    return df


def new_stores():
    '''
    returns dataframe of stores
    '''
    stores_list = []
    url = 'https://python.zach.lol/api/v1/stores'
    response = requests.get(url)
    data = response.json()
    n = data['payload']['max_page']

    for i in range(1,n+1):
        store_url = url + '?page=' +str(i)
        response = requests.get(store_url)
        data = response.json()
        page_store = data['payload']['stores']
        stores_list += page_store
        
    return pd.DataFrame(stores_list)
    

def get_stores():
    '''
    returns dataframe of stores from stores.csv, or creates it for you
    '''
    if os.path.isfile('stores.csv'):
        df = pd.read_csv('stores.csv')
    else:
        df = new_stores()
        df.to_csv('stores.csv', index=False)
        
    return df


def get_sales():
    '''
    retrieves sales dataframe from sales.csv, or creates it for you
    '''
    if os.path.isfile('sales.csv'):
        df = pd.read_csv('sales.csv')
        return df
    
    else: 
        sales_list = []
        url = 'https://python.zach.lol/api/v1/sales'
        response = requests.get(url)
        data = response.json()
        n = data['payload']['max_page']

        for i in range(1,n+1):
    
            sales_url = url + '?page=' +str(i)
            response = requests.get(sales_url)
            data = response.json()
            page_sales = data['payload']['sales']
            sales_list += page_sales
            df = pd.DataFrame(sales_list)
            df.to_csv('sales.csv', index=False)
    return df 
            

def combined_data():
    '''
    combines items, stores, and sales into a dataframe
    '''
    if os.path.isfile('combined.csv'):
        df = pd.read_csv('combined.csv')
        return df
    
    else: 
        items = get_items()
        stores = get_stores()
        sales = get_sales()
        
        sales = sales.rename(columns={'item':'item_id'})
        sales = sales.rename(columns={'store':'store_id'})
        combine_data = sales.merge(stores, on='store_id', how='left')
        combine_data = combine_data.merge(items, on='item_id', how='left')
        
        combine_data.to_csv('combined.csv', index=False)
        return combine_data
        
        
def get_germany_power():
    '''
    returns Germany power data into a csv, and creates it for you
    '''
    if os.path.isfile('germany_power.csv'):
        df = pd.read_csv('germany_power.csv')
        return df
    else:
        
        data = pd.read_csv("https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv")
        data.to_csv('germany_power.csv')
    return data

def combine_store_data():
    df = combined_data()
    df = df.drop(columns=['item_upc14'])
    df = df.rename(columns={"item_upc12": "item_upc"})
    return df