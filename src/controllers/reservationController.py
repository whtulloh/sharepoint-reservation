import requests
from src.services.sharepointService import get_user, generate_demo_reservation, update_user, get_all_user
from flask import Flask, request, jsonify, make_response

def set_response_headers(response, code):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response, code

def set_response_body(data, successCode):
    if (('error' in data)):
        code = 400
    else:
        code = successCode
    
    response = make_response(jsonify(data), code)
    response = set_response_headers(response, code)

    return response

def getAllData():
    try:
        data = get_all_user()
        return set_response_body(data, 200)
    except Exception as e:
        return jsonify(error=str(e)), 400

def getData(accnumber):
    try:
        data = get_user(accnumber)
        return set_response_body(data, 200) 
    except Exception as e:
        # Return an error message and a 400 status code if there was an error with the data
        return jsonify(error=str(e)), 400

def updateData(accnumber):
    try:
        request_data = request.get_data()
        data = update_user(accnumber, request_data)
        return set_response_body(data, 201) 
    except Exception as e:
        # Return an error message and a 400 status code if there was an error with the data
        return jsonify(error=str(e)), 400

def getHook():
    try:
        data = "Hello"
        return set_response_body(data, 200)
    except Exception as e:
        return jsonify(error=str(e)), 400