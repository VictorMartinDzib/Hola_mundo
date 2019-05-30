from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__) #Nuevo objeto

#Conexion a mysql
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)


#sesion
app.secret_key = 'mysecretkey'


@app.route("/") #wrap o un decorador
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts")
    data = cur.fetchall()
    print(data)
    return render_template('index.html', contacts = data)

#Metodo para recibir los datos
@app.route("/add_contact", methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        print(fullname, phone, email)

        #cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)", (fullname, phone, email))
        mysql.connection.commit()
        #cur.close()

        #redireccionando a la vista inicial
        flash("Contact Added Successfully!")
        return redirect(url_for('index'))

@app.route("/edit/<string:id>")
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = {0} ".format(id))
    data = cur.fetchall()
    #print(data[0])
    return render_template('edit_contact.html', contacts = data[0])
    
@app.route("/update/<string:id>", methods=['POST'])
def update(id):    
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']   

        cur = mysql.connection.cursor()
        cur.execute(""" 
                UPDATE contacts SET fullname = %s, 
                phone = %s, 
                email = %s
                WHERE id = %s
        """, (fullname, phone, email, id))
        mysql.connection.commit()
        flash("contact updated succesfully")
        return redirect(url_for('index'))

@app.route("/delete/<string:id>")
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash("Contact removed succesfully")
    return redirect(url_for('index'))
    

if __name__ == "__main__":
    app.run(debug = True) #se encarga de ejecutar el servidor