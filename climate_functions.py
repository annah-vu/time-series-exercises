import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from math import sqrt
from sklearn.metrics import mean_squared_error


def get_temp_data():
    '''
    bring in global land temperatures by major city
    '''
    df = pd.read_csv('GlobalLandTemperaturesByMajorCity.csv')
    return df

def prepare_temp_data(df):
    df['dt'] = pd.to_datetime(df.dt)
    df = df.loc[df['City'] == 'Chicago']
    df = df.interpolate(method='linear')
    df = df.rename(columns={'dt':'date','AverageTemperature':'avg_temp','City':'city','Country':'country'})
    df = df.set_index('date')
    df['year']= df.index.year
    df['month']= df.index.month
    df = df.loc['1900':'2013']
    return df
    
    
def evaluate(target_var):
    '''
    This function will take the actual values of the target_var from validate, 
    and the predicted values stored in yhat_df, 
    and compute the rmse, rounding to 0 decimal places. 
    it will return the rmse. 
    '''
    rmse = round(sqrt(mean_squared_error(validate[target_var], yhat_df[target_var])), 0)
    return rmse


def plot_and_eval(target_var):
    '''
    This function takes in the target var name (string), and returns a plot
    of the values of train for that variable, validate, and the predicted values from yhat_df. 
    it will als lable the rmse. 
    '''
    plt.figure(figsize = (12,4))
    plt.plot(train[target_var], label='Train', linewidth=1)
    plt.plot(validate[target_var], label='Validate', linewidth=1)
    plt.plot(yhat_df[target_var])
    plt.title(target_var)
    rmse = evaluate(target_var)
    print(target_var, '-- RMSE: {:.0f}'.format(rmse))
    plt.show()
    
def append_eval_df(model_type, target_var):
    '''
    this function takes in as arguments the type of model run, and the name of the target variable. 
    It returns the eval_df with the rmse appended to it for that model and target_var. 
    '''
    rmse = evaluate(target_var)
    d = {'model_type': [model_type], 'target_var': [target_var],
        'rmse': [rmse]}
    d = pd.DataFrame(d)
    return eval_df.append(d, ignore_index = True)