from main import *

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def sendtoken(email):
    
    user = users.query.filter_by(email=email).first()
    print(user)
    #check if user account has been confiremed and redirect to page
    if user!=None:
       if user.is_confirmed()==0:
            token = serializer.dumps({'user_id': user.id})
            link = url_for("confirmToken",token=token, _external=True)
            print(link)            
            # create the email message with the confirmation link
            msg = Message(subject='Confirm Your Email',
                      recipients=[f"{email}"],
                      body= f"Please click on the link below to confirm your email\n<a href={link}>{link}</a>", sender="donotreply.dut.ac.za"
                     )
            thr = Thread(target=send_async_email, args=[app, msg])
            thr.start()
            #user.confirmed = True
            #db.session.commit()
            print("Email sent") 
       else: 
           print("Email sending failed")
       


