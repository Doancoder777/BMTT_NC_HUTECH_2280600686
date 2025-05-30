from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigener import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher  # THÊM PlayFair
from cipher.transposition import TranspositionCipher  # THÊM Transposition

app = Flask(__name__)

# CIPHER ALGORITHMS
caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
playfair_cipher = PlayFairCipher()  # THÊM
transposition_cipher = TranspositionCipher()  # THÊM

# Error handling decorator
def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return jsonify({'error': f'Missing required field: {str(e)}'}), 400
        except ValueError as e:
            return jsonify({'error': f'Invalid value: {str(e)}'}), 400
        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    wrapper.__name__ = func.__name__
    return wrapper

# CAESAR CIPHER ROUTES
@app.route("/caesar/encrypt", methods=["POST"])
@app.route("/api/caesar/encrypt", methods=["POST"])
@handle_errors
def caesar_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route("/caesar/decrypt", methods=["POST"])
@app.route("/api/caesar/decrypt", methods=["POST"])
@handle_errors
def caesar_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_text})

# VIGENERE CIPHER ROUTES
@app.route('/api/vigenere/encrypt', methods=['POST'])
@handle_errors
def vigenere_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    encrypted_text = vigenere_cipher.vigenere_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/vigenere/decrypt', methods=['POST'])
@handle_errors
def vigenere_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    decrypted_text = vigenere_cipher.vigenere_decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})

# RAILFENCE CIPHER ROUTES
@app.route('/api/railfence/encrypt', methods=['POST'])
@handle_errors
def railfence_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = railfence_cipher.rail_fence_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/railfence/decrypt', methods=['POST'])
@handle_errors
def railfence_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = railfence_cipher.rail_fence_decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})

# PLAYFAIR CIPHER ROUTES
@app.route('/api/playfair/encrypt', methods=['POST'])
@app.route('/playfair/encrypt', methods=['POST'])  # Backward compatibility
@handle_errors
def playfair_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    
    # Tạo matrix từ key
    matrix = playfair_cipher.create_playfair_matrix(key)
    encrypted_text = playfair_cipher.playfair_encrypt(plain_text, matrix)
    
    return jsonify({
        'encrypted_text': encrypted_text,
        'matrix': matrix
    })

@app.route('/api/playfair/decrypt', methods=['POST'])
@app.route('/playfair/decrypt', methods=['POST'])  # Backward compatibility
@handle_errors
def playfair_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    
    # Tạo matrix từ key
    matrix = playfair_cipher.create_playfair_matrix(key)
    decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, matrix)
    
    return jsonify({
        'decrypted_text': decrypted_text,
        'matrix': matrix
    })

# TRANSPOSITION CIPHER ROUTES
@app.route('/api/transposition/encrypt', methods=['POST'])
@app.route('/transposition/encrypt', methods=['POST'])  # Backward compatibility
@handle_errors
def transposition_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    
    if key <= 0:
        return jsonify({'error': 'Key must be a positive integer'}), 400
    
    encrypted_text = transposition_cipher.encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/transposition/decrypt', methods=['POST'])
@app.route('/transposition/decrypt', methods=['POST'])  # Backward compatibility
@handle_errors
def transposition_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    
    if key <= 0:
        return jsonify({'error': 'Key must be a positive integer'}), 400
    
    decrypted_text = transposition_cipher.decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})

# API INFO ROUTE
@app.route('/api/info', methods=['GET'])
def api_info():
    return jsonify({
        'name': 'Cipher API',
        'version': '2.0',
        'supported_algorithms': [
            'Caesar Cipher',
            'Vigenere Cipher', 
            'Rail Fence Cipher',
            'PlayFair Cipher',
            'Transposition Cipher'
        ],
        'endpoints': {
            'caesar': ['/api/caesar/encrypt', '/api/caesar/decrypt'],
            'vigenere': ['/api/vigenere/encrypt', '/api/vigenere/decrypt'],
            'railfence': ['/api/railfence/encrypt', '/api/railfence/decrypt'],
            'playfair': ['/api/playfair/encrypt', '/api/playfair/decrypt'],
            'transposition': ['/api/transposition/encrypt', '/api/transposition/decrypt']
        }
    })

# HEALTH CHECK
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'API is running'})

# DEBUG ROUTES - List all available routes
@app.route('/routes')
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        output.append(f"{rule.endpoint}: {rule.rule} [{methods}]")
    return '<br>'.join(sorted(output))

# main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)