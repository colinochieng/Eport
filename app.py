from flask_mail import Mail, Message
from marshmallow import fields, Schema, ValidationError, validates_schema
from flask_cors import CORS
from flask import Flask, request, jsonify
import os

app = Flask(__name__)


app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")
RECIPIENT = os.getenv("MAIL_USERNAME")

# mail object
mail = Mail(app=app)

# CORS settings
cors = CORS(app=app)
app.extensions["mail"].debug = 0

class ContactForm(Schema):
    """
    class defining data provided in a contact form
    """

    name = fields.Str(required=True)
    email = fields.Email(required=True)
    message = fields.Str(required=True)


class HireMeForm(Schema):
    """
    Class defining the structure of the hire me form
    """

    name = fields.Str(required=True)
    email = fields.Email(required=False, allow_none=True)
    phoneNumber = fields.Str(required=False, allow_none=True)
    communicationMethod = fields.Str(required=True)
    projectTitle = fields.Str(required=True)
    projectDeadline = fields.Str(required=False)
    projectDescription = fields.Str(required=True)

    @validates_schema
    def validate_contacts(self, data, **kwargs):
        if not data.get('email') and not data.get('phoneNumber'):
            raise ValidationError("Either email or phone must be provided.")
        if data.get('email') and data.get('phone'):
            raise ValidationError("Only one of email or phone should be provided.")



@app.post("/contact", strict_slashes=False)
def contact():
    """
    View function handling contact form
    """
    contact_schema = ContactForm()

    try:
        contact_msg = contact_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    msg = Message(subject="Contact", recipients=[RECIPIENT])
    formatted_body = f"Username: {contact_msg['name']}\n"\
                     f"Email Address: {contact_msg['email']}\n\n"\
                     f"{contact_msg['message']}"

    msg.body = formatted_body

    try:
        mail.send(msg)
        return jsonify({'message': 'Email sent successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.post("/hire_me", strict_slashes=False)
def hire_me():
    """
    View functiom for handling hiring form
    """
    hire_me_schema = HireMeForm()

    try:
        hire_me_msg = hire_me_schema.load(request.json)
    except ValidationError as e:
        print(e.messages)
        print(request.json)
        return jsonify(e.messages), 400

    
    formatted_body = f"Username: {hire_me_msg['name']}\n"
    formatted_body += f"Email Address: {hire_me_msg['email']}\n\n" if hire_me_msg.get("email") else f"Phone No.: {hire_me_msg['phoneNumber']}\n\n"
    formatted_body += f"Communication Method: {hire_me_msg['communicationMethod']}\n"\
                      f"Project Title: {hire_me_msg['projectTitle']}\n"
    
    formatted_body += f"Project Deadline: {hire_me_msg['projectDeadline']}" if "projectDeadline" in hire_me_msg else ""
    formatted_body += f"Project Description: {hire_me_msg['projectDescription']}"

    msg = Message(subject="Hire Me", recipients=[RECIPIENT], body=formatted_body)

    try:
        mail.send(msg)
        return jsonify({'message': 'Email sent successfully!'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
