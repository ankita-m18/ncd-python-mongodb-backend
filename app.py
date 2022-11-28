from flask import Flask, jsonify, request, redirect
from flask.helpers import url_for
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from bson.objectid import ObjectId
from random import randint

app = Flask(__name__)
cors = CORS(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ncdspringbootbackend'
app.config['CORS_Headers'] = 'Content-Type'
mongo = PyMongo(app)

# patientid 
@app.route('/search', methods = ['GET'])
def retrieveAll():
    holder = list()
    currentCollection = mongo.db.patient_info
    for i in currentCollection.find():
        holder.append({'patientid':i['patientid'],'firstname':i['firstname'], 'lastname':i['lastname'], 'phone':i['phone'], 'gender':i['gender'], 'birthday':i['birthday'], 'pincode':i['pincode'], 'score':i['score'], 'screening':i['screening']})
    return jsonify(holder)

@app.route('/search/firstname/<firstname>', methods = ['GET'])
@cross_origin()
def retrieveFromFirstName(firstname):
    print(f"the value of firstname :{firstname}")
    holder = list()
    currentCollection = mongo.db.patient_info
    datas = currentCollection.find({"firstname" : firstname})
    for data in datas:
        holder.append({'patientid' : data['patientid'],'firstname' : data['firstname'],'lastname' : data['lastname'],'phone' : data['phone'], 'gender' : data['gender'], 'birthday' : data['birthday'],'pincode' : data['pincode'],'score' : data['score'],'screening' : data['screening']})
    return jsonify(holder)

@app.route('/search/lastname/<lastname>', methods = ['GET'])
@cross_origin()
def retrieveFromLastName(lastname):
    holder = list()
    currentCollection = mongo.db.patient_info
    datas = currentCollection.find({"lastname" : lastname})
    for data in datas:
        holder.append({'patientid' : data['patientid'],'firstname' : data['firstname'],'lastname' : data['lastname'],'phone' : data['phone'], 'gender' : data['gender'], 'birthday' : data['birthday'],'pincode' : data['pincode'],'score' : data['score'],'screening' : data['screening']})
    return jsonify(holder)

@app.route('/search/id/<patientid>', methods = ['GET'])
@cross_origin()
def retrieveFrompatId(patientid):
    print(f"this is tha value of aptient id {patientid}")
    currentCollection = mongo.db.patient_info
    holder = list()
    #patientid = request.json['patientid']
    i = currentCollection.find_one({"patientid" : patientid})
    holder.append({'patientid':i['patientid'],'firstname':i['firstname'], 'lastname':i['lastname'], 'phone':i['phone'], 'gender':i['gender'], 'birthday':i['birthday'], 'pincode':i['pincode'], 'score':i['score'], 'screening':i['screening']})
    return jsonify(holder)


@app.route('/postData', methods = ['POST'])
def postData():
    currentCollection = mongo.db.patient_info
    # global patientid
    # patientid = randint(10000000000000,99999999999999)

    patientid = request.json['patientid']
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    # phone = request.json['phone']
    gender = request.json['gender']
    phone = request.json['phone']
    birthday = request.json['birthday']
    pincode = request.json['pincode']
    score = request.json['score']
    screening = request.json['screening']
    print("post method is calling ")

    currentCollection.insert_one({'patientid': patientid , 'firstname' : firstname, 'lastname' : lastname, 'phone' : phone,'gender':gender,'birthday': birthday, 'pincode' : pincode , 'score': score, 'screening' : screening })
    return  jsonify({ 'firstname' : firstname, 'lastname' : lastname, 'phone' : phone,'gender' : gender, 'birthday' : birthday, 'pincode' : pincode})
    
@app.route('/deleteData/<firstname>', methods = ['DELETE'])
def deleteData(firstname):
    currentCollection = mongo.db.patient_info
    currentCollection.delete_one({'firstname' : firstname})
    return redirect(url_for('retrieveAll'))

@app.route('/update/<patientid>', methods = ['PUT'])
def updateData(patientid):

    currentCollection = mongo.db.patient_info
    print("this is update function ")
    # param = request.json['param']
    # patientid1 = request.json['patientid']
    patientid1 = request.json['patientid']
    score = request.json['score']
    screening = request.json['screening']
    print("$%$$$$$$$$$$$$$$$$$$$$$$$$$$$$$^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^%")
    print("this is score of global patientid  value:  ",patientid)
    print("this is score of global patientid  value:  ",patientid1)
    print("this is score of global patientid  value score value :  ",score)
    print("this is patientid  value:  ",screening)
    # age = request.json['age']
    # smoke = request.json['smoke']
    # alcohol = request.json['alcohol']
    # waist = request.json['waist']
    # phy_act = request.json['phy_act']
    # fam_his = request.json['fam_his']
    # print(type(age))
    # score = int(age)+int(smoke)+int(alcohol)+int(waist)+int(phy_act)+int(fam_his)
    # score = age+smoke+alcohol+waist+phy_act+fam_his
    # screening = ""
    # if score>4:
    #     screening = "screening"
    # else:
    #     screening = "No screening"

    print("this is score value :",score)
    print("this is screening value :",screening)
    print("%%%%%%%%%%%%%%%%%%%%%%%% ")

    print(currentCollection.update_one({'patientid':patientid1}, {"$set": {"score" :score,"screening" :screening}}))
    try:

        currentCollection.update_one({'patientid':patientid1}, {"$set": {"score" :score,"screening" :screening}})
        msg="update done "
        print(msg)
    except:
        print("exception called")
    msg="update done "
    return msg

if __name__ == '__main__':
    app.run(debug = True,port=5000)