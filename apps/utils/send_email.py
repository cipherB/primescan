# import threading
# from django.core.mail import EmailMessage
# from django.core.mail import EmailMultiAlternatives, send_mail
# from rest_framework import status
# from django.template.loader import render_to_string
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText


# class EmailThread(threading.Thread):
#     def __init__(self, email, subject, message, from_email, **kwargs):
#         self.subject = subject
#         self.message = message
#         self.recipient = email
#         self.sender = from_email
#         threading.Thread.__init__(self)

#     def run(self):
#         try:
#             context, status = send_mail_(
#                 self.recipient, self.subject, self.message, self.sender
#             )
#             print(context)
#             # html_content = render_to_string(self.message, self.context)
#             # text_content = 'This is an important message.'
#             # msg = EmailMultiAlternatives(self.subject, text_content, self.sender, [self.recipient])
#             # msg.attach_alternative(html_content, "text/html")
#             # msg.send(fail_silently=False)
#             print("Sending email to", self.recipient, "with subject", self.subject)
#         except Exception as e:
#             print("Error sending email:", e)


# class EmailManager:
#     @staticmethod
#     def send_email(email, subject, message, from_email, **kwargs):
#         email_thread = EmailThread(email, subject, message, from_email, **kwargs)
#         email_thread.start()


# def email_user(email, subject, message, context, from_email, **kwargs):
#     """
#     Sends an email to this User.

#     """
#     try:
#         context = dict(context)
#         print(context)
#         html_content = render_to_string(message, context)
#         # sent = mail.send_mail(subject, message, from_email, [email], **kwargs)
#         text_content = "This is an important message."
#         msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send(fail_silently=False)
#         status_ = status.HTTP_200_OK
#         context = {"status": 200, "message": "email sent successfully"}
#         return context, status_

#     except Exception as e:
#         error = str(e)
#         status_ = status.HTTP_501_NOT_IMPLEMENTED
#         context = {"status": 501, "message": error}
#         return context, status_


# def send_mail_(email, subject, message, from_email):
#     try:
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=from_email,
#             recipient_list=[email],
#         )
#         status_ = status.HTTP_200_OK
#         context = {"status": 200, "message": "email sent successfully"}
#         return context, status_
#     except Exception as e:
#         error = str(e)
#         status_ = status.HTTP_501_NOT_IMPLEMENTED
#         context = {"status": 501, "message": error}
#         return context, status_
