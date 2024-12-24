import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

#============================================================= IMPORT FUNCTIONS

def df_import(folder_path, frac=0.5):
    
    train_path = folder_path + 'train.csv'
    eval_path = folder_path + 'test.csv'
    store_path = folder_path + 'store.csv'
            
    try:
        train = pd.read_csv(train_path).sample(frac=frac, random_state=42)
        eval_ = pd.read_csv(eval_path)
        store = pd.read_csv(store_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    
    train['train_eval'] = 'train'
    eval_['train_eval'] = 'eval'
    
    df = pd.concat([train,eval_])
    df = df.merge(store, how='left', on='Store')
    
    df.Date = pd.to_datetime(df.Date, format='%Y-%m-%d')
    
    category_columns = ['StoreType', 'Assortment', 'DayOfWeek', ]  # List of columns to convert
    
    for col in category_columns:
        df[col] = df[col].astype('category')
        
        
    bool_columns = ['Open', 'Promo', 'SchoolHoliday', 'Promo2' ]
    
    for col in bool_columns:
        df[col] = df[col].astype('bool')
    
    return df

#============================================================= MAIN FUNCTIONS


def nan_summary(df):
    nan_counts = {}
    for column in df.columns:
        total_values = df[column].size
        nan_count = df[column].isna().sum()
        nan_percentage = (nan_count / total_values) * 100 if total_values > 0 else 0
        nan_counts[column] = {'Count': nan_count, 'Percentage': nan_percentage}
    
    nan = pd.DataFrame(nan_counts).T
    return nan


def assign_competition_distance_category(df):
    # Create a new column 'cat_CompetitionDistance' initialized to NaN
    df['cat_CompetitionDistance'] = np.nan

    # Apply qcut for values less than 4000
    mask1 = df['CompetitionDistance'] < 4000
    df.loc[mask1, 'cat_CompetitionDistance'] = pd.qcut(df.loc[mask1, 'CompetitionDistance'], 
                                                         q=10, 
                                                         labels=False) + 1  # +1 to start deciles from 1

    # Assign 11 for values between 4000 and 20000
    mask2 = (df['CompetitionDistance'] >= 4000) & (df['CompetitionDistance'] <= 20000)
    df.loc[mask2, 'cat_CompetitionDistance'] = 11

    # Assign 12 for values greater than 20000
    mask3 = df['CompetitionDistance'] > 20000
    df.loc[mask3, 'cat_CompetitionDistance'] = 12

    return df


def process_competition_data(df):
    
    # Imputación de valor extremo
    df['CompetitionDistance'] = df['CompetitionDistance'].fillna(9999999)
    
    # Definición de condiciones de imputación a la nueva variable.
    df['CompetitionOpen'] = 0  
    condition_open_since_na = df['CompetitionOpenSinceYear'].isna() | df['CompetitionOpenSinceMonth'].isna()
    df.loc[condition_open_since_na, 'CompetitionOpen'] = 1
    df.loc[condition_open_since_na, 'CompetitionOpenSinceYear'] = 2013
    df.loc[condition_open_since_na, 'CompetitionOpenSinceMonth'] = 1

    condition_competition_open = (
        (df['Year'] == df['CompetitionOpenSinceYear']) & (df['Month'] >= df['CompetitionOpenSinceMonth']) |
        (df['Year'] > df['CompetitionOpenSinceYear'])
    )
    
    df.loc[condition_competition_open, 'CompetitionOpen'] = 1

    return df




def process_promo2_active(df):
    
    month_map = {'Jan': 1, 'Feb': 2, 'Mar': 3,
                 'Apr': 4, 'May': 5, 'Jun': 6,
                 'Jul': 7, 'Aug': 8, 'Sept': 9,
                 'Oct': 10, 'Nov': 11, 'Dec': 12}

    # Reemplazo numérico
    df['PromoInterval'] = df['PromoInterval'].apply(lambda x: x.split(',') if isinstance(x, str) else x)
    df['PromoInterval'] = df['PromoInterval'].apply(lambda lst: [month_map.get(elem, elem) for elem in lst] if isinstance(lst, list) else lst)

    # Imputación
    df['Promo2Active'] = np.nan
    for line in range(len(df)):
        # Si alguna variable es nula, aplico un valor extremo
        if pd.isna(df.loc[line, 'Promo2SinceYear']) or pd.isna(df.loc[line, 'Promo2SinceWeek']):
            df.loc[line, 'Promo2Active'] = 999
        # Si se cumple que el año y semana del dato son mayores a la promo o el mes igual, activo.
        elif (df.loc[line, 'Year'] >= df.loc[line, 'Promo2SinceYear']) and \
             (df.loc[line, 'Week'] >= df.loc[line, 'Promo2SinceWeek']) and \
             (df.loc[line, 'Month'] in df.loc[line, 'PromoInterval']):
            df.loc[line, 'Promo2Active'] = 1
        # Cualquier otro caso, no activo
        else:
            df.loc[line, 'Promo2Active'] = 0
            
    df.drop(['Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval'], axis=1, inplace=True)

    return df




def get_mean(train):
    return np.full(len(train), train.Sales.mean())

def rmspe(y_true, y_pred):
    """
    Compute the Root Mean Square Percentage Error (RMSPE) between the true and predicted values.
    
    Parameters:
    - y_true: array-like, true target values
    - y_pred: array-like, predicted target values
    
    Returns:
    - float, RMSPE value
    """
    # Ensure both arrays have the same length
    assert len(y_true) == len(y_pred)
    
    # Compute the percentage error for each observation
    percentage_error = (y_true - y_pred) / y_true
    
    # Exclude observations where true value is zero
    percentage_error[y_true == 0] = 0
    
    # Square the percentage errors
    squared_percentage_error = percentage_error ** 2
    
    # Compute the mean of the squared percentage errors
    mean_squared_percentage_error = np.mean(squared_percentage_error)
    
    # Compute the square root of the mean squared percentage error
    rmspe = np.sqrt(mean_squared_percentage_error)
    
    return rmspe # Convert to percentage


def try_model(model, train_inputs, train_targets, val_inputs, val_targets):
    model.fit(train_inputs, train_targets)

    train_preds = model.predict(train_inputs)
    val_preds = model.predict(val_inputs)

    # Get RMSE
    train_rmse = np.round(mean_squared_error(train_targets, train_preds, squared=False), 5)
    val_rmse = np.round(mean_squared_error(val_targets, val_preds, squared=False), 5)

    # Get RMSPE
    train_rmspe = np.round(rmspe(train_targets, train_preds), 5)
    val_rmspe = np.round(rmspe(val_targets, val_preds), 5)

    print(f"Train RMSE: {train_rmse}")
    print(f"Val RMSE: {val_rmse}")
    print()
    print(f"Train RMSPE: {train_rmspe}")
    print(f"Val RMSPE: {val_rmspe}")

    return model



def try_model_ols(model, train_inputs, train_targets, val_inputs, val_targets, input_cols):
    
    # Training
    model.fit(train_inputs, train_targets)
    
    # Predicting
    val_preds = model.predict(val_inputs)
    
    # R2 en validación
    val_r_squared = r2_score(val_targets, val_preds)
    print(f"Validation R-squared: {val_r_squared}")
    
    # Mostrar coeficientes
    if hasattr(model, 'coef_'):
        coef_table = pd.DataFrame({
            'Variable': input_cols,
            'Coefficient': model.coef_
        })
        print("\nCoefficients Table:")
        print(coef_table)



