from flask import Flask, render_template, request
from datetime import datetime
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/support')
def support():
    return render_template('support_form.html')

@app.route('/process', methods=['POST'])
def process_request():
    name = request.form['name']
    email = request.form['email']
    issue = request.form['issue']
    consent = request.form.get('consent')

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    request_id = random.randint(10000, 99999)

    # Mask ALL sensitive data
    masked_name = name[0] + "***"
    masked_email = email[:2] + "****" + email[-4:]

    if not consent:
        with open('data.txt', 'a') as file:
            file.write(
                f"[{timestamp}] REJECTED | "
                f"RequestID: {request_id} | Consent Missing\n"
            )
        return render_template('rejected.html')

    with open('data.txt', 'a') as file:
        file.write(
            f"[{timestamp}] PROCESSED | "
            f"RequestID: {request_id} | "
            f"Name: {masked_name} | "
            f"Email: {masked_email}\n"
        )

    return render_template(
        'processed.html',
        request_id=request_id,
        name=masked_name,
        email=masked_email,
        issue=issue
    )

if __name__ == '__main__':
    app.run(debug=True)
