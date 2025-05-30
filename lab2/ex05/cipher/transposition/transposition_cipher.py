class TranspositionCipher:
    def __init__(self):
        pass
    
    def encrypt(self, text, key):
        """Mã hóa bằng cách đọc theo cột"""
        encrypted_text = ''
        for col in range(key):
            pointer = col
            while pointer < len(text):
                encrypted_text += text[pointer]
                pointer += key
        return encrypted_text
    
    def decrypt(self, text, key):
        """Giải mã bằng cách khôi phục lại grid gốc"""
        # Tính toán kích thước grid
        num_rows = len(text) // key
        num_extra_chars = len(text) % key
        
        # Tạo mảng để lưu độ dài mỗi cột
        col_lengths = []
        for col in range(key):
            if col < num_extra_chars:
                col_lengths.append(num_rows + 1)
            else:
                col_lengths.append(num_rows)
        
        # Phân phối ký tự vào từng cột
        decrypted_cols = [''] * key
        char_index = 0
        
        for col in range(key):
            for _ in range(col_lengths[col]):
                if char_index < len(text):
                    decrypted_cols[col] += text[char_index]
                    char_index += 1
        
        # Khôi phục text gốc bằng cách đọc theo hàng
        decrypted_text = ''
        max_rows = max(col_lengths) if col_lengths else 0
        
        for row in range(max_rows):
            for col in range(key):
                if row < len(decrypted_cols[col]):
                    decrypted_text += decrypted_cols[col][row]
        
        return decrypted_text


# Test function để verify
def test_transposition_cipher():
    cipher = TranspositionCipher()
    
    # Test cases
    test_cases = [
        ("HELLO", 3),
        ("RASPBERRYPT", 5),
        ("HELLOWORLD", 4),
        ("ABCDEFGHIJ", 3),
        ("TESTMESSAGE", 6)
    ]
    
    print("Testing Transposition Cipher:")
    print("=" * 50)
    
    for original, key in test_cases:
        encrypted = cipher.encrypt(original, key)
        decrypted = cipher.decrypt(encrypted, key)
        
        print(f"Original:  {original}")
        print(f"Key:       {key}")
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
        print(f"Match:     {original == decrypted} {'✅' if original == decrypted else '❌'}")
        print("-" * 30)

# Uncomment để test
# test_transposition_cipher()