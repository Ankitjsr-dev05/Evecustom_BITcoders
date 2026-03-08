from django.conf import settings
from django.core.mail import send_mail,EmailMultiAlternatives

# mail send 
def send_mail_maltialt(email, otp="555555"):
    try:
        subject = "Verify Your Email Address"

        message = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            body {{
              font-family: Arial, sans-serif;
              background-color: #f4f6f9;
              margin: 0;
              padding: 0;
            }}
            .container {{
              max-width: 500px;
              margin: 40px auto;
              background: #ffffff;
              padding: 30px;
              border-radius: 10px;
              box-shadow: 0 4px 12px rgba(0,0,0,0.1);
              text-align: center;
            }}
            .otp {{
              font-size: 28px;
              font-weight: bold;
              letter-spacing: 4px;
              color: #ffffff;
              background: #4f46e5;
              padding: 12px 20px;
              border-radius: 8px;
              display: inline-block;
              margin: 20px 0;
            }}
            .footer {{
              font-size: 12px;
              color: #777;
              margin-top: 20px;
            }}
          </style>
        </head>
        <body>
          <div class="container">
            <h2>Email Verification</h2>
            <p>Hello,</p>
            <p>Thank you for registering with us.</p>
            <p>Your One-Time Password (OTP) is:</p>

            <div class="otp">{otp}</div>

            <p>This OTP is valid for 5 minutes.</p>
            <p>If you did not request this, please ignore this email.</p>

            <div class="footer">
              &copy; 2026 BITCoders. All rights reserved.
            </div>
          </div>
        </body>
        </html>
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        email_message = EmailMultiAlternatives(subject, message, from_email, recipient_list)
        email_message.content_subtype = "html"  # Set the content type to HTML
        email_message.send()
        print("Email sent successfully", email, otp)
        
    except Exception as e:
        print("Failed to send email:", str(e))

def send_create_team_mail(email, team_name, team_code, event_name):
    try:
        subject = "Team Created Successfully"

        message = f"""
                  Hello Team Leader,

                  Your team has been created successfully.

                  Event Name : {event_name}
                  Team Name  : {team_name}
                  Team Code  : {team_code}

                  Share this team code with your teammates so they can join your team.

                  Good luck for the event 🚀

                  Regards,
                  Event Management Team
                  """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        email_message = EmailMultiAlternatives(subject, message, from_email, recipient_list)
        email_message.content_subtype = "html"  # Set the content type to HTML
        email_message.send()
        print("Email sent successfully", email)   
    except Exception as e:
        print("Failed to send email:", str(e))
    print("Join team email sent successfully")

def send_join_team_mail(email, team_name, team_code, event_name):
    try:
        subject = "Joined Team Successfully"

        message = f"""
                  Hello Participant,

                  You have successfully joined the team.

                  Event Name : {event_name}
                  Team Name  : {team_name}
                  Team Code  : {team_code}

                  Good luck for the event 🚀

                  Regards,
                  Event Management Team
                  """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        email_message = EmailMultiAlternatives(subject, message, from_email, recipient_list)
        email_message.content_subtype = "html"  # Set the content type to HTML
        email_message.send()
        print("Email sent successfully", email)   
    except Exception as e:
        print("Failed to send email:", str(e))
    print("Join team email sent successfully")
    
def sending_otp_mail(email, otp):
    try:
        subject = "Email Verification"
        message = f"Welcome to our service! Your OTP for email verification is: {otp}. Please use this OTP to complete your registration process. If you did not request this, please ignore this email."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        print("Email sent successfully")
        
    except Exception as e:
        print("Failed to send email:", str(e))
