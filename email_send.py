import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
sender_email = 'crazyvastra@gmail.com'
sender_password = 'vwehrwxqblxckman'
receiver_email = 'crazyvastra@gmail.com'


def send_user_code_in_mail(code):
    subject = 'User Code to login to Microsoft Account'
    message = 'Your User code to login to your Microsoft account : '+code

    # Create the MIME object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Establish a secure session with Gmail's outgoing SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Log in with your Gmail account
        server.login(sender_email, sender_password)

        # Send email
        server.sendmail(sender_email, receiver_email, msg.as_string())

        print('Email sent successfully!')
    except Exception as e:
        print('Error:', e)
    finally:
        server.quit()
