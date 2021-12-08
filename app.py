import flask
import os
import pickle
import pandas as pd
from skimage import io
from skimage import transform
import numpy as np
from flask import send_from_directory, Flask, request, jsonify, render_template, redirect, url_for



app = flask.Flask(__name__, template_folder='templates')

path_to_vectorizer = 'models/vectorizer.pkl'
path_to_text_classifier = 'models/text-classifier.pkl'
path_to_image_classifier = 'models/image-classifier.pkl'
path_to_loan_prediction = 'models/loanPrediction.pkl'

with open(path_to_vectorizer, 'rb') as f:
    vectorizer = pickle.load(f)

with open(path_to_text_classifier, 'rb') as f:
    model = pickle.load(f)

with open(path_to_image_classifier, 'rb') as f:
    image_classifier = pickle.load(f)

with open(path_to_loan_prediction, 'rb') as f:
    loan_prediction = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('index.html'))


    if flask.request.method == 'POST':
        # Get the input from the user.
        # user_input_text = flask.request.form['user_input_text']


        uer_contractType=flask.request.form['loan_type']               
        user_credit=flask.request.form['ask_loan_amount']                                
        user_downPayment=flask.request.form['down_payment_amount']           
        user_goodsPrice=flask.request.form['goods_price']              
        user_weekdate=flask.request.form['date']
        user_hour=flask.request.form['time_hour']     
        user_accompany=flask.request.form['accompany']             
        user_type=flask.request.form['client_type']       
        user_goodsCategory=flask.request.form['goods_category']         
        user_sellerIndustry=flask.request.form['seller_industry']
        user_loanTerm=flask.request.form['payment_term']                  
        user_gender=flask.request.form['user_gender']        
        user_ownCar=flask.request.form['user_ownCar']       
        user_ownHouse=flask.request.form['user_haveHouse']              
        user_childrenCount=flask.request.form['user_childrenCount']                  
        user_annualIncome=flask.request.form['user_annualIncome']              
        user_incomeType=flask.request.form['user_incomeType']              
        user_educationType=flask.request.form['user_educationType']          
        user_familyStatus=flask.request.form['user_familyStatus']           
        user_housingType=flask.request.form['user_houseType']            
        user_daysBirth=flask.request.form['user_age']                
        user_daysEmployed=flask.request.form['User_employment_days']                 
        user_ownCarAge=flask.request.form['User_ageOwnCar']                 
        user_ownMobil=flask.request.form['user_ownMobile']                            
        user_ownEmail=flask.request.form['user_ownEmail']                    
        user_familyMemberCount=flask.request.form['User_familyMembersCount']   



        list_of_inputs=[uer_contractType,user_credit,user_downPayment,user_goodsPrice,user_weekdate,user_hour,user_accompany,user_type,
        user_goodsCategory,user_sellerIndustry,user_loanTerm,user_gender,user_ownCar,user_ownHouse,user_childrenCount,user_annualIncome,
        user_incomeType,user_educationType,user_familyStatus,user_housingType,user_daysBirth,user_daysEmployed,user_ownCarAge,user_ownMobil,
        user_ownEmail,user_familyMemberCount]

        result = loan_prediction(list_of_inputs)
        
        if result=='Approved':
            prediction='Approved'
        else:
            prediction='Not Approved'
            
        return flask.render_template('index.html',
            result=prediction)
        
        # # Turn the text into numbers using our vectorizer
        # X = vectorizer.transform([user_input_text])
        
        # # Make a prediction 
        # predictions = model.predict(X)
        
        # # Get the first and only value of the prediction.
        # prediction = predictions[0]

        # # Get the predicted probabs
        # predicted_probas = model.predict_proba(X)

        # # Get the value of the first, and only, predicted proba.
        # predicted_proba = predicted_probas[0]

        # # The first element in the predicted probabs is % democrat
        # precent_democrat = predicted_proba[0]

        # # The second elemnt in predicted probas is % republican
        # precent_republican = predicted_proba[1]


        # return flask.render_template('index.html', 
        #     input_text=user_input_text,
        #     result=prediction,
        #     precent_democrat=precent_democrat,
        #     precent_republican=precent_republican)




@app.route('/input_values/', methods=['GET', 'POST'])
def input_values():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('input_values.html'))

    if flask.request.method == 'POST':
        # Get the input from the user.
        var_one = flask.request.form['input_variable_one']
        var_two = flask.request.form['another-input-variable']
        var_three = flask.request.form['third-input-variable']

        list_of_inputs = [var_one, var_two, var_three]

        return(flask.render_template('input_values.html', 
            returned_var_one=var_one,
            returned_var_two=var_two,
            returned_var_three=var_three,
            returned_list=list_of_inputs))

    return(flask.render_template('input_values.html'))


@app.route('/images/')
def images():
    return flask.render_template('images.html')


@app.route('/bootstrap/')
def bootstrap():
    return flask.render_template('bootstrap.html')


@app.route('/classify_image/', methods=['GET', 'POST'])
def classify_image():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('classify_image.html'))

    if flask.request.method == 'POST':
        # Get file object from user input.
        file = flask.request.files['file']

        if file:
            # Read the image using skimage
            img = io.imread(file)

            # Resize the image to match the input the model will accept
            img = transform.resize(img, (28, 28))

            # Flatten the pixels from 28x28 to 784x0
            img = img.flatten()

            # Get prediction of image from classifier
            predictions = image_classifier.predict([img])

            # Get the value of the prediction
            prediction = predictions[0]

            return flask.render_template('classify_image.html', prediction=str(prediction))

    return(flask.render_template('classify_image.html'))


if __name__ == '__main__':
    app.run(debug=True)