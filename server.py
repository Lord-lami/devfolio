from flask import Flask, render_template, send_from_directory, request, redirect
import csv
from email.message import EmailMessage
import smtplib
from string import Template
from pathlib import Path

app = Flask(__name__)


@app.route('/')
def home():
	return render_template('./index.html')


@app.route('/thankyou.html')
def display():
	return render_template('./thankyou.html')

def write_to_csv(data):
	with open('database.csv', 'a') as database:
		name = data['name']
		email = data['email']
		subject = data['subject']
		messag = data['message']
		csv_writer = csv.writer(database, delimiter=',')
		csv_writer.writerow([name, email, subject, messag])


def send_mail_alert(data):
	html_doc = Template(Path('email.html').read_text())
	email = EmailMessage()
	email['from'] = data['name']
	email['to'] = 'lordelami@gmail.com'
	email['subject'] = data['subject']
	email.set_content(html_doc.substitute({'name': data['name'], 'email': data['email'], 'message': data['message']}), 'html')

	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.ehlo()
		# smtp.starttls()
		smtp.login('machinamailus@gmail.com', 'xdnoewixezingdon')
		smtp.send_message(email)
		print('Beep boop sent!')

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
	if request.method == 'POST':
		try:
			data = request.form.to_dict()
			write_to_csv(data)
			send_mail_alert(data)
			return "Your message has been sent. I will reply you soon" #redirect('/thankyou.html')
		except:
			return 'the data was not saved for some reason try again'
	else:
		return 'Somethings wrong'
