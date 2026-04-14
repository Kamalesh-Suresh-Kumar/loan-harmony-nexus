import smtplib
import sys
from email.mime.text import MIMEText

receiver_email = sys.argv[1]
otp = sys.argv[2]

sender_email = "230701138@rajalakshmi.edu.in"
app_password = "ofbo yvsu ajps ajmq"

msg = MIMEText(f"Your OTP is: {otp}\nDon't share it with anyone.")
msg['Subject'] = "Your OTP Code"
msg['From'] = sender_email
msg['To'] = receiver_email

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, app_password)
    server.send_message(msg)
    server.quit()
    print("SUCCESS")
except Exception as e:
    print("FAIL")
    print(str(e))
