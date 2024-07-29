import qrcode
from PIL import Image
import os
from django.conf import settings

def generate_qr_code_from_id(ticket_id, db_user):
    data_to_encode = f"busbladi: {ticket_id}{db_user.fname}"
    print(data_to_encode)
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=16,
        border=2,
    )
    qr.add_data(data_to_encode)
    qr.make(fit=True)
    file_path = os.path.join(settings.BASE_DIR, f'manage_barcode/static/barcodes/{db_user.email}.png')
    img = qr.make_image(fill_color="#EF552D", back_color="transparent")
    img = img.convert("RGBA")
    img.save(file_path)
