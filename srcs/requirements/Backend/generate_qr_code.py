import qrcode

def generate_qr_code_from_id(user_id, file_path):
    data_to_encode = f"ID: {user_id}"  # Using the ID in the QR code data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_to_encode)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)

# Example usage
user_id = "123456"  # Replace this with your actual user ID
output_file_path = "q_code1.png"

generate_qr_code_from_id(user_id, output_file_path)
