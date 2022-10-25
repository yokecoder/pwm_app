

from flask import Flask,render_template,redirect,request,url_for
from pwm_sqlite_db import pwmDB,lower_strip
import webbrowser as  w

#

app = Flask(__name__)
app.config["secret_key"] = "ahshs jsjssj jskss"

pwmd = pwmDB("db1.sqlite","passwords")





@app.route("/")
def main():
    return render_template("index.html")

@app.route("/p")
def view_pswd():
    return render_template("passwords.html",pwm_list=pwmd.getAllData(),pwm_dict=pwmd.GetDict())


@app.route("/update/<key>" ,methods=['POST','GET'])
def update_pass(key):
    if request.method == "POST":
        key = request.form.get("key")
        newp = request.form.get("passw")
        
        pwmd.updateData(key=key,new_passw=newp)
        return redirect("/p")
    else: 
        return render_template("update.html",key=key,allkeys = pwmd.getKeys(),alldata = pwmd.getAllData())


## API METHODS 



@app.route("/add_passw",methods = ["POST", "GET"])
def addp():
    
    if request.method == "POST":
        key = request.form.get("key")
        
        passw = request.form.get("passw")
        
        if request.form['action'] == "Add New":
            pwmd.addData(key=lower_strip(key),passw=passw)
        
        elif request.form["action"] == "Edit":
            pwmd.updateData(key=lower_strip(key),new_passw=passw)
        
        return redirect("/")


@app.route("/del_all_",methods = ["POST", "GET"])
def del_all_():
    
    if request.method == "POST":
        pwmd.removeAllData()
        return redirect("/p")
    
    else:
        return " Error Page Not Found "
    
        
@app.route("/del/<key>")
def delpass(key):
    pwmd.removeData(key=key)
    return redirect("/p")
    



if __name__ == "__main__":
    #w.open("http://localhost:5000/")
   
    app.run(debug=True,port=5000)

    
    

