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
    

# CAESAR CIPHER ROUTES (ORIGINAL)
@app.route("/caesar/encrypt", methods=["POST"])
@handle_errors
def caesar_encrypt_original():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route("/caesar/decrypt", methods=["POST"])
@handle_errors
def caesar_decrypt_original():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_text})

# CAESAR CIPHER API ROUTES (Lab3 Compatible)
@app.route("/api/caesar/encrypt", methods=["POST"])
@handle_errors
def caesar_encrypt_api():
    data = request.json
    
    # Hỗ trợ cả 2 format: Lab3 format và standard format
    plain_text = data.get('txt_Plaintext', data.get('plain_text', ''))
    key_raw = data.get('txt_Key', data.get('key', 0))
    
    # Convert key to int
    if isinstance(key_raw, str):
        key = int(key_raw) if key_raw.strip() else 0
    else:
        key = int(key_raw)
    
    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    
    return jsonify({
        'encrypted_message': encrypted_text,
        'success': True,
        'original_text': plain_text,
        'key_used': key
    })

@app.route("/api/caesar/decrypt", methods=["POST"])
@handle_errors
def caesar_decrypt_api():
    data = request.json
    
    # Hỗ trợ cả 2 format: Lab3 format và standard format
    cipher_text = data.get('txt_Ciphertext', data.get('cipher_text', ''))
    key_raw = data.get('txt_Key', data.get('key', 0))
    
    # Convert key to int
    if isinstance(key_raw, str):
        key = int(key_raw) if key_raw.strip() else 0
    else:
        key = int(key_raw)
    
    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
    
    return jsonify({
        'decrypted_message': decrypted_text,
        'success': True,
        'original_cipher': cipher_text,
        'key_used': key
    })

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
        'version': '2.1 - Lab3 Compatible',
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
        },
        'lab3_support': True,
        'supported_formats': {
            'lab3_format': {
                'encrypt': {'txt_Plaintext': 'string', 'txt_Key': 'string'},
                'decrypt': {'txt_Ciphertext': 'string', 'txt_Key': 'string'}
            },
            'standard_format': {
                'encrypt': {'plain_text': 'string', 'key': 'int'},
                'decrypt': {'cipher_text': 'string', 'key': 'int'}
            }
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
# THÊM VÀO CUỐI FILE api.py (trước if __name__ == "__main__")

# =====================================
# ECC CIPHER ROUTES - THÊM PHẦN NÀY
# =====================================

@app.route('/api/ecc/generate_keys', methods=['GET'])
@handle_errors
def ecc_generate_keys():
    try:
        ecc_cipher.generate_keys()
        return jsonify({
            'success': True,
            'message': 'ECC Keys generated successfully!',
            'public_key_path': 'cipher/ecc/keys/publicKey.pem',
            'private_key_path': 'cipher/ecc/keys/privateKey.pem'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to generate ECC keys: {str(e)}'
        }), 500

@app.route('/api/ecc/sign', methods=['POST'])
@handle_errors
def ecc_sign():
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    try:
        # For ECC, we typically use the private key for signing
        signature = ecc_cipher.sign(message)
        
        # Convert to base64 string if it's bytes
        if isinstance(signature, bytes):
            signature_str = base64.b64encode(signature).decode('utf-8')
        else:
            signature_str = str(signature)
        
        return jsonify({
            'success': True,
            'signature': signature_str,
            'message': message,
            'algorithm': 'ECC'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'ECC signing failed: {str(e)}'
        }), 500

@app.route('/api/ecc/verify', methods=['POST'])
@handle_errors
def ecc_verify():
    data = request.json
    message = data.get('message', '')
    signature = data.get('signature', '')
    
    if not message or not signature:
        return jsonify({'error': 'Message and signature are required'}), 400
    
    try:
        # Convert from base64 if needed
        try:
            signature_bytes = base64.b64decode(signature)
        except:
            signature_bytes = signature
        
        # Verify with public key
        is_verified = ecc_cipher.verify(message, signature_bytes)
        
        return jsonify({
            'success': True,
            'is_verified': bool(is_verified),
            'message': message,
            'algorithm': 'ECC'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'ECC verification failed: {str(e)}',
            'is_verified': False
        }), 500

@app.route('/api/ecc/encrypt', methods=['POST'])
@handle_errors
def ecc_encrypt():
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    try:
        encrypted_message = ecc_cipher.encrypt(message)
        
        # Convert to string if needed
        if isinstance(encrypted_message, bytes):
            encrypted_str = base64.b64encode(encrypted_message).decode('utf-8')
        else:
            encrypted_str = str(encrypted_message)
        
        return jsonify({
            'success': True,
            'encrypted_message': encrypted_str,
            'original_message': message,
            'algorithm': 'ECC'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'ECC encryption failed: {str(e)}'
        }), 500

@app.route('/api/ecc/decrypt', methods=['POST'])
@handle_errors
def ecc_decrypt():
    data = request.json
    ciphertext = data.get('ciphertext', '')
    
    if not ciphertext:
        return jsonify({'error': 'Ciphertext is required'}), 400
    
    try:
        # Convert from base64 if needed
        try:
            cipher_bytes = base64.b64decode(ciphertext)
        except:
            cipher_bytes = ciphertext
            
        decrypted_message = ecc_cipher.decrypt(cipher_bytes)
        
        return jsonify({
            'success': True,
            'decrypted_message': decrypted_message,
            'algorithm': 'ECC'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'ECC decryption failed: {str(e)}'
        }), 500
# TEST ROUTE - Test Lab3 compatibility
@app.route('/test/lab3', methods=['GET'])
def test_lab3():
    return jsonify({
        'message': 'Lab3 API Test Endpoint',
        'test_encrypt_url': '/api/caesar/encrypt',
        'test_decrypt_url': '/api/caesar/decrypt',
        'sample_encrypt_payload': {
            'txt_Plaintext': 'HELLO',
            'txt_Key': '3'
        },
        'sample_decrypt_payload': {
            'txt_Ciphertext': 'KHOOR',
            'txt_Key': '3'
        }
    })

# main function
if __name__ == "__main__":
    print("🚀 Starting Cipher API Server...")
    print("📡 Lab3 Compatible - Version 2.1")
    print("🌐 Access at: http://localhost:5000")
    print("📋 API Info: http://localhost:5000/api/info")
    print("🧪 Test Lab3: http://localhost:5000/test/lab3")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)