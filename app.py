from flask import Flask, render_template, request, redirect, url_for, flash,jsonify,make_response,session
from firebase import firebase
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import datetime
from firebase_admin import storage, credentials
from werkzeug import secure_filename
import firebase_admin
from return_json import return_json,return_json_for_admin
import os
import sys
import json
import requests

firebase = firebase.FirebaseApplication(
    'https://test-database-anres.firebaseio.com', None)
app = Flask(__name__)

app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

def set_susname(susname):
    for i in range(len(susname)):
            if len(susname[i].split('_')) > 1:
                susname[i] = susname[i].split('_')[0] + ' '  + susname[i].split('_')[1]
    return susname

@app.route("/")
def Home():
    return render_template('Home.html')


@app.route("/Search/user")
def Searchuser():
    return render_template('searchuser.html')


@app.route("/Search/suspect")
def Searchsuspect():
    return render_template('searchsuspect.html')


@app.route("/Search/case")
def Searchcase():
    return render_template('searchcase.html')


@app.route("/Search/date")
def Searchdate():
    return render_template('searchdate.html')


@app.route("/Search/type")
def Searchtype():
    return render_template('searchtype.html')


@app.route("/InformationFromSuspect_API", methods=['GET'])
def API_Showsusname():
    # try:
        fname = request.args.get('fname')
        sname = request.args.get('sname')
        susfname = fname
        suslname = sname
        Susname = susfname+' '+suslname
        # print(Susname)
        Susname1 = susfname+'_'+suslname
        result = firebase.get('/users', None)
        # print(result)
        # name = []
        sussocial = []
        case = []
        susname = []
        socialtype = []
        count = []
        date = []
        key = []
        gender = []
        age = []
        i = 0
        for Info in result:
            if (result[Info] != None):
                for ii in result[Info]:
                    if ii == "Susname":
                        if (result[Info][ii].lower() == Susname.lower() or result[Info][ii].lower() == Susname1.lower()):
                            # if "Name" in result[Info]:
                            #     name.append(result[Info]["Name"])
                            # else:
                            #     name.append("NO Info")
                            if "Case" in result[Info]:
                                case.append(result[Info]["Case"])
                            else:
                                case.append("NO Info")
                            if "Susname" in result[Info]:
                                susname.append(result[Info]["Susname"])
                            else:
                                susname.append("NO Info")
                            if "Sussocial" in result[Info]:
                                sussocial.append(result[Info]["Sussocial"])
                            else:
                                sussocial.append("NO Info")
                            if "Type" in result[Info]:
                                socialtype.append(result[Info]["Type"])
                            else:
                                socialtype.append("NO Info")
                            if "Gender" in result[Info]:
                                if(result[Info]["Gender"] == "M"):
                                    gender.append("Male")
                                elif (result[Info]["Gender"] == "F"):
                                    gender.append("Female")
                                else:
                                    gender.append("Alternative")
                                # gender.append(result[Info]["Gender"])
                            else:
                                gender.append("NO Info")
                            if "Age" in result[Info]:
                                age.append(result[Info]["Age"])
                            else:
                                age.append("NO Info")
                            sp = Info.split("-")
                            d = sp[2]+'/'+sp[1]+'/20'+sp[0]
                            date.append(d)
                            key.append(Info)
                            count.append(i)
                            i += 1
        susname = set_susname(susname)
        resp = make_response(return_json(case, susname, sussocial, socialtype, gender,age))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    # except:
    #     return render_template('no_data.html')

@app.route("/InformationFromCase_API", methods=['GET'])
def API_Showcase():
    try:
        casee = request.args.get('case')
        Case = casee.lower()
        result = firebase.get('/users', None)
        # name = []
        sussocial = []
        case = []
        susname = []
        socialtype = []
        count = []
        date = []
        key = []
        gender = []
        age =[]
        i = 0
        for Info in result:
            if (result[Info] != None):
                if ((result[Info]['Case']).lower() == Case.lower()):
                    # if "Name" in result[Info]:
                    #     name.append(result[Info]["Name"])
                    # else:
                    #     name.append("NO Info")
                    if "Case" in result[Info]:
                        case.append(result[Info]["Case"])
                    else:
                        case.append("NO Info")
                    if "Susname" in result[Info]:
                        susname.append(result[Info]["Susname"])
                    else:
                        susname.append("NO Info")
                    if "Sussocial" in result[Info]:
                        sussocial.append(result[Info]["Sussocial"])
                    else:
                        sussocial.append("NO Info")
                    if "Type" in result[Info]:
                        socialtype.append(result[Info]["Type"])
                    else:
                        socialtype.append("NO Info")
                    if "Gender" in result[Info]:
                        if(result[Info]["Gender"] == "M"):
                            gender.append("Male")
                        elif (result[Info]["Gender"] == "F"):
                            gender.append("Female")
                        else:
                            gender.append("Alternative")
                        # gender.append(result[Info]["Gender"])
                    else:
                        gender.append("NO Info")
                    if "Age" in result[Info]:
                        age.append(result[Info]["Age"])
                    else:
                        age.append("NO Info")
                    sp = Info.split("-")
                    
                    d = sp[2]+'/'+sp[1]+'/20'+sp[0]
                    
                    date.append(d)
                    key.append(Info)
                    count.append(i)
                    i += 1

        susname = set_susname(susname)
        resp = make_response(return_json(case, susname, sussocial, socialtype, gender,age))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    except:
        # flash("Don't Have any Day that you want")
        return render_template('no_data.html')


@app.route("/InformationFromDate_API", methods=['GET'])
def API_Showdate():
    Date = request.args.get('date')
    # Date = date
    try:
        result = firebase.get('/users', None)
        # name = []
        sussocial = []
        case = []
        susname = []
        socialtype = []
        count = []
        date = []
        key = []
        gender = []
        age = []
        i = 0
        for Info in result:
            sp = Info.split("-")
            dsp = Date.split("_")
            if len(dsp[0]) < 2:
                dsp[0] = '0'+(dsp[0])
            if len(dsp[1]) < 2:
                dsp[1] = '0'+(dsp[1])
            if ((dsp[0] == sp[2]) and (dsp[1] == sp[1]) and (dsp[2] == sp[0])):
                if (result[Info] != None):
                    # if "Name" in result[Info]:
                    #     name.append(result[Info]["Name"])
                    # else:
                    #     name.append("NO Info")
                    if "Case" in result[Info]:
                        case.append(result[Info]["Case"])
                    else:
                        case.append("NO Info")
                    if "Susname" in result[Info]:
                        susname.append(result[Info]["Susname"])
                    else:
                        susname.append("NO Info")
                    if "Sussocial" in result[Info]:
                        sussocial.append(result[Info]["Sussocial"])
                    else:
                        sussocial.append("NO Info")
                    if "Type" in result[Info]:
                        socialtype.append(result[Info]["Type"])
                    else:
                        socialtype.append("NO Info")
                    if "Gender" in result[Info]:
                        if(result[Info]["Gender"] == "M"):
                            gender.append("Male")
                        elif (result[Info]["Gender"] == "F"):
                            gender.append("Female")
                        else:
                            gender.append("Alternative")
                        # gender.append(result[Info]["Gender"])
                    else:
                        gender.append("NO Info")
                    if "Age" in result[Info]:
                        age.append(result[Info]["Age"])
                    else:
                        age.append("NO Info")
                    d = sp[2]+'/'+sp[1]+'/20'+sp[0]
                    date.append(d)
                    key.append(Info)
                    count.append(i)
                    i += 1
        susname = set_susname(susname)
        resp = make_response(return_json(case, susname, sussocial, socialtype, gender,age))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except:
        # flash("Don't Have any Day that you want")
        return render_template('no_data.html')


@app.route("/InformationFromType_API", methods=['GET'])
def API_Showtype():
    try:
        typee = request.args.get('type')
        sussocialinp = request.args.get('sussocialinp')
        result = firebase.get('/users', None)
        Type = typee
        # if (Type == "Facebook"):
        #     Sussocial = request.form['Susfacebook']
        # elif (Type == "E-mail"):
        #     Sussocial = request.form['Susemail']
        # elif (Type == "Website"):
        #     Sussocial = request.form['Susurl']
        # else:
        #     Sussocial = request.form['Susline']
        Sussocial = sussocialinp
        # name = []
        sussocial = []
        case = []
        susname = []
        socialtype = []
        count = []
        date = []
        key = []
        gender = []
        age = []
        i = 0
        for Info in result:
            if (result[Info] != None):
                # print(result[Info]["Type"].lower(),file=sys.stderr)
                if (result[Info]["Type"].lower() == Type.lower()):
                    if (result[Info]["Sussocial"] == Sussocial):
                        # if "Name" in result[Info]:
                        #     name.append(result[Info]["Name"])
                        # else:
                        #     name.append("NO Info")
                        if "Case" in result[Info]:
                            case.append(result[Info]["Case"])
                        else:
                            case.append("NO Info")
                        if "Susname" in result[Info]:
                            susname.append(result[Info]["Susname"])
                        else:
                            susname.append("NO Info")
                        if "Sussocial" in result[Info]:
                            sussocial.append(result[Info]["Sussocial"])
                        else:
                            sussocial.append("NO Info")
                        if "Type" in result[Info]:
                            socialtype.append(result[Info]["Type"])
                        else:
                            socialtype.append("NO Info")
                        if "Gender" in result[Info]:
                            if(result[Info]["Gender"] == "M"):
                                gender.append("Male")
                            elif (result[Info]["Gender"] == "F"):
                                gender.append("Female")
                            else:
                                gender.append("Alternative")
                            # gender.append(result[Info]["Gender"])
                        else:
                            gender.append("NO Info")
                        if "Age" in result[Info]:
                            age.append(result[Info]["Age"])
                        else:
                            age.append("NO Info")
                        sp = Info.split("-")
                        d = sp[2]+'/'+sp[1]+'/20'+sp[0]
                        date.append(d)
                        key.append(Info)
                        count.append(i)
                        i += 1
        susname = set_susname(susname)
        resp = make_response(return_json(case, susname, sussocial, socialtype,gender,age))
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except:
        return render_template('no_data.html')


@app.route("/ShowAll")
def showData():
    result = firebase.get('/users', None)
    name = []
    sussocial = []
    age = []
    case = []
    susname = []
    socialtype = []
    count = []
    date = []
    other = []
    email = []
    tel = []
    key = []
    gender = []
    age = []
    image = []
    i = 0
    for Info in result:
        if result[Info] != None:
            if "Name" in result[Info]:
                name.append(result[Info]["Name"])
            else:
                name.append("NO Info")
            if "Case" in result[Info]:
                case.append(result[Info]["Case"])
            else:
                case.append("NO Info")
            if "Susname" in result[Info]:
                # temp = result[Info]["Susname"].split('_')
                # nt = temp[0]+" "+temp[1]
                # susname.append(nt)
                susname.append(result[Info]["Susname"])
            else:
                susname.append("NO Info")
            if "Sussocial" in result[Info]:
                sussocial.append(result[Info]["Sussocial"])
            else:
                sussocial.append("NO Info")
            if "Type" in result[Info]:
                socialtype.append(result[Info]["Type"])
            else:
                socialtype.append("NO Info")
            if "Age" in result[Info]:
                age.append(result[Info]["Age"])
            else:
                age.append("NO Info")
            if "Other" in result[Info]:
                other.append(result[Info]["Other"])
            else:
                other.append("NO Info")
            if "E-mail" in result[Info]:
                email.append(result[Info]["E-mail"])
            else:
                email.append("NO Info")
            if "Tel" in result[Info]:
                tel.append(result[Info]["Tel"])
            else:
                tel.append("NO Info")
            if "Image1" in result[Info]:
                image.append(result[Info]["Image1"])
            else:
                image.append("https://upload.wikimedia.org/wikipedia/en/6/60/No_Picture.jpg")
            if "Gender" in result[Info]:
                if(result[Info]["Gender"] == "M"):
                    gender.append("Male")
                elif (result[Info]["Gender"] == "F"):
                    gender.append("Female")
                else:
                    gender.append("Alternative")
                # # gender.append(result[Info]["Gender"])
            else:
                gender.append("NO Info")
            sp = Info.split("-")
            d = sp[2]+'/'+sp[1]+'/20'+sp[0]
            date.append(d)
            key.append(Info)
            count.append(i)
            i += 1
    susname = set_susname(susname)
    return render_template('index.html', name=name, case=case, susname=susname, sussocial=sussocial, socialtype=socialtype, date=date, count=count, key=key, age=age, other=other, email=email, tel=tel, gender = gender, image = image)

@app.route("/ShowAll_API",methods = ['GET'])
def APIshowData():
    result = firebase.get('/users', None)
    name = []
    sussocial = []
    age = []
    case = []
    susname = []
    socialtype = []
    count = []
    date = []
    other = []
    email = []
    tel = []
    key = []
    gender = []
    age = []
    image = []
    i = 0
    for Info in result:
        if result[Info] != None:
            if "Name" in result[Info]:
                name.append(result[Info]["Name"])
            else:
                name.append("NO Info")
            if "Case" in result[Info]:
                case.append(result[Info]["Case"])
            else:
                case.append("NO Info")
            if "Susname" in result[Info]:
                # temp = result[Info]["Susname"].split('_')
                # nt = temp[0]+" "+temp[1]
                # susname.append(nt)
                susname.append(result[Info]["Susname"])
            else:
                susname.append("NO Info")
            if "Sussocial" in result[Info]:
                sussocial.append(result[Info]["Sussocial"])
            else:
                sussocial.append("NO Info")
            if "Type" in result[Info]:
                socialtype.append(result[Info]["Type"])
            else:
                socialtype.append("NO Info")
            if "Age" in result[Info]:
                age.append(result[Info]["Age"])
            else:
                age.append("NO Info")
            if "Other" in result[Info]:
                other.append(result[Info]["Other"])
            else:
                other.append("NO Info")
            if "E-mail" in result[Info]:
                email.append(result[Info]["E-mail"])
            else:
                email.append("NO Info")
            if "Tel" in result[Info]:
                tel.append(result[Info]["Tel"])
            else:
                tel.append("NO Info")
            k = 1
            while True:
                img_name = "Image"+str(k)
                if "Image1" not in result[Info]:
                    image.append("No Info")
                    break
                elif img_name in result[Info]:
                    image.append(result[Info][img_name])
                    k+=1
                else:
                    break
            if "Gender" in result[Info]:
                if(result[Info]["Gender"] == "M"):
                    gender.append("Male")
                elif (result[Info]["Gender"] == "F"):
                    gender.append("Female")
                else:
                    gender.append("Alternative")
                # # gender.append(result[Info]["Gender"])
            else:
                gender.append("NO Info")
            sp = Info.split("-")
            d = sp[2]+'/'+sp[1]+'/20'+sp[0]
            date.append(d)
            key.append(Info)
            count.append(i)
            i += 1
    susname = set_susname(susname)
    resp = make_response(return_json_for_admin(name, case, susname, sussocial, socialtype, gender,age,image))
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
    # return result

@app.route("/ThankYou")
def thank():
    return render_template("Thanks.html")

@app.route("/insert", methods=['POST'])
def insert():
    # return "hello"
    # print('Success',file=sys.stderr)
    if request.method == 'POST':
        userfname = request.form['userfname']
        userlname = request.form['userlname']
        useremail = request.form['useremail']
        userage = request.form['userage']
        usertel = request.form['usertel']
        CaseType = request.form['Type']
        Case = request.form['Case']
        Susfname = request.form['Susfname']
        Suslname = request.form['Suslname']
        Other = request.form['Other']
        Gender = request.form['Gender']
        username = userfname+' '+userlname
        if (CaseType == "Facebook"):
            Sussocial = request.form['Susfacebook']
        elif (CaseType == "E-mail"):
            Sussocial = request.form['Susemail']
        elif (CaseType == "Website"):
            Sussocial = request.form['Susurl']
        else:
            Sussocial = request.form['Susline']
        if ((Susfname != '-') and (Suslname != '-')):
            Susname = Susfname+' '+Suslname
        else:
            Susname = '-'
        time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")

        pth = '/users/'+time
        
        firebase.put(pth, name="Name", data=username)
        firebase.put(pth, name="E-mail", data=useremail)
        firebase.put(pth, name="Tel", data=usertel)
        firebase.put(pth, name="Age", data=userage)
        firebase.put(pth, name="Type", data=CaseType)
        firebase.put(pth, name="Sussocial", data=Sussocial)
        firebase.put(pth, name="Susname", data=Susname)
        firebase.put(pth, name="Case", data=Case)
        firebase.put(pth, name="Other", data=Other)
        firebase.put(pth, name="Gender", data=Gender)

        # return "hello"

        current_path = os.path.abspath(':')
        current_path = current_path.split(":")[0]

        
        name_sum = userfname+'_'+userlname
        # img = request.files['image']
        img = request.files.getlist("image")
        # img = request.files("image")
        k = 1
        
        try:
            cred = credentials.Certificate(
                current_path+'mysite/anres-test-firebase-adminsdk-4z967-07c79cd90f.json')
        except Exception:
            cred = credentials.Certificate(
                'anres-test-firebase-adminsdk-4z967-07c79cd90f.json')

        firebase_admin.initialize_app(
            cred, {'storageBucket': 'anres-test.appspot.com'})
        
        for i in img:

            fille = i
            filenames = photos.save(fille,name=(time+"_T_"+fille.filename))
            
            # filename = secure_filename(i.filename)
            # i.save('upload/'+name_sum+"_"+time+filenames+"_"+str(k))
            
            bucket = storage.bucket()
            blob = bucket.blob(name_sum+'/'+time+"T"+filenames)
            # blob.upload_from_filename('../uploads/'+name_sum+"_"+time+filenames+"_"+str(k))

            blob.upload_from_filename(current_path+'uploads/'+time+"_T_"+fille.filename)
            blob.make_public()
            
            firebase.put(pth,name="Image"+str(k), data=blob.public_url)
            k += 1
            os.remove(os.getcwd() + '/uploads/'+time+"_T_"+fille.filename)

        return  render_template("Thanks.html")


@app.route("/delete/<string:key_data>", methods=['GET'])
def delete(key_data):
    firebase.delete('/users', key_data)
    return redirect(url_for('showData'))

@app.route("/ShowGraph")		
def showgraph():		
    return render_template("Graph.html")

@app.route("/InsertData")		
def showForm():		
    return render_template('Report.html')

@app.route("/SuspectShow")		
def susshow():		
    return render_template('Suspect.html')


# @app.route("/update", methods=['POST'])
# def update():
#     if request.method == 'POST':
#         updatekey = request.form['id']
#         userfname = request.form['userfname']
#         userlname = request.form['userlname']
#         userage = request.form['userage']
#         useremail = request.form['useremail']
#         usertel = request.form['usertel']
#         CaseType = request.form['Type']
#         Case = request.form['Case']
#         Sussocial = request.form['Sussocial']
#         Susfname = request.form['Susfname']
#         Suslname = request.form['Suslname']
#         Other = request.form['Other']
#         username = userfname+'_'+userlname
#         if ((Susfname != '-') and (Suslname)):
#             Susname = Susfname+'_'+Suslname
#         else:
#             Susname = '-'
#         pth = '/users/'+(updatekey)
#         firebase.put(pth, name="Name", data=username)
#         firebase.put(pth, name="E-mail", data=useremail)
#         firebase.put(pth, name="Tel", data=usertel)
#         firebase.put(pth, name="Age", data=userage)
#         firebase.put(pth, name="Type", data=CaseType)
#         firebase.put(pth, name="Sussocial", data=Sussocial)
#         firebase.put(pth, name="Susname", data=Susname)
#         firebase.put(pth, name="Case", data=Case)
#         firebase.put(pth, name="Other", data=Other)
#         return redirect(url_for('showData'))

@app.route("/urlcheck")
def urlcheck():
    alert = 2
    status = request.args.get('status')
    check = request.args.get('link')
    if status is None:
        status = ""
    elif status == "eKfeoLK":
        status = '"'+check+'" ไม่มีในฐานข้อมูล'
        alert = 0
    elif status == "KfekaKL":
        status = '"'+check+'" มีความน่าจะเป็นสูงที่จะเป็นฟิชชิ่ง'
        alert = 1
    else:
        status = ""
    return render_template("detection.html",status=status,alert=alert)


@app.route("/check_phishing",methods=['POST'])
def check_phishing():
    result = None
    if request.method == 'POST':
        check = request.form['detect']
        if(check[:5] == "http:"):
            url = check.split('/')
            url = url[2]
            if url[:3] == "www":
                url = url.split('.')[1:]
            else:
                url = url.split('.')
            ans = ''
            for i in url:
                ans += i+'_'
            ans = ans[:len(ans)-1]
            result = firebase.get("/phishing_data",ans)
            print(ans,file=sys.stderr)
        elif(check[:5] == "https"):
            url = check.split('/')
            url = url[2]
            if url[:3] == "www":
                url = url.split('.')[1:]
            else:
                url = url.split('.')
            ans = ''
            for i in url:
                ans += i+'_'
            ans = ans[:len(ans)-1]
            result = firebase.get("/phishing_data",ans)
            print(url,file=sys.stderr)
        elif(check[:4] != 'www.'):
            url = check
            url = url.split('.')
            ans = ''
            for i in url:
                ans += i+'_'
            ans = ans[:len(ans)-1]
            result = firebase.get("/phishing_data",ans)
            print(result,file=sys.stderr)
        else:
            url = check
            url = url.split('.')
            url[0] = ''
            ans = ''
            for i in url:
                ans += i+'_'
            ans = ans[1:len(ans)-1]
            result = firebase.get("/phishing_data",ans)
            # print(ans,file=sys.stderr)
        if result is None:
            return redirect(url_for("urlcheck",status= "eKfeoLK",link=check))
            # return render_template('detection.html',status = "เว็ปนีไซต์นี้ไม่มีในฐานข้อมูล")
        else:
            return redirect(url_for("urlcheck",status= "KfekaKL",link=check))
            # return render_template('detection.html',status = "เว็ปนี้มีในฐานข้อมูล")

@app.route("/check_phishing_API",methods=['GET'])
def API_check_phishing():
    result = None
    if request.method == 'GET':
        check = request.args.get('link')
        if(check[:4] == "http"):
            url = check.split('/')
            url = url[2]
            url = url.split('.')[1:]
            ans = ''
            for i in url:
                ans += i+'_'
            ans = ans[:len(ans)-1]
            result = firebase.get("/phishing_data",ans)
            print(ans,file=sys.stderr)
        elif(check[:4] != 'www.'):
            url = check
            url = url.split('.')
            ans = ''
            for i in url:
                ans += i+'_'
            ans = ans[:len(ans)-1]
            result = firebase.get("/phishing_data",ans)
            print(result,file=sys.stderr)
        else:
            url = check
            url = url.split('.')
            url[0] = ''
            ans = ''
            for i in url:
                ans += i+'_'
            ans = ans[1:len(ans)-1]
            result = firebase.get("/phishing_data",ans)
            # print(ans,file=sys.stderr)
        if result is None:
            # return redirect(url_for("urlcheck",status= "eKfeoLK",link=check))
            resp = make_response("0")
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers["Access-Control-Allow-Methods"] = '*'
            resp.headers["Access-Control-Allow-Header"] = "*"
            return resp
        else:
            # return redirect(url_for("urlcheck",status= "KfekaKL",link=check))
            resp = make_response("1")
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers["Access-Control-Allow-Methods"] = '*'
            resp.headers["Access-Control-Allow-Header"] = "*"
            return resp


if __name__ == "__main__":
    # port = int(os.getenv('PORT', 5000))

    # print("Starting app on port %d" % port)

    # app.run(debug=True, port=port, host='0.0.0.0', threaded=True)

    app.run(debug=True)
