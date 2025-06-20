import sys
from PIL import Image

def decode_image(encoded_image_path):
    try:
        img = Image.open(encoded_image_path)
        # Đảm bảo hình ảnh ở chế độ RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        width, height = img.size
        binary_message = ""

        img_data = img.load()  # Sử dụng load() để truy cập pixel nhanh hơn

        for row in range(height):
            for col in range(width):
                pixel = img_data[col, row]
                for color_channel in range(3):
                    binary_message += format(pixel[color_channel], '08b')[-1]

        # Tìm dấu kết thúc '1111111111111110'
        end_marker = '1111111111111110'
        message = ""
        for i in range(0, len(binary_message) - 16, 8):
            byte = binary_message[i:i+8]
            # Kiểm tra xem 16 bit tiếp theo có phải là dấu kết thúc không
            if binary_message[i:i+16] == end_marker:
                break
            char = chr(int(byte, 2))
            message += char

        return message

    except Exception as e:
        print(f"Lỗi khi giải mã: {e}")
        return ""

def main():
    if len(sys.argv) != 2:
        print("Cách sử dụng: python decrypt.py <đường_dẫn_hình_ảnh_đã_mã_hóa>")
        return

    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    if decoded_message:
        print("Thông điệp giải mã:", decoded_message)
    else:
        print("Không thể giải mã thông điệp.")

if __name__ == '__main__':
    main()