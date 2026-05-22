from flask import Flask, render_template, request, redirect, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "secretkey"


# MYSQL CONFIG

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'phonebook'

mysql = MySQL(app)


# HOME PAGE

@app.route('/')
def home():

    return render_template('login.html')


# REGISTER

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s",
            [username]
        )

        existing = cur.fetchone()

        if existing:

            return "Username Already Exists"

        hashed_password = generate_password_hash(password)

        cur.execute("""

        INSERT INTO users(
        username,
        password
        )

        VALUES(%s,%s)

        """, (

            username,
            hashed_password

        ))

        mysql.connection.commit()

        cur.close()

        return redirect('/')

    return render_template('register.html')


# LOGIN

@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=%s",
        [username]
    )

    user = cur.fetchone()

    cur.close()

    if user and check_password_hash(user[2], password):

        session['user_id'] = user[0]

        return redirect('/dashboard')

    return "Invalid Username or Password"


# DASHBOARD

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:

        return redirect('/')

    cur = mysql.connection.cursor()

    cur.execute("""

    SELECT *

    FROM contacts

    WHERE user_id=%s

    ORDER BY name ASC

    """, [session['user_id']])

    contacts = cur.fetchall()

    cur.close()

    return render_template(
        'dashboard.html',
        contacts=contacts
    )


# ADD CONTACT

@app.route('/add_contact', methods=['POST'])
def add_contact():

    if 'user_id' not in session:

        return redirect('/')

    try:

        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        company = request.form['company']
        address = request.form['address']
        category = request.form['category']

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM contacts WHERE phone=%s",
            [phone]
        )

        existing = cur.fetchone()

        if existing:

            return "Phone number already exists!"

        cur.execute("""

        INSERT INTO contacts(

        name,
        phone,
        email,
        company,
        address,
        category,
        user_id

        )

        VALUES(%s,%s,%s,%s,%s,%s,%s)

        """, (

            name,
            phone,
            email,
            company,
            address,
            category,
            session['user_id']

        ))

        mysql.connection.commit()

        cur.close()

        return redirect('/dashboard')

    except Exception as e:

        return str(e)


# DELETE CONTACT

@app.route('/delete/<int:id>')
def delete(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE id=%s",
        [id]
    )

    mysql.connection.commit()

    cur.close()

    return redirect('/dashboard')


# FAVORITE

@app.route('/favorite/<int:id>')
def favorite(id):

    cur = mysql.connection.cursor()

    cur.execute("""

    UPDATE contacts

    SET favorite = NOT favorite

    WHERE id=%s

    """, [id])

    mysql.connection.commit()

    cur.close()

    return redirect('/dashboard')


# SEARCH

@app.route('/search')
def search():

    if 'user_id' not in session:

        return jsonify([])

    query = request.args.get('query')

    cur = mysql.connection.cursor()

    sql = """

    SELECT *

    FROM contacts

    WHERE user_id=%s

    AND (

    name LIKE %s OR
    phone LIKE %s OR
    email LIKE %s OR
    company LIKE %s

    )

    """

    search = "%" + query + "%"

    cur.execute(sql, (

        session['user_id'],

        search,
        search,
        search,
        search

    ))

    contacts = cur.fetchall()

    cur.close()

    data = []

    for c in contacts:

        data.append({

            'name': c[1],
            'phone': c[2],
            'email': c[3],
            'company': c[4]

        })

    return jsonify(data)


# LOGOUT

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


# RUN

if __name__ == '__main__':

    app.run(debug=False)