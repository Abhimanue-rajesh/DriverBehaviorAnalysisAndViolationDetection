# Send email to using Gmail SMTP server
import smtplib
from email.mime.text import MIMEText

def send_email(email):
   from_email = "driverviolation@gmail.com"
   from_password = "kege mleo pruw znbl"
   to_email = email


   subject = "Test Message from violation email"
   message = "Hello This is a test message"


   msg = MIMEText(message, 'html')
   msg['Subject'] = subject
   msg['To'] = to_email
   msg['From'] = from_email

   # Create SMTP session for sending the mail
   gmail = smtplib.SMTP('smtp.gmail.com', 587)
   gmail.ehlo()
   gmail.starttls()
   # Login to gmail account
   gmail.login(from_email, from_password)
   # Send mail
   gmail.send_message(msg)


if __name__ == '__main__':
   send_email("abhimanuemvk@gmail.com")