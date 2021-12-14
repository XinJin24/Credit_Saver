import flask
import os
import pickle
import pandas as pd
from skimage import io
from skimage import transform
import numpy as np
from flask import send_from_directory, Flask, request, jsonify, render_template, redirect, url_for
app = flask.Flask(__name__, template_folder='templates')
path_to_loan_amount_prediction = 'models/Loan_Amount_predict.pkl'
path_to_loan_prediction = 'models/loanPrediction.pkl'

with open(path_to_loan_prediction, 'rb') as f:
    loan_prediction = pickle.load(f)

with open(path_to_loan_amount_prediction, 'rb') as f:
    loan_amount_prediction = pickle.load(f)


@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('index.html'))

    if flask.request.method == 'POST':
        # Get the input from the user.
        # user_input_text = flask.request.form['user_input_text']
        uer_contractType = flask.request.form['loan_type']
        user_credit = flask.request.form['ask_loan_amount']
        user_downPayment = flask.request.form['down_payment_amount']
        user_goodsPrice = flask.request.form['goods_price']
        user_weekdate = flask.request.form['date']
        user_hour = flask.request.form['time_hour']
        user_accompany = flask.request.form['accompany']
        user_type = flask.request.form['client_type']
        user_goodsCategory = flask.request.form['goods_category']
        user_sellerIndustry = flask.request.form['seller_industry']
        user_loanTerm = flask.request.form['payment_term']
        user_gender = flask.request.form['user_gender']
        user_ownCar = flask.request.form['user_ownCar']
        user_ownHouse = flask.request.form['user_haveHouse']
        user_childrenCount = flask.request.form['user_childrenCount']
        user_annualIncome = flask.request.form['user_annualIncome']
        user_incomeType = flask.request.form['user_incomeType']
        user_educationType = flask.request.form['user_educationType']
        user_familyStatus = flask.request.form['user_familyStatus']
        user_housingType = flask.request.form['user_houseType']
        user_daysBirth = float(flask.request.form['user_age'])*-360
        user_daysEmployed = float(
            flask.request.form['User_employment_days'])*-1
        user_ownCarAge = flask.request.form['User_ageOwnCar']
        user_ownMobil = flask.request.form['user_ownMobile']
        user_ownEmail = flask.request.form['user_ownEmail']
        user_familyMemberCount = flask.request.form['User_familyMembersCount']

        if(uer_contractType == 'loan_type_consumer_loan'):
            NAME_CONTRACT_TYPE_Consumer_loans = 1
            NAME_CONTRACT_TYPE_Revolving_loans = 0
        elif(uer_contractType == 'loan_type_revolving_loan'):
            NAME_CONTRACT_TYPE_Consumer_loans = 0
            NAME_CONTRACT_TYPE_Revolving_loans = 1

        if(user_weekdate == 'date_mon'):
            WEEKDAY_APPR_PROCESS_START_MONDAY = 1
            WEEKDAY_APPR_PROCESS_START_SATURDAY = 0
            WEEKDAY_APPR_PROCESS_START_SUNDAY = 0
            WEEKDAY_APPR_PROCESS_START_THURSDAY = 0
            WEEKDAY_APPR_PROCESS_START_TUESDAY = 0
            WEEKDAY_APPR_PROCESS_START_WEDNESDAY = 0
        elif(user_weekdate == 'date_tue'):
            WEEKDAY_APPR_PROCESS_START_MONDAY = 0
            WEEKDAY_APPR_PROCESS_START_SATURDAY = 0
            WEEKDAY_APPR_PROCESS_START_SUNDAY = 0
            WEEKDAY_APPR_PROCESS_START_THURSDAY = 0
            WEEKDAY_APPR_PROCESS_START_TUESDAY = 1
            WEEKDAY_APPR_PROCESS_START_WEDNESDAY = 0
        elif(user_weekdate == 'date_wed'):
            WEEKDAY_APPR_PROCESS_START_MONDAY = 0
            WEEKDAY_APPR_PROCESS_START_SATURDAY = 0
            WEEKDAY_APPR_PROCESS_START_SUNDAY = 0
            WEEKDAY_APPR_PROCESS_START_THURSDAY = 0
            WEEKDAY_APPR_PROCESS_START_TUESDAY = 0
            WEEKDAY_APPR_PROCESS_START_WEDNESDAY = 1
        elif(user_weekdate == 'date_thu'):
            WEEKDAY_APPR_PROCESS_START_MONDAY = 0
            WEEKDAY_APPR_PROCESS_START_SATURDAY = 0
            WEEKDAY_APPR_PROCESS_START_SUNDAY = 0
            WEEKDAY_APPR_PROCESS_START_THURSDAY = 1
            WEEKDAY_APPR_PROCESS_START_TUESDAY = 0
            WEEKDAY_APPR_PROCESS_START_WEDNESDAY = 0
        elif(user_weekdate == 'date_sat'):
            WEEKDAY_APPR_PROCESS_START_MONDAY = 0
            WEEKDAY_APPR_PROCESS_START_SATURDAY = 1
            WEEKDAY_APPR_PROCESS_START_SUNDAY = 0
            WEEKDAY_APPR_PROCESS_START_THURSDAY = 0
            WEEKDAY_APPR_PROCESS_START_TUESDAY = 0
            WEEKDAY_APPR_PROCESS_START_WEDNESDAY = 0
        elif(user_weekdate == 'date_sun'):
            WEEKDAY_APPR_PROCESS_START_MONDAY = 0
            WEEKDAY_APPR_PROCESS_START_SATURDAY = 0
            WEEKDAY_APPR_PROCESS_START_SUNDAY = 1
            WEEKDAY_APPR_PROCESS_START_THURSDAY = 0
            WEEKDAY_APPR_PROCESS_START_TUESDAY = 0
            WEEKDAY_APPR_PROCESS_START_WEDNESDAY = 0

        if(user_accompany == 'accompany_family'):
            NAME_TYPE_SUITE_Family = 1
            NAME_TYPE_SUITE_Group_of_people = 0
            NAME_TYPE_SUITE_No_Specified = 0
            NAME_TYPE_SUITE_Other_A = 0
            NAME_TYPE_SUITE_Other_B = 0
            NAME_TYPE_SUITE_Spouse_partner = 0
            NAME_TYPE_SUITE_Unaccompanied = 0
        elif(user_accompany == 'accompany_spouse'):
            NAME_TYPE_SUITE_Family = 0
            NAME_TYPE_SUITE_Group_of_people = 0
            NAME_TYPE_SUITE_No_Specified = 0
            NAME_TYPE_SUITE_Other_A = 0
            NAME_TYPE_SUITE_Other_B = 0
            NAME_TYPE_SUITE_Spouse_partner = 1
            NAME_TYPE_SUITE_Unaccompanied = 0
        elif(user_accompany == 'accompany_group'):
            NAME_TYPE_SUITE_Family = 0
            NAME_TYPE_SUITE_Group_of_people = 1
            NAME_TYPE_SUITE_No_Specified = 0
            NAME_TYPE_SUITE_Other_A = 0
            NAME_TYPE_SUITE_Other_B = 0
            NAME_TYPE_SUITE_Spouse_partner = 0
            NAME_TYPE_SUITE_Unaccompanied = 0
        elif(user_accompany == 'accompany_other'):
            NAME_TYPE_SUITE_Family = 0
            NAME_TYPE_SUITE_Group_of_people = 0
            NAME_TYPE_SUITE_No_Specified = 0
            NAME_TYPE_SUITE_Other_A = 1
            NAME_TYPE_SUITE_Other_B = 0
            NAME_TYPE_SUITE_Spouse_partner = 0
            NAME_TYPE_SUITE_Unaccompanied = 0
        elif(user_accompany == 'accompany_unaccompanied'):
            NAME_TYPE_SUITE_Family = 0
            NAME_TYPE_SUITE_Group_of_people = 0
            NAME_TYPE_SUITE_No_Specified = 0
            NAME_TYPE_SUITE_Other_A = 0
            NAME_TYPE_SUITE_Other_B = 0
            NAME_TYPE_SUITE_Spouse_partner = 0
            NAME_TYPE_SUITE_Unaccompanied = 1

        if(user_type == 'client_type_refreshed'):
            NAME_CLIENT_TYPE_Refreshed = 1
            NAME_CLIENT_TYPE_Repeater = 0
            NAME_CLIENT_TYPE_XNA = 0
        elif(user_type == 'client_type_repeater'):
            NAME_CLIENT_TYPE_Refreshed = 0
            NAME_CLIENT_TYPE_Repeater = 1
            NAME_CLIENT_TYPE_XNA = 0

        if(user_goodsCategory == 'goods_category_audionvideo'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 1
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_autoAccessories'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 1
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_cloth'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 1
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_computer'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 1
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_construction'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 1
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_consumerElectronics'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 1
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_directSales'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 1
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_education'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 1
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_fitness'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 1
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_furniture'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 1
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_gardening'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 1
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_homewares'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 1
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_insurance'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 1
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_jewelry'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 1
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_medicalSupplies'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 1
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_medicine'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 1
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_mobile'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 1
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_officeAppliances'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 1
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_photo'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 1
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_sport'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 1
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_tourism'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 1
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_vehicles'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 1
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_weapon'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 1
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_animal'):
            NAME_GOODS_CATEGORY_Animals = 1
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 0
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0
        elif(user_goodsCategory == 'goods_category_other'):
            NAME_GOODS_CATEGORY_Animals = 0
            NAME_GOODS_CATEGORY_Audio = 0
            NAME_GOODS_CATEGORY_Auto_Accessories = 0
            NAME_GOODS_CATEGORY_Clothing = 0
            NAME_GOODS_CATEGORY_Computers = 0
            NAME_GOODS_CATEGORY_Construction = 0
            NAME_GOODS_CATEGORY_Consumer_Electronics = 0
            NAME_GOODS_CATEGORY_Direct_Sales = 0
            NAME_GOODS_CATEGORY_Education = 0
            NAME_GOODS_CATEGORY_Fitness = 0
            NAME_GOODS_CATEGORY_Furniture = 0
            NAME_GOODS_CATEGORY_Gardening = 0
            NAME_GOODS_CATEGORY_Homewares = 0
            NAME_GOODS_CATEGORY_Insurance = 0
            NAME_GOODS_CATEGORY_Jewelry = 0
            NAME_GOODS_CATEGORY_Medical_Supplies = 0
            NAME_GOODS_CATEGORY_Medicine = 0
            NAME_GOODS_CATEGORY_Mobile = 0
            NAME_GOODS_CATEGORY_Office_Appliances = 0
            NAME_GOODS_CATEGORY_Other = 1
            NAME_GOODS_CATEGORY_Photo_Cinema_Equipment = 0
            NAME_GOODS_CATEGORY_Sport_and_Leisure = 0
            NAME_GOODS_CATEGORY_Tourism = 0
            NAME_GOODS_CATEGORY_Vehicles = 0
            NAME_GOODS_CATEGORY_Weapon = 0
            NAME_GOODS_CATEGORY_XNA = 0

        if(user_sellerIndustry == 'seller_industry_clothing'):
            NAME_SELLER_INDUSTRY_Clothing = 1
            NAME_SELLER_INDUSTRY_Connectivity = 0
            NAME_SELLER_INDUSTRY_Construction = 0
            NAME_SELLER_INDUSTRY_Consumer_electronics = 0
            NAME_SELLER_INDUSTRY_Furniture = 0
            NAME_SELLER_INDUSTRY_Industry = 0
            NAME_SELLER_INDUSTRY_Jewelry = 0
            NAME_SELLER_INDUSTRY_MLM_partners = 0
            NAME_SELLER_INDUSTRY_Tourism = 0
            NAME_SELLER_INDUSTRY_XNA = 0
        elif(user_sellerIndustry == 'seller_industry_connectivity'):
            NAME_SELLER_INDUSTRY_Clothing = 0
            NAME_SELLER_INDUSTRY_Connectivity = 1
            NAME_SELLER_INDUSTRY_Construction = 0
            NAME_SELLER_INDUSTRY_Consumer_electronics = 0
            NAME_SELLER_INDUSTRY_Furniture = 0
            NAME_SELLER_INDUSTRY_Industry = 0
            NAME_SELLER_INDUSTRY_Jewelry = 0
            NAME_SELLER_INDUSTRY_MLM_partners = 0
            NAME_SELLER_INDUSTRY_Tourism = 0
            NAME_SELLER_INDUSTRY_XNA = 0
        elif(user_sellerIndustry == 'seller_industry_construction'):
            NAME_SELLER_INDUSTRY_Clothing = 0
            NAME_SELLER_INDUSTRY_Connectivity = 0
            NAME_SELLER_INDUSTRY_Construction = 1
            NAME_SELLER_INDUSTRY_Consumer_electronics = 0
            NAME_SELLER_INDUSTRY_Furniture = 0
            NAME_SELLER_INDUSTRY_Industry = 0
            NAME_SELLER_INDUSTRY_Jewelry = 0
            NAME_SELLER_INDUSTRY_MLM_partners = 0
            NAME_SELLER_INDUSTRY_Tourism = 0
            NAME_SELLER_INDUSTRY_XNA = 0
        elif(user_sellerIndustry == 'seller_industry_consumerElectronics'):
            NAME_SELLER_INDUSTRY_Clothing = 0
            NAME_SELLER_INDUSTRY_Connectivity = 0
            NAME_SELLER_INDUSTRY_Construction = 0
            NAME_SELLER_INDUSTRY_Consumer_electronics = 1
            NAME_SELLER_INDUSTRY_Furniture = 0
            NAME_SELLER_INDUSTRY_Industry = 0
            NAME_SELLER_INDUSTRY_Jewelry = 0
            NAME_SELLER_INDUSTRY_MLM_partners = 0
            NAME_SELLER_INDUSTRY_Tourism = 0
            NAME_SELLER_INDUSTRY_XNA = 0
        elif(user_sellerIndustry == 'seller_industry_furniture'):
            NAME_SELLER_INDUSTRY_Clothing = 0
            NAME_SELLER_INDUSTRY_Connectivity = 0
            NAME_SELLER_INDUSTRY_Construction = 0
            NAME_SELLER_INDUSTRY_Consumer_electronics = 0
            NAME_SELLER_INDUSTRY_Furniture = 1
            NAME_SELLER_INDUSTRY_Industry = 0
            NAME_SELLER_INDUSTRY_Jewelry = 0
            NAME_SELLER_INDUSTRY_MLM_partners = 0
            NAME_SELLER_INDUSTRY_Tourism = 0
            NAME_SELLER_INDUSTRY_XNA = 0
        elif(user_sellerIndustry == 'seller_industry_industry'):
            NAME_SELLER_INDUSTRY_Clothing = 0
            NAME_SELLER_INDUSTRY_Connectivity = 0
            NAME_SELLER_INDUSTRY_Construction = 0
            NAME_SELLER_INDUSTRY_Consumer_electronics = 0
            NAME_SELLER_INDUSTRY_Furniture = 0
            NAME_SELLER_INDUSTRY_Industry = 1
            NAME_SELLER_INDUSTRY_Jewelry = 0
            NAME_SELLER_INDUSTRY_MLM_partners = 0
            NAME_SELLER_INDUSTRY_Tourism = 0
            NAME_SELLER_INDUSTRY_XNA = 0
        elif(user_sellerIndustry == 'seller_industry_jewelry'):
            NAME_SELLER_INDUSTRY_Clothing = 0
            NAME_SELLER_INDUSTRY_Connectivity = 0
            NAME_SELLER_INDUSTRY_Construction = 0
            NAME_SELLER_INDUSTRY_Consumer_electronics = 0
            NAME_SELLER_INDUSTRY_Furniture = 0
            NAME_SELLER_INDUSTRY_Industry = 0
            NAME_SELLER_INDUSTRY_Jewelry = 1
            NAME_SELLER_INDUSTRY_MLM_partners = 0
            NAME_SELLER_INDUSTRY_Tourism = 0
            NAME_SELLER_INDUSTRY_XNA = 0
        elif(user_sellerIndustry == 'seller_industry_MLMpartners'):
            NAME_SELLER_INDUSTRY_Clothing = 0
            NAME_SELLER_INDUSTRY_Connectivity = 0
            NAME_SELLER_INDUSTRY_Construction = 0
            NAME_SELLER_INDUSTRY_Consumer_electronics = 0
            NAME_SELLER_INDUSTRY_Furniture = 0
            NAME_SELLER_INDUSTRY_Industry = 0
            NAME_SELLER_INDUSTRY_Jewelry = 0
            NAME_SELLER_INDUSTRY_MLM_partners = 1
            NAME_SELLER_INDUSTRY_Tourism = 0
            NAME_SELLER_INDUSTRY_XNA = 0
        elif(user_sellerIndustry == 'seller_industry_tourism'):
            NAME_SELLER_INDUSTRY_Clothing = 0
            NAME_SELLER_INDUSTRY_Connectivity = 0
            NAME_SELLER_INDUSTRY_Construction = 0
            NAME_SELLER_INDUSTRY_Consumer_electronics = 0
            NAME_SELLER_INDUSTRY_Furniture = 0
            NAME_SELLER_INDUSTRY_Industry = 0
            NAME_SELLER_INDUSTRY_Jewelry = 0
            NAME_SELLER_INDUSTRY_MLM_partners = 0
            NAME_SELLER_INDUSTRY_Tourism = 1
            NAME_SELLER_INDUSTRY_XNA = 0
        elif(user_sellerIndustry == 'seller_industry_others'):
            NAME_SELLER_INDUSTRY_Clothing = 0
            NAME_SELLER_INDUSTRY_Connectivity = 0
            NAME_SELLER_INDUSTRY_Construction = 0
            NAME_SELLER_INDUSTRY_Consumer_electronics = 0
            NAME_SELLER_INDUSTRY_Furniture = 0
            NAME_SELLER_INDUSTRY_Industry = 0
            NAME_SELLER_INDUSTRY_Jewelry = 0
            NAME_SELLER_INDUSTRY_MLM_partners = 0
            NAME_SELLER_INDUSTRY_Tourism = 0
            NAME_SELLER_INDUSTRY_XNA = 1

        if(user_incomeType == 'user_incomeType_working'):
            NAME_INCOME_TYPE_Maternity_leave = 0
            NAME_INCOME_TYPE_Pensioner = 0
            NAME_INCOME_TYPE_State_servant = 0
            NAME_INCOME_TYPE_Student = 0
            NAME_INCOME_TYPE_Unemployed = 0
            NAME_INCOME_TYPE_Working = 1
        elif(user_incomeType == 'user_incomeType_pensioner'):
            NAME_INCOME_TYPE_Maternity_leave = 0
            NAME_INCOME_TYPE_Pensioner = 1
            NAME_INCOME_TYPE_State_servant = 0
            NAME_INCOME_TYPE_Student = 0
            NAME_INCOME_TYPE_Unemployed = 0
            NAME_INCOME_TYPE_Working = 0
        elif(user_incomeType == 'user_incomeType_state'):
            NAME_INCOME_TYPE_Maternity_leave = 0
            NAME_INCOME_TYPE_Pensioner = 0
            NAME_INCOME_TYPE_State_servant = 1
            NAME_INCOME_TYPE_Student = 0
            NAME_INCOME_TYPE_Unemployed = 0
            NAME_INCOME_TYPE_Working = 0
        elif(user_incomeType == 'user_incomeType_unemployed'):
            NAME_INCOME_TYPE_Maternity_leave = 0
            NAME_INCOME_TYPE_Pensioner = 0
            NAME_INCOME_TYPE_State_servant = 0
            NAME_INCOME_TYPE_Student = 0
            NAME_INCOME_TYPE_Unemployed = 1
            NAME_INCOME_TYPE_Working = 0
        elif(user_incomeType == 'user_incomeType_student'):
            NAME_INCOME_TYPE_Maternity_leave = 0
            NAME_INCOME_TYPE_Pensioner = 0
            NAME_INCOME_TYPE_State_servant = 0
            NAME_INCOME_TYPE_Student = 1
            NAME_INCOME_TYPE_Unemployed = 0
            NAME_INCOME_TYPE_Working = 0
        elif(user_incomeType == 'user_incomeType_maternity'):
            NAME_INCOME_TYPE_Maternity_leave = 1
            NAME_INCOME_TYPE_Pensioner = 0
            NAME_INCOME_TYPE_State_servant = 0
            NAME_INCOME_TYPE_Student = 0
            NAME_INCOME_TYPE_Unemployed = 0
            NAME_INCOME_TYPE_Working = 0

        if(user_educationType == 'user_educationType_secondary'):
            NAME_EDUCATION_TYPE_Higher_education = 0
            NAME_EDUCATION_TYPE_Incomplete_higher = 0
            NAME_EDUCATION_TYPE_Lower_secondary = 0
            NAME_EDUCATION_TYPE_Secondary_secondary_special = 1
        elif(user_educationType == 'user_educationType_higher'):
            NAME_EDUCATION_TYPE_Higher_education = 0
            NAME_EDUCATION_TYPE_Incomplete_higher = 1
            NAME_EDUCATION_TYPE_Lower_secondary = 0
            NAME_EDUCATION_TYPE_Secondary_secondary_special = 0
        elif(user_educationType == 'user_educationType_incompleteHigher'):
            NAME_EDUCATION_TYPE_Higher_education = 0
            NAME_EDUCATION_TYPE_Incomplete_higher = 1
            NAME_EDUCATION_TYPE_Lower_secondary = 0
            NAME_EDUCATION_TYPE_Secondary_secondary_special = 0
        elif(user_educationType == 'user_educationType_lowerSecondary'):
            NAME_EDUCATION_TYPE_Higher_education = 0
            NAME_EDUCATION_TYPE_Incomplete_higher = 0
            NAME_EDUCATION_TYPE_Lower_secondary = 1
            NAME_EDUCATION_TYPE_Secondary_secondary_special = 0

        if(user_familyStatus == 'user_familyStatus_married'):
            NAME_FAMILY_STATUS_Married = 1
            NAME_FAMILY_STATUS_Separated = 0
            NAME_FAMILY_STATUS_Single_not_married = 0
            NAME_FAMILY_STATUS_Widow = 0
        elif(user_familyStatus == 'user_familyStatus_notMarried'):
            NAME_FAMILY_STATUS_Married = 0
            NAME_FAMILY_STATUS_Separated = 0
            NAME_FAMILY_STATUS_Single_not_married = 1
            NAME_FAMILY_STATUS_Widow = 0
        elif(user_familyStatus == 'user_familyStatus_separated'):
            NAME_FAMILY_STATUS_Married = 0
            NAME_FAMILY_STATUS_Separated = 1
            NAME_FAMILY_STATUS_Single_not_married = 0
            NAME_FAMILY_STATUS_Widow = 0
        elif(user_familyStatus == 'user_familyStatus_widow'):
            NAME_FAMILY_STATUS_Married = 0
            NAME_FAMILY_STATUS_Separated = 0
            NAME_FAMILY_STATUS_Single_not_married = 0
            NAME_FAMILY_STATUS_Widow = 1

        if(user_housingType == 'user_houseType_house'):
            NAME_HOUSING_TYPE_House_apartment = 1
            NAME_HOUSING_TYPE_Municipal_apartment = 0
            NAME_HOUSING_TYPE_Office_apartment = 0
            NAME_HOUSING_TYPE_Rented_apartment = 0
            NAME_HOUSING_TYPE_With_parents = 0
        elif(user_housingType == 'user_houseType_withParents'):
            NAME_HOUSING_TYPE_House_apartment = 0
            NAME_HOUSING_TYPE_Municipal_apartment = 0
            NAME_HOUSING_TYPE_Office_apartment = 0
            NAME_HOUSING_TYPE_Rented_apartment = 0
            NAME_HOUSING_TYPE_With_parents = 1
        elif(user_housingType == 'user_houseType_municiupal'):
            NAME_HOUSING_TYPE_House_apartment = 0
            NAME_HOUSING_TYPE_Municipal_apartment = 1
            NAME_HOUSING_TYPE_Office_apartment = 0
            NAME_HOUSING_TYPE_Rented_apartment = 0
            NAME_HOUSING_TYPE_With_parents = 0
        elif(user_housingType == 'user_houseType_office'):
            NAME_HOUSING_TYPE_House_apartment = 0
            NAME_HOUSING_TYPE_Municipal_apartment = 0
            NAME_HOUSING_TYPE_Office_apartment = 1
            NAME_HOUSING_TYPE_Rented_apartment = 0
            NAME_HOUSING_TYPE_With_parents = 0
        elif(user_housingType == 'user_houseType_rented'):
            NAME_HOUSING_TYPE_House_apartment = 0
            NAME_HOUSING_TYPE_Municipal_apartment = 0
            NAME_HOUSING_TYPE_Office_apartment = 0
            NAME_HOUSING_TYPE_Rented_apartment = 1
            NAME_HOUSING_TYPE_With_parents = 0

        list_of_inputs = [user_credit,
                          user_downPayment,
                          user_goodsPrice,
                          user_hour,
                          user_loanTerm,
                          user_gender,
                          user_ownCar,
                          user_ownHouse,
                          user_childrenCount,
                          user_annualIncome,
                          user_daysBirth,
                          user_daysEmployed,
                          user_ownCarAge,
                          user_ownMobil,
                          user_ownEmail,
                          user_familyMemberCount,
                          NAME_CONTRACT_TYPE_Consumer_loans,
                          NAME_CONTRACT_TYPE_Revolving_loans,
                          WEEKDAY_APPR_PROCESS_START_MONDAY,
                          WEEKDAY_APPR_PROCESS_START_SATURDAY,
                          WEEKDAY_APPR_PROCESS_START_SUNDAY,
                          WEEKDAY_APPR_PROCESS_START_THURSDAY,
                          WEEKDAY_APPR_PROCESS_START_TUESDAY,
                          WEEKDAY_APPR_PROCESS_START_WEDNESDAY,
                          NAME_TYPE_SUITE_Family,
                          NAME_TYPE_SUITE_Group_of_people,
                          NAME_TYPE_SUITE_No_Specified,
                          NAME_TYPE_SUITE_Other_A,
                          NAME_TYPE_SUITE_Other_B,
                          NAME_TYPE_SUITE_Spouse_partner,
                          NAME_TYPE_SUITE_Unaccompanied,
                          NAME_CLIENT_TYPE_Refreshed,
                          NAME_CLIENT_TYPE_Repeater,
                          NAME_CLIENT_TYPE_XNA,
                          NAME_GOODS_CATEGORY_Animals,
                          NAME_GOODS_CATEGORY_Audio,
                          NAME_GOODS_CATEGORY_Auto_Accessories,
                          NAME_GOODS_CATEGORY_Clothing,
                          NAME_GOODS_CATEGORY_Computers,
                          NAME_GOODS_CATEGORY_Construction,
                          NAME_GOODS_CATEGORY_Consumer_Electronics,
                          NAME_GOODS_CATEGORY_Direct_Sales,
                          NAME_GOODS_CATEGORY_Education,
                          NAME_GOODS_CATEGORY_Fitness,
                          NAME_GOODS_CATEGORY_Furniture,
                          NAME_GOODS_CATEGORY_Gardening,
                          NAME_GOODS_CATEGORY_Homewares,
                          NAME_GOODS_CATEGORY_Insurance,
                          NAME_GOODS_CATEGORY_Jewelry,
                          NAME_GOODS_CATEGORY_Medical_Supplies,
                          NAME_GOODS_CATEGORY_Medicine,
                          NAME_GOODS_CATEGORY_Mobile,
                          NAME_GOODS_CATEGORY_Office_Appliances,
                          NAME_GOODS_CATEGORY_Other,
                          NAME_GOODS_CATEGORY_Photo_Cinema_Equipment,
                          NAME_GOODS_CATEGORY_Sport_and_Leisure,
                          NAME_GOODS_CATEGORY_Tourism,
                          NAME_GOODS_CATEGORY_Vehicles,
                          NAME_GOODS_CATEGORY_Weapon,
                          NAME_GOODS_CATEGORY_XNA,
                          NAME_SELLER_INDUSTRY_Clothing,
                          NAME_SELLER_INDUSTRY_Connectivity,
                          NAME_SELLER_INDUSTRY_Construction,
                          NAME_SELLER_INDUSTRY_Consumer_electronics,
                          NAME_SELLER_INDUSTRY_Furniture,
                          NAME_SELLER_INDUSTRY_Industry,
                          NAME_SELLER_INDUSTRY_Jewelry,
                          NAME_SELLER_INDUSTRY_MLM_partners,
                          NAME_SELLER_INDUSTRY_Tourism,
                          NAME_SELLER_INDUSTRY_XNA,
                          NAME_INCOME_TYPE_Maternity_leave,
                          NAME_INCOME_TYPE_Pensioner,
                          NAME_INCOME_TYPE_State_servant,
                          NAME_INCOME_TYPE_Student,
                          NAME_INCOME_TYPE_Unemployed,
                          NAME_INCOME_TYPE_Working,
                          NAME_EDUCATION_TYPE_Higher_education,
                          NAME_EDUCATION_TYPE_Incomplete_higher,
                          NAME_EDUCATION_TYPE_Lower_secondary,
                          NAME_EDUCATION_TYPE_Secondary_secondary_special,
                          NAME_FAMILY_STATUS_Married,
                          NAME_FAMILY_STATUS_Separated,
                          NAME_FAMILY_STATUS_Single_not_married,
                          NAME_FAMILY_STATUS_Widow,
                          NAME_HOUSING_TYPE_House_apartment,
                          NAME_HOUSING_TYPE_Municipal_apartment,
                          NAME_HOUSING_TYPE_Office_apartment,
                          NAME_HOUSING_TYPE_Rented_apartment,
                          NAME_HOUSING_TYPE_With_parents]
        list_of_inputs = np.array(list_of_inputs).reshape(1, 89)
        result = loan_prediction.predict(list_of_inputs)
        

        if result == 'Approved':
            prediction = 'Approved'
        else:
            prediction = 'Not Approved'
        return (flask.render_template('index.html', result=prediction))

    return(flask.render_template('index.html'))


@app.route('/Loan_Amount_predict/', methods=['GET', 'POST'])
def Loan_Amount_predict():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('Loan_Amount_predict.html'))

    if flask.request.method == 'POST':
        # Get the input from the user.
        user_downPayment = flask.request.form['down_payment_amount']
        user_goodsPrice = flask.request.form['goods_price']
        user_annualIncome = flask.request.form['user_annualIncome']
        user_daysBirth = float(flask.request.form['user_age'])*-360
        user_daysEmployed = float(
            flask.request.form['User_employment_days'])*-1
        list_of_inputs = [ user_downPayment, user_goodsPrice,
                          user_annualIncome, user_daysBirth, user_daysEmployed]
        list_of_inputs = np.array(list_of_inputs).reshape(1, 5)
        prediction = loan_amount_prediction.predict(list_of_inputs)
        prediction = round(prediction[0][0], 2)

        return (flask.render_template('Loan_Amount_predict.html', amount_result=prediction))
    return(flask.render_template('Loan_Amount_predict.html'))


@app.route('/bootstrap/')
def bootstrap():
    return flask.render_template('bootstrap.html')


if __name__ == '__main__':
    app.run(debug=True)
