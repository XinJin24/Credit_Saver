# Import our libraries 
import pickle
# Pandas and numpy for data wrangling
import pandas as pd
import numpy as np
# Seaborn / matplotlib for visualization 
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
# Import the trees from sklearn
from sklearn import tree

# Helper function to split our data
from sklearn.model_selection import train_test_split

# Helper fuctions to evaluate our model.
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, f1_score, roc_auc_score 

# Helper function for hyper-parameter turning.
from sklearn.model_selection import GridSearchCV

# Import our Decision Tree
from sklearn.tree import DecisionTreeClassifier 

# Import our Random Forest 
from sklearn.ensemble import RandomForestClassifier

# Library for visualizing our tree
# If you get an error, run 'conda install python-graphviz' in your terminal
import graphviz
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import scipy.stats as stats


df = pd.read_csv('https://raw.githubusercontent.com/DataScience_Project/Project_Dataset/Application_Data.csv')
# df = pd.read_csv('Project_Dataset/Application_Data.csv')
df['NAME_CONTRACT_STATUS']=df['NAME_CONTRACT_STATUS'].replace('Unused offer', 'Approved')

# df.drop(df[df['NAME_CONTRACT_STATUS'] =='Canceled'].index, inplace = True)

df = df.dropna( how='any',subset=['AMT_CREDIT'])

df = df.dropna( how='any',subset=['CODE_GENDER'])

df = df.dropna( how='any',subset=['AMT_GOODS_PRICE'])

df = df.dropna( how='any',subset=['CNT_PAYMENT'])

df = df.dropna( how='any',subset=['CODE_GENDER'])

df['AMT_DOWN_PAYMENT'] = np.where(((df['AMT_DOWN_PAYMENT'].isnull()==True) ), 0,df['AMT_DOWN_PAYMENT'] )

df['OWN_CAR_AGE'] = np.where(((df['OWN_CAR_AGE'].isnull()==True) ), 0,df['OWN_CAR_AGE'] )

df['CNT_FAM_MEMBERS'] = np.where(((df['CNT_FAM_MEMBERS'].isnull()==True) ), 0,df['CNT_FAM_MEMBERS'] )

df['NAME_TYPE_SUITE'] = np.where(((df['NAME_TYPE_SUITE'].isnull()==True) ), 'No Specified',df['NAME_TYPE_SUITE'] )

df['CODE_GENDER'] = np.where(((df['CODE_GENDER']=='M') ), '1','0')

df['FLAG_OWN_CAR'] = np.where(((df['FLAG_OWN_CAR']=='Y') ), '1','0')

df['FLAG_OWN_REALTY'] = np.where(((df['FLAG_OWN_REALTY']=='Y') ), '1','0')

df.drop(['NAME_CONTRACT_TYPE','WEEKDAY_APPR_PROCESS_START','HOUR_APPR_PROCESS_START','NAME_TYPE_SUITE','NAME_CLIENT_TYPE',
        'NAME_GOODS_CATEGORY','NAME_SELLER_INDUSTRY','NAME_INCOME_TYPE','NAME_EDUCATION_TYPE','NAME_FAMILY_STATUS','NAME_HOUSING_TYPE',], axis=1, inplace=True)
#prepare datas for build



original_cols = df.columns

target_cols = ['AMT_APPLICATION','AMT_DOWN_PAYMENT','AMT_GOODS_PRICE',
               'CNT_PAYMENT','AMT_INCOME_TOTAL','DAYS_BIRTH','DAYS_EMPLOYED']

z_score_cols = []

# Loop through our target columns
for col in target_cols:
    # Make the new column name the same as the original but with 'z_score' added to it
    new_col_name = col + "_zscore"
    
    # Set the new column equal to the score
    df[new_col_name] = stats.stats.zscore( df[col] )
    
    # Set the z-score to its absolute value of the for easier filtering
    df[new_col_name] = abs( df[new_col_name] )
    
    # Append the new column name our our z_score_cols list for easier access for later.
    z_score_cols.append(new_col_name)


condition = df[z_score_cols] < 3
print(df.shape)

# # Say TRUE only if all of the rows are True, else return False
condition = condition.all(axis=1)

print('Before removal of outliers', df.shape)

df = df[condition]

print('After removal of outliers', df.shape)



features = ['AMT_APPLICATION','AMT_DOWN_PAYMENT','AMT_GOODS_PRICE','AMT_INCOME_TOTAL','DAYS_BIRTH','DAYS_EMPLOYED']
target = ['AMT_CREDIT']

X = df[features].values


# ISOLATE JUST OUR TARGET DATA, THIS IS WHAT WE ARE TRYING TO PREDICT
y = df[target].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
r_squared = metrics.r2_score(y_test, y_pred)
print('R-Squared Score:', r_squared)
mae = metrics.mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)


# GET THE COEFFICIENT VALUES FROM THE MODEL
coefficient_values = model.coef_

# MAKE A DATA FRAME OUT OF THE VALUES AND THEIR COLUMN NAMES
df_coefficients = pd.DataFrame(coefficient_values, columns=features).T

# RENAME THE COLUMN FROM 0 TO COEFFICIENT
df_coefficients.columns = ['coefficient']

y_pred = model.predict(X_test)
pickle.dump(model, open('.../models/Loan_Amount_predict.pkl', 'wb') )




