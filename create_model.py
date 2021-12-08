import pandas as pd
import pickle
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.naive_bayes import MultinomialNB

# Import our libraries 

# Pandas and numpy for data wrangling
import numpy as np

# Seaborn / matplotlib for visualization 
import seaborn as sns
sns.set()

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

from sklearn.tree import DecisionTreeClassifier 

df = pd.read_csv('https://raw.githubusercontent.com/Project Dataset/Application_Data.csv')

# Define our X
# uer_contractType=df['NAME_CONTRACT_TYPE']               
# user_credit=df['AMT_APPLICATION']                                
# user_downPayment=df['AMT_DOWN_PAYMENT']           
# user_goodsPrice=df['AMT_GOODS_PRICE']               
# user_weekdate=df['WEEKDAY_APPR_PROCESS_START']
# user_hour=df['HOUR_APPR_PROCESS_START']      
# user_accompany=df['NAME_TYPE_SUITE']              
# user_type=df['NAME_CLIENT_TYPE']         
# user_goodsCategory=df['NAME_GOODS_CATEGORY']         
# user_sellerIndustry=df['NAME_SELLER_INDUSTRY']
# user_loanTerm=df['CNT_PAYMENT']                   
# user_gender=df['CODE_GENDER']        
# user_ownCar=df['FLAG_OWN_CAR']          
# user_ownHouse=df['FLAG_OWN_REALTY']               
# user_childrenCount=df['CNT_CHILDREN']                  
# user_annualIncome=df['AMT_INCOME_TOTAL']              
# user_incomeType=df['NAME_INCOME_TYPE']              
# user_educationType=df['NAME_EDUCATION_TYPE']           
# user_familyStatus=df['NAME_FAMILY_STATUS']            
# user_housingType=df['NAME_HOUSING_TYPE']             
# user_daysBirth=df['DAYS_BIRTH']                    
# user_daysEmployed=df['DAYS_EMPLOYED']                 
# user_ownCarAge=df['OWN_CAR_AGE']                  
# user_ownMobil=df['FLAG_MOBIL']                             
# user_ownEmail=df['FLAG_EMAIL']                    
# user_familyMemberCount=df['CNT_FAM_MEMBERS']     

df['NAME_CONTRACT_STATUS']=df['NAME_CONTRACT_STATUS'].replace('Unused offer', 'Approved')
df.drop(df[df['NAME_CONTRACT_STATUS'] =='Canceled'].index, inplace = True)

df = df.dropna( how='any',subset=['AMT_CREDIT'])

df = df.dropna( how='any',subset=['CODE_GENDER'])

df = df.dropna( how='any',subset=['AMT_GOODS_PRICE'])

df = df.dropna( how='any',subset=['CNT_PAYMENT'])

df['AMT_DOWN_PAYMENT'] = np.where(((df['AMT_DOWN_PAYMENT'].isnull()==True) ), 0,df['AMT_DOWN_PAYMENT'] )

df['OWN_CAR_AGE'] = np.where(((df['OWN_CAR_AGE'].isnull()==True) ), 0,df['OWN_CAR_AGE'] )

df['CNT_FAM_MEMBERS'] = np.where(((df['CNT_FAM_MEMBERS'].isnull()==True) ), 0,df['CNT_FAM_MEMBERS'] )

df['NAME_TYPE_SUITE'] = np.where(((df['NAME_TYPE_SUITE'].isnull()==True) ), 'No Specified',df['NAME_TYPE_SUITE'] )

df['CODE_GENDER'] = np.where(((df['CODE_GENDER']=='M') ), '1','0')

df['FLAG_OWN_CAR'] = np.where(((df['FLAG_OWN_CAR']=='Y') ), '1','0')

df['FLAG_OWN_REALTY'] = np.where(((df['FLAG_OWN_REALTY']=='Y') ), '1','0')

df = pd.get_dummies(df, columns=['NAME_CONTRACT_TYPE','WEEKDAY_APPR_PROCESS_START','NAME_TYPE_SUITE',
                                'NAME_CLIENT_TYPE','NAME_GOODS_CATEGORY','NAME_SELLER_INDUSTRY','NAME_INCOME_TYPE',
                                 'NAME_EDUCATION_TYPE','NAME_FAMILY_STATUS','NAME_HOUSING_TYPE','NAME_YIELD_GROUP'
                                ], drop_first=True)

#prepare datas for build
selected_features = ['AMT_APPLICATION',
'AMT_DOWN_PAYMENT',
'AMT_GOODS_PRICE',
'HOUR_APPR_PROCESS_START',
'NAME_CONTRACT_STATUS',
'CNT_PAYMENT',
'CODE_GENDER',
'FLAG_OWN_CAR',
'FLAG_OWN_REALTY',
'CNT_CHILDREN',
'AMT_INCOME_TOTAL',
'DAYS_BIRTH',
'DAYS_EMPLOYED',
'OWN_CAR_AGE',
'FLAG_MOBIL',
'FLAG_EMAIL',
'CNT_FAM_MEMBERS',
'NAME_CONTRACT_TYPE_Consumer loans',
'NAME_CONTRACT_TYPE_Revolving loans',
'WEEKDAY_APPR_PROCESS_START_MONDAY',
'WEEKDAY_APPR_PROCESS_START_SATURDAY',
'WEEKDAY_APPR_PROCESS_START_SUNDAY',
'WEEKDAY_APPR_PROCESS_START_THURSDAY',
'WEEKDAY_APPR_PROCESS_START_TUESDAY',
'WEEKDAY_APPR_PROCESS_START_WEDNESDAY',
'NAME_TYPE_SUITE_Family',
'NAME_TYPE_SUITE_Group of people',
'NAME_TYPE_SUITE_No Specified',
'NAME_TYPE_SUITE_Other_A',
'NAME_TYPE_SUITE_Other_B',
'NAME_TYPE_SUITE_Spouse, partner',
'NAME_TYPE_SUITE_Unaccompanied',
'NAME_CLIENT_TYPE_Refreshed',
'NAME_CLIENT_TYPE_Repeater',
'NAME_CLIENT_TYPE_XNA',
'NAME_GOODS_CATEGORY_Animals',
'NAME_GOODS_CATEGORY_Audio/Video',
'NAME_GOODS_CATEGORY_Auto Accessories',
'NAME_GOODS_CATEGORY_Clothing and Accessories',
'NAME_GOODS_CATEGORY_Computers',
'NAME_GOODS_CATEGORY_Construction Materials',
'NAME_GOODS_CATEGORY_Consumer Electronics',
'NAME_GOODS_CATEGORY_Direct Sales',
'NAME_GOODS_CATEGORY_Education',
'NAME_GOODS_CATEGORY_Fitness',
'NAME_GOODS_CATEGORY_Furniture',
'NAME_GOODS_CATEGORY_Gardening',
'NAME_GOODS_CATEGORY_Homewares',
'NAME_GOODS_CATEGORY_Insurance',
'NAME_GOODS_CATEGORY_Jewelry',
'NAME_GOODS_CATEGORY_Medical Supplies',
'NAME_GOODS_CATEGORY_Medicine',
'NAME_GOODS_CATEGORY_Mobile',
'NAME_GOODS_CATEGORY_Office Appliances',
'NAME_GOODS_CATEGORY_Other',
'NAME_GOODS_CATEGORY_Photo / Cinema Equipment',
'NAME_GOODS_CATEGORY_Sport and Leisure',
'NAME_GOODS_CATEGORY_Tourism',
'NAME_GOODS_CATEGORY_Vehicles',
'NAME_GOODS_CATEGORY_Weapon',
'NAME_GOODS_CATEGORY_XNA',
'NAME_SELLER_INDUSTRY_Clothing',
'NAME_SELLER_INDUSTRY_Connectivity',
'NAME_SELLER_INDUSTRY_Construction',
'NAME_SELLER_INDUSTRY_Consumer electronics',
'NAME_SELLER_INDUSTRY_Furniture',
'NAME_SELLER_INDUSTRY_Industry',
'NAME_SELLER_INDUSTRY_Jewelry',
'NAME_SELLER_INDUSTRY_MLM partners',
'NAME_SELLER_INDUSTRY_Tourism',
'NAME_SELLER_INDUSTRY_XNA',
'NAME_INCOME_TYPE_Maternity leave',
'NAME_INCOME_TYPE_Pensioner',
'NAME_INCOME_TYPE_State servant',
'NAME_INCOME_TYPE_Student',
'NAME_INCOME_TYPE_Unemployed',
'NAME_INCOME_TYPE_Working',
'NAME_EDUCATION_TYPE_Higher education',
'NAME_EDUCATION_TYPE_Incomplete higher',
'NAME_EDUCATION_TYPE_Lower secondary',
'NAME_EDUCATION_TYPE_Secondary / secondary special',
'NAME_FAMILY_STATUS_Married',
'NAME_FAMILY_STATUS_Separated',
'NAME_FAMILY_STATUS_Single / not married',
'NAME_FAMILY_STATUS_Widow',
'NAME_HOUSING_TYPE_House / apartment',
'NAME_HOUSING_TYPE_Municipal apartment',
'NAME_HOUSING_TYPE_Office apartment',
'NAME_HOUSING_TYPE_Rented apartment',
'NAME_HOUSING_TYPE_With parents',
'NAME_YIELD_GROUP_high',
'NAME_YIELD_GROUP_low_action',
'NAME_YIELD_GROUP_low_normal',
'NAME_YIELD_GROUP_middle']

X = df[selected_features]
y = df['NAME_CONTRACT_STATUS']

model = DecisionTreeClassifier(criterion = "gini", random_state = 100,
                               max_depth=5, min_samples_leaf=5)

model.fit(X, y)
pickle.dump(model, open('models/loanPrediction.pkl', 'wb') )
# # Initalize our vectorizer
# DecisionTree = DecisionTreeClassifier()

# # Fit our vectorizer
# DecisionTree.fit(X)

# # Transform your X data using your fitted vectorizer. 
# X = vectorizer.transform(X)

# model = MultinomialNB(alpha=.025)

# # Fit our model with our training data.
# model.fit(X, y)

# # Save our vectorizer and model.
# pickle.dump(vectorizer, open('models/vectorizer.pkl', 'wb') )
# pickle.dump(model, open('models/text-classifier.pkl', 'wb') )


