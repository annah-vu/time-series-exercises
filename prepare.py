import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import datetime
import pandas as pd

def prep_combine(df):
    df.sale_date = pd.to_datetime(df.sale_date)
    df = df.set_index('sale_date').sort_index()
    df['month'] = df.index.month
    df['day_of_week'] = df.index.day_name()
    df['sales_total'] = df.sale_amount * df.item_price
    return df

def prep_opsd(df):
    df = df.drop(columns=['Unnamed: 0'])
    df.Date = pd.to_datetime(df.Date)
    df = df.set_index('Date')
    df['month']=df.index.month
    df['year']=df.index.year
    df = df.fillna(0)
    return df