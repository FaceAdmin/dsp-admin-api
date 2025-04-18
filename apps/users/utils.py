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

    html_content = f"""
        <p>Hello <strong>{user.first_name}</strong>,</p>
        <p>Please scan this QR code with your authenticator app to set up your entry code.</p>
        <p><img src="cid:qr-code-img" alt="OTP QR Code" width="200"/></p>
        <p>If you cannot scan the code, use the following setup key: <code>{user.otp_secret}</code></p>
        <br>
        <p>Best Regards,<br/>FaceAdmin Team</p>
    """

    mail_data = {
        "personalizations": [
            {
                "to": [{"email": user.email}],
                "subject": "Your FaceAdmin OTP Setup"
            }
        ],
        "from": {
            "email": "noreply@faceadmin.org",
            "name": "FaceAdmin"
        },
        "content": [
            {
                "type": "text/html",
                "value": html_content
            }
        ],
        "attachments": [
            {
                "content": base64_qr,
                "type": "image/png",
                "filename": "qrcode.png",
                "disposition": "inline",
                "content_id": "qr-code-img"
            }
        ]
    }

    try:
        sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        response = sg.client.mail.send.post(request_body=mail_data)
        print(f"[SENDGRID] Email sent: {response.status_code}")
    except Exception as e:
        print(f"[SENDGRID ERROR] {e}")
