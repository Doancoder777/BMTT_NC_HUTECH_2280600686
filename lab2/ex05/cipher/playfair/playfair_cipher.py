class PlayFairCipher:
    def __init__(self) -> None:
        pass

    def create_playfair_matrix(self, key):
        """Tạo ma trận 5x5 từ key"""
        if not key:
            key = "A"
        
        key = str(key).upper().replace("J", "I")
        key = ''.join(char for char in key if char.isalpha())
        
        if not key:
            key = "A"
        
        # Loại bỏ trùng lặp
        unique_chars = []
        seen = set()
        for char in key:
            if char not in seen:
                unique_chars.append(char)
                seen.add(char)
        
        # Thêm alphabet còn lại
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for char in alphabet:
            if char not in seen:
                unique_chars.append(char)
        
        # Tạo ma trận 5x5
        matrix_chars = unique_chars[:25]
        matrix = []
        for i in range(0, 25, 5):
            row = matrix_chars[i:i+5]
            matrix.append(row)
        
        return matrix

    def find_position(self, matrix, char):
        """Tìm vị trí ký tự trong ma trận"""
        char = char.upper().replace("J", "I")
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == char:
                    return (row, col)
        return None

    def prepare_plaintext(self, text):
        """Chuẩn bị plaintext cho PlayFair"""
        if not text:
            return ""
        
        text = str(text).upper().replace("J", "I")
        text = ''.join(char for char in text if char.isalpha())
        
        if not text:
            return ""
        
        # Thêm X giữa ký tự giống nhau
        result = []
        i = 0
        while i < len(text):
            result.append(text[i])
            if i + 1 < len(text) and text[i] == text[i + 1]:
                result.append("X")
            i += 1
        
        # Thêm X cuối nếu lẻ
        if len(result) % 2 == 1:
            result.append("X")
        
        return ''.join(result)

    def playfair_encrypt(self, plaintext, matrix):
        """Mã hóa bằng PlayFair"""
        prepared = self.prepare_plaintext(plaintext)
        if not prepared:
            return ""
        
        encrypted = []
        
        for i in range(0, len(prepared), 2):
            char1 = prepared[i]
            char2 = prepared[i + 1] if i + 1 < len(prepared) else "X"
            
            pos1 = self.find_position(matrix, char1)
            pos2 = self.find_position(matrix, char2)
            
            if pos1 is None or pos2 is None:
                continue
            
            row1, col1 = pos1
            row2, col2 = pos2
            
            if row1 == row2:
                # Cùng hàng
                new_col1 = (col1 + 1) % 5
                new_col2 = (col2 + 1) % 5
                encrypted.append(matrix[row1][new_col1])
                encrypted.append(matrix[row2][new_col2])
            elif col1 == col2:
                # Cùng cột
                new_row1 = (row1 + 1) % 5
                new_row2 = (row2 + 1) % 5
                encrypted.append(matrix[new_row1][col1])
                encrypted.append(matrix[new_row2][col2])
            else:
                # Hình chữ nhật
                encrypted.append(matrix[row1][col2])
                encrypted.append(matrix[row2][col1])
        
        return ''.join(encrypted)

    def playfair_decrypt(self, ciphertext, matrix):
        """Giải mã PlayFair"""
        if not ciphertext:
            return ""
        
        ciphertext = str(ciphertext).upper().replace("J", "I")
        ciphertext = ''.join(char for char in ciphertext if char.isalpha())
        
        if len(ciphertext) % 2 == 1:
            ciphertext += "X"
        
        decrypted = []
        
        for i in range(0, len(ciphertext), 2):
            if i + 1 >= len(ciphertext):
                break
            
            char1 = ciphertext[i]
            char2 = ciphertext[i + 1]
            
            pos1 = self.find_position(matrix, char1)
            pos2 = self.find_position(matrix, char2)
            
            if pos1 is None or pos2 is None:
                continue
            
            row1, col1 = pos1
            row2, col2 = pos2
            
            if row1 == row2:
                # Cùng hàng
                new_col1 = (col1 - 1) % 5
                new_col2 = (col2 - 1) % 5
                decrypted.append(matrix[row1][new_col1])
                decrypted.append(matrix[row2][new_col2])
            elif col1 == col2:
                # Cùng cột
                new_row1 = (row1 - 1) % 5
                new_row2 = (row2 - 1) % 5
                decrypted.append(matrix[new_row1][col1])
                decrypted.append(matrix[new_row2][col2])
            else:
                # Hình chữ nhật
                decrypted.append(matrix[row1][col2])
                decrypted.append(matrix[row2][col1])
        
        result = ''.join(decrypted)
        return self.remove_padding(result)

    def remove_padding(self, text):
        """Loại bỏ X thừa"""
        if not text:
            return text
        
        result = []
        i = 0
        
        while i < len(text):
            char = text[i]
            
            # X ở cuối
            if char == 'X' and i == len(text) - 1:
                pass  # Bỏ qua
            # X giữa hai ký tự giống nhau
            elif (char == 'X' and 
                  i > 0 and i < len(text) - 1 and 
                  text[i-1] == text[i+1]):
                pass  # Bỏ qua
            else:
                result.append(char)
            
            i += 1
        
        return ''.join(result)