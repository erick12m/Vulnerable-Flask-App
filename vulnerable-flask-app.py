from flask import Flask,jsonify,render_template_string,request,Response,render_template
import subprocess
from werkzeug.datastructures import Headers
from werkzeug.utils import secure_filename
import sqlite3
from flasgger import Swagger
from flask_apispec import FlaskApiSpec


app = Flask(__name__)
app.config['UPLOAD_FOLDER']="/home/kali/Desktop/upload"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config.update({
    'APISPEC_SPEC': app.config.get('APISPEC_SPEC', {}),
    'APISPEC_SWAGGER_URL': '/swagger/',
})
swagger = Swagger(app)
app.config.update({
    'APISPEC_SWAGGER_UI_URL': app.config.get('APISPEC_SWAGGER_URL') + 'ui/',
})
docs = FlaskApiSpec(app)



@app.route("/")
def main_page():
    # swagger api documentation
    """
    This is the main page of the REST API
    ---
    tags:
      - main_page
    responses:
        200:
            description: The main page of the REST API
            examples:
            application/json: "REST API"
        """
        
    return "REST API"

@app.route("/user/<string:name>")
def search_user(name):
    # swagger api documentation
    """
    This is the search user page of the REST API
    ---
    tags:
        - user
    parameters:
        - name: name
          in: path
          type: string
          required: true
          description: The user name
    responses:
        200:
            description: The user name
            examples:
            application/json: "user name"
        """
    
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    cur.execute("select * from test where username = '%s'" % name)
    data = str(cur.fetchall())
    con.close()
    import logging
    logging.basicConfig(filename="restapi.log", filemode='w', level=logging.DEBUG)
    logging.debug(data)
    return jsonify(data=data),200


@app.route("/welcome/<string:name>")
def welcome(name):
    # swagger api documentation
    """
    This is the welcome page of the REST API
    ---
    tags:
        - welcome
    parameters:
        - name: name
          in: path
          type: string
          required: true
          description: The user name
    responses:
        200:
            description: The welcome message
            examples:
            application/json: "Welcome user name"
        """
    
    data="Welcome "+name
    return jsonify(data=data),200

@app.route("/welcome2/<string:name>")
def welcome2(name):
    # swagger api documentation
    """
    This is the welcome page of the REST API
    ---
    tags:
        - welcome2
    parameters:
        - name: name
          in: path
          type: string
          required: true
          description: The user name
    responses:
        200:
            description: The welcome message
            examples:
            application/json: "Welcome user name"
        """
    
    data="Welcome "+name
    return data

@app.route("/hello")
def hello_ssti():
    # swagger api documentation
    """
    This is the hello page of the REST API
    ---
    tags:
        - hello
    parameters:
        - name: name
          in: query
          type: string
          required: true
          description: The user name
    responses:
        200:
            description: The hello message
            examples:
            application/json: "Hello user name"
        """
    
    if request.args.get('name'):
        name = request.args.get('name')
        template = f'''<div>
        <h1>Hello</h1>
        {name}
</div>
'''
        import logging
        logging.basicConfig(filename="restapi.log", filemode='w', level=logging.DEBUG)
        logging.debug(str(template))
        return render_template_string(template)

@app.route("/get_users")
def get_users():
    # swagger api documentation
    """
    This is the get users page of the REST API
    ---
    tags:
        - get_users
    parameters:
        - name: hostname
          in: query
          type: string
          required: true
          description: The hostname
    responses:
        200:
            description: The users
            examples:
            application/json: "Users"
        """
        
    
    try:
        hostname = request.args.get('hostname')
        command = "dig " + hostname
        data = subprocess.check_output(command, shell=True)
        return data
    except:
        data = str(hostname) + " username didn't found"
        return data

@app.route("/get_log/")
def get_log():
    # swagger api documentation
    """
    This is the get log page of the REST API
    ---
    tags:
        - get_log
    responses:
        200:
            description: The log
            examples:
            application/json: "Log"
        """
    
    try:
        command="cat restapi.log"
        data=subprocess.check_output(command,shell=True)
        return data
    except:
        return jsonify(data="Command didn't run"), 200


@app.route("/read_file")
def read_file():
    # swagger api documentation
    """
    This is the read file page of the REST API
    ---
    tags:
        - read_file
    parameters:
        - name: filename
          in: query
          type: string
          required: true
          description: The filename
    responses:
        200:
            description: The file
            examples:
            application/json: "File"
        """
    
    filename = request.args.get('filename')
    file = open(filename, "r")
    data = file.read()
    file.close()
    import logging
    logging.basicConfig(filename="restapi.log", filemode='w', level=logging.DEBUG)
    logging.debug(str(data))
    return jsonify(data=data),200

@app.route("/deserialization/")
def deserialization():
    # swagger api documentation
    """
    This is the deserialization page of the REST API
    ---
    tags:
        - deserialization
    responses:
        200:
            description: The data
            examples:
            application/json: "Data"
        """
    
    try:
        import socket, pickle
        HOST = "0.0.0.0"
        PORT = 8001
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            connection, address = s.accept()
            with connection:
                received_data = connection.recv(1024)
                data=pickle.loads(received_data)
                return str(data)
    except:
        return jsonify(data="You must connect 8001 port"), 200


@app.route("/get_admin_mail/<string:control>")
def get_admin_mail(control):
    # swagger api documentation
    """
    This is the get admin mail page of the REST API
    ---
    tags:
        - get_admin_mail
    parameters:
        - name: control
          in: path
          type: string
          required: true
          description: The control
    responses:
        200:
            description: The admin mail
            examples:
            application/json: "Admin mail"
        """
        
    
    if control=="admin":
        data="admin@cybersecurity.intra"
        import logging
        logging.basicConfig(filename="restapi.log", filemode='w', level=logging.DEBUG)
        logging.debug(data)
        return jsonify(data=data),200
    else:
        return jsonify(data="Control didn't set admin"), 200

@app.route("/run_file")
def run_file():
    # swagger api documentation
    """
    This is the run file page of the REST API
    ---
    tags:
        - run_file
    parameters:
        - name: filename
          in: query
          type: string
          required: true
          description: The filename
    responses:
        200:
            description: The file
            examples:
            application/json: "File"
        """
        
    try:
        filename=request.args.get("filename")
        command="/bin/bash "+filename
        data=subprocess.check_output(command,shell=True)
        return data
    except:
        return jsonify(data="File failed to run"), 200

@app.route("/create_file")
def create_file():
    # swagger api documentation
    """
    This is the create file page of the REST API
    ---
    tags:
        - create_file
    parameters:
        - name: filename
          in: query
          type: string
          required: true
          description: The filename
        - name: text
          in: query
          type: string
          required: true
          description: The text
    responses:
        200:
            description: The file
            examples:
            application/json: "File"
        """
    
    try:
        filename=request.args.get("filename")
        text=request.args.get("text")
        file=open(filename,"w")
        file.write(text)
        file.close()
        return jsonify(data="File created"), 200
    except:
        return jsonify(data="File didn't create"), 200


connection = {}
max_con = 50

def factorial(number):
    if number == 1:
        return 1
    else:
        return number * factorial(number - 1)


@app.route('/factorial/<int:n>')
def factroial(n:int):
    # swagger api documentation
    """
    This is the factorial page of the REST API
    ---
    tags:
        - factorial
    parameters:
        - name: n
          in: path
          type: integer
          required: true
          description: The number
    responses:
        200:
            description: The factorial
            examples:
            application/json: "Factorial"
        """
        
    
    if request.remote_addr in connection:
        if connection[request.remote_addr] > 2:
            return jsonify(data="Too many req."), 403
        connection[request.remote_addr] += 1
    else:
        connection[request.remote_addr] = 1
    result=factorial(n)
    if connection[request.remote_addr] == 1:
        del connection[request.remote_addr]
    else:
        connection[request.remote_addr] -= 1
    return jsonify(data=result), 200


@app.route('/login',methods=["GET"])
def login():
    # swagger api documentation
    """
    This is the login page of the REST API
    ---
    tags:
        - login
    parameters:
        - name: username
          in: query
          type: string
          required: true
          description: The username
        - name: password
          in: query
          type: string
          required: true
          description: The password
    responses:
        200:
            description: The login
            examples:
            application/json: "Login"
        """
        
    
    username=request.args.get("username")
    passwd=request.args.get("password")
    if "anil" in username and "cyber" in passwd:
        return jsonify(data="Login successful"), 200
    else:
        return jsonify(data="Login unsuccessful"), 403

@app.route('/route')
def route():
    # swagger api documentation
    """
    This is the route page of the REST API
    ---
    tags:
        - route
    parameters:
        - name: route
          in: query
          type: string
          required: true
          description: The route
    responses:
        200:
            description: The route
            examples:
            application/json: "Route"
        """
    
    content_type = request.args.get("Content-Type")
    response = Response()
    headers = Headers()
    headers.add("Content-Type", content_type)
    response.headers = headers
    return response

@app.route('/logs')
def ImproperOutputNeutralizationforLogs():
    # swagger api documentation
    """
    This is the logs page of the REST API
    ---
    tags:
        - logs
    parameters:
        - name: data
          in: query
          type: string
          required: true
          description: The data
    responses:
        200:
            description: The logs
            examples:
            application/json: "Logs"
        """
    
    data = request.args.get('data')
    import logging
    logging.basicConfig(filename="restapi.log", filemode='w', level=logging.DEBUG)
    logging.debug(data)
    return jsonify(data="Logging ok"), 200


@app.route("/user_pass_control")
def user_pass_control():
    # swagger api documentation
    """
    This is the user pass control page of the REST API
    ---
    tags:
        - user_pass_control
    parameters:
        - name: username
          in: query
          type: string
          required: true
          description: The username
        - name: password
          in: query
          type: string
          required: true
          description: The password
    responses:
        200:
            description: The user pass control
            examples:
            application/json: "User pass control"
        """
    
    import re
    username=request.form.get("username")
    password=request.form.get("password")
    if re.search(username,password):
        return jsonify(data="Password include username"), 200
    else:
        return jsonify(data="Password doesn't include username"), 200




@app.route('/upload', methods = ['GET','POST'])
def uploadfile():
    # swagger api documentation
    """
    This is the upload page of the REST API
    ---
    tags:
        - upload
    responses:
        200:
            description: The upload
            examples:
            application/json: "Upload"
        """
    import os
    
    if request.method == 'POST':
      f = request.files['file']
      filename=secure_filename(f.filename)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return 'File uploaded successfully'
    else:
      return '''
<html>
   <body>
      <form  method = "POST"  enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>   
   </body>
</html>


      '''

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8081)
