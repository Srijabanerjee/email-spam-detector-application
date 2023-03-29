import streamlit as st
import pickle
import smtplib, ssl
# import pygeoip
# import socket
import re
from PIL import Image

# gi = pygeoip.GeoIP('GeoIP.dat')
model = pickle.load(open('spam.pkl','rb'))
cv=pickle.load(open('vectorizer.pkl','rb'))

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


# Define a function for
# for validating an Email
def check(email):
    f=True
    if (re.fullmatch(regex, email)):
        f=True
    else:
        f=False
    return f

def main():
    st.title("Email Spam Detector Application")
    st.subheader("Build With Streamlit & Python")
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = st.text_input("Senders' Email", "Enter a valid email id")
    image = Image.open('stimage1.png')
    st.image(image, caption='How to activate App Password')
    password = st.text_input("Senders' Password", "Enter the App Password of senders' email")
    receiver_email = st.text_input("Receivers' Email", "Enter a valid email id")
    msg = st.text_input('Message','Enter Text')
    message = f"""\
    Hello   
    {msg}."""

    if st.button("Send"):
        data=[msg]
        vect=cv.transform(data).toarray()
        prediction=model.predict(vect)
        result=prediction[0]
        if result==1:
            st.error("This is a spam mail.")
            st.error("Doesn't send spam email.")
            #speak("This is a spam email")
        elif msg.isspace():
            st.error("The mail contains only splaces enter a proper mail/message.")
        elif msg=="":
            st.error("You can't leave the 'Message' box blank please enter a proper mail/message.")

        else:
            st.success("This is a ham mail")
            #speak("This is not a spam email")
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                if (check(receiver_email)==True):
                    try:
                        server.ehlo()
                        server.starttls(context=context)
                        server.ehlo()
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message)
                        st.success("Email has been sent successfully.")
                    except smtplib.SMTPAuthenticationError:
                        st.error("Senders' email id or password is not valid please put a valid email id and the respective App Password of senders' email.")
                else:
                    st.error("Enter a valid receivers' email id.")
            # except socket.gaierror:
            #     st.error("Connection Interrupted! Please check your internet connectivity.")
main()

# Import modules
# import smtplib, ssl
# port = 587  # For starttls
# smtp_server = "smtp.gmail.com"
# sender_email = "banerjeeofficial21@gmail.com"
# receiver_email = input("Type the mail id of the receiver: ")
# name = input("Put the receiver's name : ")
# m = input("Enter the message: ")
# password = 'hcidbztwrbsohjti'
# message = f"""\
# Subject: Hi {name}
# {m}."""
# context = ssl.create_default_context()
# with smtplib.SMTP(smtp_server, port) as server:
#     server.ehlo()
#     server.starttls(context=context)
#     server.ehlo()
#     server.login(sender_email, password)
#     server.sendmail(sender_email, receiver_email, message)