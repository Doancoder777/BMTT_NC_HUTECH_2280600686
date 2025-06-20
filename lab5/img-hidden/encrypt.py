import sys
from PIL import Image

def encode_image(image_path, message):
    try:
        img = Image.open(image_path)
        # Đảm bảo hình ảnh ở chế độ RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        width, height = img.size
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        binary_message += '1111111111111110'  # Dấu kết thúc thông điệp

        if len(binary_message) > width * height * 3:
            raise ValueError("Thông điệp quá dài để nhúng vào hình ảnh này!")

        data_index = 0
        img_data = img.load()  # Sử dụng load() để truy cập pixel nhanh hơn

        for row in range(height):
            for col in range(width):
                if data_index >= len(binary_message):
                    break
                pixel = list(img_data[col, row])

                for color_channel in range(3):
                    if data_index < len(binary_message):
                        pixel[color_channel] = int(format(pixel[color_channel], '08b')[:-1] + binary_message[data_index], 2)
                        data_index += 1
                    img_data[col, row] = tuple(pixel)

        encoded_image_path = 'encoded_image.png'
        img.save(encoded_image_path, 'PNG')
        print("Mã hóa hoàn tất. Hình ảnh đã mã hóa được lưu tại", encoded_image_path)

    except Exception as e:
        print(f"Lỗi khi mã hóa: {e}")

def main():
    if len(sys.argv) != 3:
        print("Cách sử dụng: python encrypt.py <đường_dẫn_hình_ảnh> <thông_điệp>")
        return

    image_path = sys.argv[1]
    message = sys.argv[2]
    encode_image(image_path, message)

if __name__ == '__main__':
    main()