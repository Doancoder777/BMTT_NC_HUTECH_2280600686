from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import sys

# Add cipher modules to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'cipher'))

# Cipher configurations
CIPHER_CONFIGS = {
    'caesar': {
        'cipher_name': 'Caesar Cipher',
        'cipher_icon': '🔐',
        'cipher_description': 'Thuật toán mã hóa cổ điển bằng dịch chuyển ký tự',
        'key_input_type': 'number',
        'key_placeholder': 'Nhập key số (1-25)...',
        'key_attributes': 'min="1" max="25"',
        'encrypt_url': '/caesar/encrypt',
        'decrypt_url': '/caesar/decrypt',
        'cipher_info': 'là một trong những thuật toán mã hóa cổ điển nhất, được Julius Caesar sử dụng để bảo mật thông tin quân sự.',
        'cipher_how_it_works': 'Mỗi ký tự trong văn bản được dịch chuyển một số vị trí cố định trong bảng chữ cái.',
        'cipher_example': 'Với key = 3, chữ "A" sẽ thành "D", chữ "B" thành "E", v.v.'
    },
    'vigener': {
        'cipher_name': 'Vigenère Cipher',
        'cipher_icon': '🔑',
        'cipher_description': 'Thuật toán mã hóa đa ký tự sử dụng từ khóa',
        'key_input_type': 'text',
        'key_placeholder': 'Nhập từ khóa...',
        'key_attributes': 'pattern="[A-Za-z]+" title="Chỉ nhập chữ cái"',
        'encrypt_url': '/vigener/encrypt',
        'decrypt_url': '/vigener/decrypt',
        'cipher_info': 'sử dụng một từ khóa để tạo ra chuỗi key lặp lại. Mỗi ký tự được mã hóa bằng Caesar cipher với key khác nhau.',
        'cipher_how_it_works': 'Từ khóa được lặp lại để có độ dài bằng văn bản gốc, sau đó mỗi ký tự được shift theo ký tự tương ứng trong key.',
        'cipher_example': 'Với key = "KEY" và text = "HELLO", H+K=R, E+E=I, L+Y=J, L+K=V, O+E=S → "RIJVS".'
    },
    'railfence': {
        'cipher_name': 'Rail Fence Cipher',
        'cipher_icon': '🚂',
        'cipher_description': 'Thuật toán mã hóa hoán vị theo hình zigzag',
        'key_input_type': 'number',
        'key_placeholder': 'Nhập số rail (2-10)...',
        'key_attributes': 'min="2" max="10"',
        'encrypt_url': '/railfence/encrypt',
        'decrypt_url': '/railfence/decrypt',
        'cipher_info': 'viết văn bản theo hình zigzag trên một số hàng (rails) nhất định, sau đó đọc từng hàng để tạo ra cipher text.',
        'cipher_how_it_works': 'Văn bản được viết theo hình zigzag xuống và lên các rail, sau đó đọc từ trái qua phải theo từng rail.',
        'cipher_example': 'Với 3 rails và text "HELLO WORLD", sẽ tạo thành pattern zigzag và đọc theo hàng.'
    },
    'transposition': {
        'cipher_name': 'Transposition Cipher',
        'cipher_icon': '🔄',
        'cipher_description': 'Thuật toán mã hóa bằng hoán vị vị trí ký tự',
        'key_input_type': 'number',
        'key_placeholder': 'Nhập số cột (2-10)...',
        'key_attributes': 'min="2" max="10"',
        'encrypt_url': '/transposition/encrypt',
        'decrypt_url': '/transposition/decrypt',
        'cipher_info': 'sắp xếp văn bản thành lưới theo số cột được xác định bởi key, sau đó đọc theo cột để tạo cipher text.',
        'cipher_how_it_works': 'Văn bản được viết theo hàng trong một lưới có số cột = key, sau đó đọc theo cột từ trái qua phải.',
        'cipher_example': 'Với key = 3 và text "HELLO", viết thành H-E-L / L-O-X, đọc theo cột: HLE-EO-LX.'
    },
    'playfair': {
        'cipher_name': 'PlayFair Cipher',
        'cipher_icon': '📋',
        'cipher_description': 'Thuật toán mã hóa sử dụng ma trận 5x5',
        'key_input_type': 'text',
        'key_placeholder': 'Nhập từ khóa...',
        'key_attributes': 'pattern="[A-Za-z]+" title="Chỉ nhập chữ cái"',
        'encrypt_url': '/playfair/encrypt',
        'decrypt_url': '/playfair/decrypt',
        'cipher_info': 'sử dụng ma trận 5x5 chứa 25 ký tự (I và J được coi là một). Văn bản được chia thành cặp và mã hóa theo các quy tắc của ma trận.',
        'cipher_how_it_works': 'Tạo ma trận 5x5 từ key, chia text thành cặp, áp dụng quy tắc: cùng hàng/cột thì shift, khác thì swap góc hình chữ nhật.',
        'cipher_example': 'Với key "KEYWORD", tạo ma trận 5x5 và mã hóa từng cặp ký tự theo quy tắc PlayFair.'
    }
}

app = Flask(__name__)

def format_matrix_display(matrix, title="Ma trận PlayFair:"):
    """Helper function to format PlayFair matrix for display"""
    if not matrix:
        return ""
    
    html = f'<div class="matrix-display mt-2"><div class="matrix-title">{title}</div>'
    for row in matrix:
        html += f'<div class="matrix-row">{" ".join(row)}</div>'
    html += '</div>'
    return html

def render_cipher_page(cipher_type, encrypt_result=None, decrypt_result=None, matrix=None):
    """Universal function to render cipher pages"""
    config = CIPHER_CONFIGS[cipher_type]
    
    # Handle PlayFair matrix display
    matrix_display_encrypt = ""
    matrix_display_decrypt = ""
    
    if matrix and cipher_type == 'playfair':
        if encrypt_result:
            matrix_display_encrypt = format_matrix_display(matrix)
        if decrypt_result:
            matrix_display_decrypt = format_matrix_display(matrix)
    
    return render_template('cipher_base.html',
                         encrypt_result=encrypt_result,
                         decrypt_result=decrypt_result,
                         matrix_display_encrypt=matrix_display_encrypt,
                         matrix_display_decrypt=matrix_display_decrypt,
                         **config)

# Try to import cipher classes
try:
    # Multiple import attempts
    cipher_paths = [
        os.path.join(current_dir, 'cipher', 'caesar'),
        os.path.join(current_dir, 'cipher', 'vigener'),
        os.path.join(current_dir, 'cipher', 'railfence'),
        os.path.join(current_dir, 'cipher', 'transposition'),
        os.path.join(current_dir, 'cipher', 'playfair')
    ]
    
    for path in cipher_paths:
        if path not in sys.path:
            sys.path.append(path)
    
    from caesar import CaesarCipher
    from vigener import VigenereCipher
    from railfence import RailFenceCipher
    from transposition import TranspositionCipher
    from playfair import PlayFairCipher
    
    print("✅ Successfully imported all cipher classes")
    
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    print("💡 Using fallback implementations")
    
    # Fallback implementations
    class CaesarCipher:
        def encrypt_text(self, text, key):
            result = ""
            for char in text:
                if char.isalpha():
                    ascii_offset = 65 if char.isupper() else 97
                    result += chr((ord(char) - ascii_offset + key) % 26 + ascii_offset)
                else:
                    result += char
            return result
        
        def decrypt_text(self, text, key):
            return self.encrypt_text(text, -key)
    
    class VigenereCipher:
        def vigenere_encrypt(self, text, key):
            text = text.upper()
            key = key.upper()
            result = ""
            key_index = 0
            
            for char in text:
                if char.isalpha():
                    shift = ord(key[key_index % len(key)]) - ord('A')
                    result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                    key_index += 1
                else:
                    result += char
            return result
        
        def vigenere_decrypt(self, text, key):
            text = text.upper()
            key = key.upper()
            result = ""
            key_index = 0
            
            for char in text:
                if char.isalpha():
                    shift = ord(key[key_index % len(key)]) - ord('A')
                    result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                    key_index += 1
                else:
                    result += char
            return result
    
    class RailFenceCipher:
        def rail_fence_encrypt(self, plain_text, num_rails):
            if num_rails <= 1:
                return plain_text
                
            rails = [[] for _ in range(num_rails)]
            rail_index = 0
            direction = 1
            
            for char in plain_text:
                rails[rail_index].append(char)
                
                if rail_index == 0:
                    direction = 1
                elif rail_index == num_rails - 1:
                    direction = -1
                    
                rail_index += direction
            
            cipher_text = ''.join([''.join(rail) for rail in rails])
            return cipher_text
        
        def rail_fence_decrypt(self, cipher_text, num_rails):
            if num_rails <= 1:
                return cipher_text
                
            # Calculate rail lengths
            rail_lengths = [0] * num_rails
            rail_index = 0
            direction = 1
            
            for i in range(len(cipher_text)):
                rail_lengths[rail_index] += 1
                
                if rail_index == 0:
                    direction = 1
                elif rail_index == num_rails - 1:
                    direction = -1
                    
                rail_index += direction
            
            # Split cipher text into rails
            rails = []
            start = 0
            for length in rail_lengths:
                rails.append(list(cipher_text[start:start + length]))
                start += length
            
            # Reconstruct plain text
            plain_text = ""
            rail_index = 0
            direction = 1
            
            for i in range(len(cipher_text)):
                plain_text += rails[rail_index].pop(0)
                
                if rail_index == 0:
                    direction = 1
                elif rail_index == num_rails - 1:
                    direction = -1
                    
                rail_index += direction
            
            return plain_text
    
    class TranspositionCipher:
        def encrypt(self, text, key):
            encrypted_text = ''
            for col in range(key):
                pointer = col
                while pointer < len(text):
                    encrypted_text += text[pointer]
                    pointer += key
            return encrypted_text
        
        def decrypt(self, text, key):
            num_rows = len(text) // key
            num_extra_chars = len(text) % key
            
            col_lengths = []
            for col in range(key):
                if col < num_extra_chars:
                    col_lengths.append(num_rows + 1)
                else:
                    col_lengths.append(num_rows)
            
            decrypted_cols = [''] * key
            char_index = 0
            
            for col in range(key):
                for _ in range(col_lengths[col]):
                    if char_index < len(text):
                        decrypted_cols[col] += text[char_index]
                        char_index += 1
            
            decrypted_text = ''
            max_rows = max(col_lengths) if col_lengths else 0
            
            for row in range(max_rows):
                for col in range(key):
                    if row < len(decrypted_cols[col]):
                        decrypted_text += decrypted_cols[col][row]
            
            return decrypted_text
    
    class PlayFairCipher:
        def __init__(self) -> None:
            pass

        def create_playfair_matrix(self, key):
            if not key:
                key = "A"
            
            key = str(key).upper().replace("J", "I")
            key = ''.join(char for char in key if char.isalpha())
            
            if not key:
                key = "A"
            
            # Remove duplicates
            unique_chars = []
            seen = set()
            for char in key:
                if char not in seen:
                    unique_chars.append(char)
                    seen.add(char)
            
            # Add remaining alphabet
            alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
            for char in alphabet:
                if char not in seen:
                    unique_chars.append(char)
            
            # Create 5x5 matrix
            matrix_chars = unique_chars[:25]
            matrix = []
            for i in range(0, 25, 5):
                row = matrix_chars[i:i+5]
                matrix.append(row)
            
            return matrix

        def find_position(self, matrix, char):
            char = char.upper().replace("J", "I")
            for row in range(5):
                for col in range(5):
                    if matrix[row][col] == char:
                        return (row, col)
            return None

        def prepare_plaintext(self, text):
            if not text:
                return ""
            
            text = str(text).upper().replace("J", "I")
            text = ''.join(char for char in text if char.isalpha())
            
            if not text:
                return ""
            
            # Add X between duplicate letters
            result = []
            i = 0
            while i < len(text):
                result.append(text[i])
                if i + 1 < len(text) and text[i] == text[i + 1]:
                    result.append("X")
                i += 1
            
            # Add X at end if odd length
            if len(result) % 2 == 1:
                result.append("X")
            
            return ''.join(result)

        def playfair_encrypt(self, plaintext, matrix):
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
                    # Same row
                    new_col1 = (col1 + 1) % 5
                    new_col2 = (col2 + 1) % 5
                    encrypted.append(matrix[row1][new_col1])
                    encrypted.append(matrix[row2][new_col2])
                elif col1 == col2:
                    # Same column
                    new_row1 = (row1 + 1) % 5
                    new_row2 = (row2 + 1) % 5
                    encrypted.append(matrix[new_row1][col1])
                    encrypted.append(matrix[new_row2][col2])
                else:
                    # Rectangle
                    encrypted.append(matrix[row1][col2])
                    encrypted.append(matrix[row2][col1])
            
            return ''.join(encrypted)

        def playfair_decrypt(self, ciphertext, matrix):
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
                    # Same row
                    new_col1 = (col1 - 1) % 5
                    new_col2 = (col2 - 1) % 5
                    decrypted.append(matrix[row1][new_col1])
                    decrypted.append(matrix[row2][new_col2])
                elif col1 == col2:
                    # Same column
                    new_row1 = (row1 - 1) % 5
                    new_row2 = (row2 - 1) % 5
                    decrypted.append(matrix[new_row1][col1])
                    decrypted.append(matrix[new_row2][col2])
                else:
                    # Rectangle
                    decrypted.append(matrix[row1][col2])
                    decrypted.append(matrix[row2][col1])
            
            result = ''.join(decrypted)
            return self.remove_padding(result)

        def remove_padding(self, text):
            if not text:
                return text
            
            result = []
            i = 0
            
            while i < len(text):
                char = text[i]
                
                if char == 'X' and i == len(text) - 1:
                    pass  # Skip trailing X
                elif (char == 'X' and 
                      i > 0 and i < len(text) - 1 and 
                      text[i-1] == text[i+1]):
                    pass  # Skip X between duplicates
                else:
                    result.append(char)
                
                i += 1
            
            return ''.join(result)

# Initialize cipher objects
caesar_cipher = CaesarCipher()
vigener_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
transposition_cipher = TranspositionCipher()
playfair_cipher = PlayFairCipher()

@app.route('/')
def home():
    return render_template('index.html')

# CAESAR CIPHER ROUTES
@app.route('/caesar')
def caesar_page():
    return render_cipher_page('caesar')

@app.route('/caesar/encrypt', methods=['GET', 'POST'])
def caesar_encrypt():
    if request.method == 'GET':
        return redirect('/caesar')
    
    try:
        plain_text = request.form.get('plain_text', '')
        key = int(request.form.get('key', 0))
        encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
        return render_cipher_page('caesar', encrypt_result=encrypted_text)
    except Exception as e:
        return render_cipher_page('caesar', encrypt_result=f"Error: {str(e)}")

@app.route('/caesar/decrypt', methods=['GET', 'POST'])
def caesar_decrypt():
    if request.method == 'GET':
        return redirect('/caesar')
    
    try:
        cipher_text = request.form.get('cipher_text', '')
        key = int(request.form.get('key', 0))
        decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
        return render_cipher_page('caesar', decrypt_result=decrypted_text)
    except Exception as e:
        return render_cipher_page('caesar', decrypt_result=f"Error: {str(e)}")

# VIGENERE CIPHER ROUTES
@app.route('/vigener')
def vigener_page():
    return render_cipher_page('vigener')

@app.route('/vigener/encrypt', methods=['GET', 'POST'])
def vigener_encrypt():
    if request.method == 'GET':
        return redirect('/vigener')
    
    try:
        plain_text = request.form.get('plain_text', '')
        key = request.form.get('key', '')
        encrypted_text = vigener_cipher.vigenere_encrypt(plain_text, key)
        return render_cipher_page('vigener', encrypt_result=encrypted_text)
    except Exception as e:
        return render_cipher_page('vigener', encrypt_result=f"Error: {str(e)}")

@app.route('/vigener/decrypt', methods=['GET', 'POST'])
def vigener_decrypt():
    if request.method == 'GET':
        return redirect('/vigener')
    
    try:
        cipher_text = request.form.get('cipher_text', '')
        key = request.form.get('key', '')
        decrypted_text = vigener_cipher.vigenere_decrypt(cipher_text, key)
        return render_cipher_page('vigener', decrypt_result=decrypted_text)
    except Exception as e:
        return render_cipher_page('vigener', decrypt_result=f"Error: {str(e)}")

# RAILFENCE CIPHER ROUTES
@app.route('/railfence')
def railfence_page():
    return render_cipher_page('railfence')

@app.route('/railfence/encrypt', methods=['GET', 'POST'])
def railfence_encrypt():
    if request.method == 'GET':
        return redirect('/railfence')
    
    try:
        plain_text = request.form.get('plain_text', '')
        key = int(request.form.get('key', 0))
        encrypted_text = railfence_cipher.rail_fence_encrypt(plain_text, key)
        return render_cipher_page('railfence', encrypt_result=encrypted_text)
    except Exception as e:
        return render_cipher_page('railfence', encrypt_result=f"Error: {str(e)}")

@app.route('/railfence/decrypt', methods=['GET', 'POST'])
def railfence_decrypt():
    if request.method == 'GET':
        return redirect('/railfence')
    
    try:
        cipher_text = request.form.get('cipher_text', '')
        key = int(request.form.get('key', 0))
        decrypted_text = railfence_cipher.rail_fence_decrypt(cipher_text, key)
        return render_cipher_page('railfence', decrypt_result=decrypted_text)
    except Exception as e:
        return render_cipher_page('railfence', decrypt_result=f"Error: {str(e)}")

# TRANSPOSITION CIPHER ROUTES
@app.route('/transposition')
def transposition_page():
    return render_cipher_page('transposition')

@app.route('/transposition/encrypt', methods=['GET', 'POST'])
def transposition_encrypt():
    if request.method == 'GET':
        return redirect('/transposition')
    
    try:
        plain_text = request.form.get('plain_text', '')
        key = int(request.form.get('key', 0))
        encrypted_text = transposition_cipher.encrypt(plain_text, key)
        return render_cipher_page('transposition', encrypt_result=encrypted_text)
    except Exception as e:
        return render_cipher_page('transposition', encrypt_result=f"Error: {str(e)}")

@app.route('/transposition/decrypt', methods=['GET', 'POST'])
def transposition_decrypt():
    if request.method == 'GET':
        return redirect('/transposition')
    
    try:
        cipher_text = request.form.get('cipher_text', '')
        key = int(request.form.get('key', 0))
        decrypted_text = transposition_cipher.decrypt(cipher_text, key)
        return render_cipher_page('transposition', decrypt_result=decrypted_text)
    except Exception as e:
        return render_cipher_page('transposition', decrypt_result=f"Error: {str(e)}")

# PLAYFAIR CIPHER ROUTES
@app.route('/playfair')
def playfair_page():
    return render_cipher_page('playfair')

@app.route('/playfair/encrypt', methods=['GET', 'POST'])
def playfair_encrypt():
    if request.method == 'GET':
        return redirect('/playfair')
    
    try:
        plain_text = request.form.get('plain_text', '')
        key = request.form.get('key', '')
        matrix = playfair_cipher.create_playfair_matrix(key)
        encrypted_text = playfair_cipher.playfair_encrypt(plain_text, matrix)
        return render_cipher_page('playfair', encrypt_result=encrypted_text, matrix=matrix)
    except Exception as e:
        return render_cipher_page('playfair', encrypt_result=f"Error: {str(e)}")

@app.route('/playfair/decrypt', methods=['GET', 'POST'])
def playfair_decrypt():
    if request.method == 'GET':
        return redirect('/playfair')
    
    try:
        cipher_text = request.form.get('cipher_text', '')
        key = request.form.get('key', '')
        matrix = playfair_cipher.create_playfair_matrix(key)
        decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, matrix)
        return render_cipher_page('playfair', decrypt_result=decrypted_text, matrix=matrix)
    except Exception as e:
        return render_cipher_page('playfair', decrypt_result=f"Error: {str(e)}")

# API Routes
@app.route('/api/info')
def api_info():
    return jsonify({
        'name': 'Cryptography Demo - HUTECH',
        'version': '1.0',
        'algorithms': list(CIPHER_CONFIGS.keys()),
        'endpoints': {
            'web': ['/', '/caesar', '/vigener', '/railfence', '/transposition', '/playfair'],
            'api': ['/api/info']
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('home'))

@app.errorhandler(405)
def method_not_allowed(error):
    return redirect(url_for('home'))

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting HUTECH Cryptography Demo")
    print("📁 Current directory:", os.getcwd())
    print("📂 Templates folder:", os.path.exists('templates'))
    print("📂 Cipher folder:", os.path.exists('cipher'))
    print("🌐 Access at: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, port=5000, host='0.0.0.0')