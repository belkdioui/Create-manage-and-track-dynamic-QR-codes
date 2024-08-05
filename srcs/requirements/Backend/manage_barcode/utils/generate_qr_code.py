import qrcode
from PIL import Image
import os
from django.conf import settings

def generate_qr_code_from_id(ticket):
    data_to_encode = ticket.barcode
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=16,
        border=2,
    )
    qr.add_data(data_to_encode)
    qr.make(fit=True)
    file_path = os.path.join(settings.BASE_DIR, f'manage_barcode/static/barcodes/{ticket.client.email}.png')
    img = qr.make_image(fill_color="#181822", back_color="transparent")
    img = img.convert("RGBA")
    img.save(file_path)
