import base64
import io
import qrcode
import pyotp
from django.conf import settings
from sendgrid import SendGridAPIClient

def generate_qr_base64(user):
    totp = pyotp.TOTP(user.otp_secret)
    uri = totp.provisioning_uri(name=user.email, issuer_name="FaceAdmin")
    qr = qrcode.make(uri)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return base64_img

def send_otp_email(user):
    base64_qr = generate_qr_base64(user)
    img_tag = f'<img src="data:image/png;base64,{base64_qr}" alt="OTP QR Code" width="200"/>'

    #TODO Change the email content and also fix the QR Code generation
    html_content = f"""
        <p>Hello <strong>{user.fname}</strong>,</p>
        <p>Please scan this QR code with your Google Authenticator app to set up two-factor authentication.</p>
        {img_tag}
        <p>If you cannot scan the code, use the following secret: <code>{user.otp_secret}</code></p>
        <p><strong>Issuer:</strong> FaceAdmin</p>
        <br>
        <p>Thanks,<br/>FaceAdmin Team</p>
    """

    mail_data = {
        "personalizations": [
            {
                "to": [
                    {"email": user.email}
                ],
                "subject": "Your FaceAdmin OTP Setup"
            }
        ],
        "from": {"email": "noreply@faceadmin.org"},
        "content": [
            {
                "type": "text/html",
                "value": html_content
            }
        ]
    }

    try:
        sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        response = sg.client.mail.send.post(request_body=mail_data)
        print(f"[SENDGRID] Email sent: {response.status_code}")
    except Exception as e:
        print(f"[SENDGRID ERROR] {e}")
