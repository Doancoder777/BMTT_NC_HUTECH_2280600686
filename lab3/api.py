from flask import Flask, request, jsonify
import base64
import sys
import os

# Add cipher modules to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'cipher'))

app = Flask(__name__)

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

# =====================================
# CIPHER ALGORITHMS INITIALIZATION
# =====================================

# Caesar Cipher
try:
    from cipher.caesar import CaesarCipher
    caesar_cipher = CaesarCipher()
    print("✅ Caesar cipher loaded")
except ImportError as e:
    print(f"⚠️ Caesar Import error: {e}")
    # Fallback implementation
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
    
    caesar_cipher = CaesarCipher()

# Vigenere Cipher
try:
    from cipher.vigener import VigenereCipher
    vigenere_cipher = VigenereCipher()
    print("✅ Vigenere cipher loaded")
except ImportError as e:
    print(f"⚠️ Vigenere Import error: {e}")
    class VigenereCipher:
        def vigenere_encrypt(self, text, key):
            return f"VIGENERE_ENCRYPTED({text})"
        def vigenere_decrypt(self, text, key):
            return text.replace("VIGENERE_ENCRYPTED(", "").replace(")", "")
    vigenere_cipher = VigenereCipher()

# Rail Fence Cipher
try:
    from cipher.railfence import RailFenceCipher
    railfence_cipher = RailFenceCipher()
    print("✅ RailFence cipher loaded")
except ImportError as e:
    print(f"⚠️ RailFence Import error: {e}")
    class RailFenceCipher:
        def rail_fence_encrypt(self, text, key):
            return f"RAILFENCE_ENCRYPTED({text})"
        def rail_fence_decrypt(self, text, key):
            return text.replace("RAILFENCE_ENCRYPTED(", "").replace(")", "")
    railfence_cipher = RailFenceCipher()

# PlayFair Cipher
try:
    from cipher.playfair import PlayFairCipher
    playfair_cipher = PlayFairCipher()
    print("✅ PlayFair cipher loaded")
except ImportError as e:
    print(f"⚠️ PlayFair Import error: {e}")
    class PlayFairCipher:
        def create_playfair_matrix(self, key):
            return [['A', 'B', 'C', 'D', 'E']] * 5
        def playfair_encrypt(self, text, matrix):
            return f"PLAYFAIR_ENCRYPTED({text})"
        def playfair_decrypt(self, text, matrix):
            return text.replace("PLAYFAIR_ENCRYPTED(", "").replace(")", "")
    playfair_cipher = PlayFairCipher()

# Transposition Cipher
try:
    from cipher.transposition import TranspositionCipher
    transposition_cipher = TranspositionCipher()
    print("✅ Transposition cipher loaded")
except ImportError as e:
    print(f"⚠️ Transposition Import error: {e}")
    class TranspositionCipher:
        def encrypt(self, text, key):
            return f"TRANSPOSITION_ENCRYPTED({text})"
        def decrypt(self, text, key):
            return text.replace("TRANSPOSITION_ENCRYPTED(", "").replace(")", "")
    transposition_cipher = TranspositionCipher()

# RSA Cipher
try:
    from cipher.rsa.rsa_cipher import RSACipher
    rsa_cipher = RSACipher()
    print("✅ RSA cipher loaded")
except ImportError as e:
    print(f"⚠️ RSA Import error: {e}")
    # Fallback RSA implementation
    class RSACipher:
        def generate_keys(self):
            os.makedirs('cipher/rsa/keys', exist_ok=True)
            print("RSA keys generated (dummy implementation)")
            return True
        
        def load_keys(self):
            return {"public_key": "dummy_public", "private_key": "dummy_private"}
        
        def encrypt(self, message, key):
            return base64.b64encode(f"RSA_ENCRYPTED({message})".encode()).decode()
        
        def decrypt(self, ciphertext, key):
            try:
                decoded = base64.b64decode(ciphertext).decode()
                return decoded.replace("RSA_ENCRYPTED(", "").replace(")", "")
            except:
                return "Decryption failed"
        
        def sign(self, message, key):
            return base64.b64encode(f"RSA_SIGNATURE({message})".encode()).decode()
        
        def verify(self, message, signature, key):
            try:
                decoded = base64.b64decode(signature).decode()
                return f"RSA_SIGNATURE({message})" == decoded
            except:
                return False
    
    rsa_cipher = RSACipher()

# ECC Cipher
try:
    from cipher.ecc.ecc_cipher import ECCCipher
    ecc_cipher = ECCCipher()
    print("✅ ECC cipher loaded")
except ImportError as e:
    print(f"⚠️ ECC Import error: {e}")
    # Fallback ECC implementation
    class ECCCipher:
        def generate_keys(self):
            os.makedirs('cipher/ecc/keys', exist_ok=True)
            print("ECC keys generated (dummy implementation)")
            return True
        
        def encrypt(self, message):
            return base64.b64encode(f"ECC_ENCRYPTED({message})".encode()).decode()
        
        def decrypt(self, ciphertext):
            try:
                decoded = base64.b64decode(ciphertext).decode()
                return decoded.replace("ECC_ENCRYPTED(", "").replace(")", "")
            except:
                return "Decryption failed"
        
        def sign(self, message):
            return base64.b64encode(f"ECC_SIGNATURE({message})".encode()).decode()
        
        def verify(self, message, signature):
            try:
                decoded = base64.b64decode(signature).decode()
                return f"ECC_SIGNATURE({message})" == decoded
            except:
                return False
    
    ecc_cipher = ECCCipher()

# =====================================
# CAESAR CIPHER ROUTES
# =====================================

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

# =====================================
# RSA CIPHER ROUTES
# =====================================

@app.route('/api/rsa/generate_keys', methods=['GET'])
@handle_errors
def rsa_generate_keys():
    try:
        rsa_cipher.generate_keys()
        return jsonify({
            'success': True,
            'message': 'RSA Keys generated successfully!',
            'public_key_path': 'cipher/rsa/keys/publicKey.pem',
            'private_key_path': 'cipher/rsa/keys/privateKey.pem'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to generate RSA keys: {str(e)}'
        }), 500

@app.route('/api/rsa/encrypt', methods=['POST'])
@handle_errors
def rsa_encrypt():
    data = request.json
    message = data.get('message', '')
    key_type = data.get('key_type', 'public')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    try:
        keys = rsa_cipher.load_keys()
        public_key = keys['public_key']
        
        # Encrypt with public key
        encrypted_data = rsa_cipher.encrypt(message, public_key)
        
        # Convert to base64 string if it's bytes
        if isinstance(encrypted_data, bytes):
            encrypted_message = base64.b64encode(encrypted_data).decode('utf-8')
        else:
            encrypted_message = str(encrypted_data)
        
        return jsonify({
            'success': True,
            'encrypted_message': encrypted_message,
            'original_message': message,
            'algorithm': 'RSA'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'RSA encryption failed: {str(e)}'
        }), 500

@app.route('/api/rsa/decrypt', methods=['POST'])
@handle_errors
def rsa_decrypt():
    data = request.json
    ciphertext = data.get('ciphertext', '')
    key_type = data.get('key_type', 'private')
    
    if not ciphertext:
        return jsonify({'error': 'Ciphertext is required'}), 400
    
    try:
        keys = rsa_cipher.load_keys()
        private_key = keys['private_key']
        
        # Convert from base64 if needed
        try:
            cipher_bytes = base64.b64decode(ciphertext)
        except:
            cipher_bytes = ciphertext
        
        # Decrypt with private key
        decrypted_message = rsa_cipher.decrypt(cipher_bytes, private_key)
        
        if decrypted_message == False or decrypted_message == "Decryption failed":
            return jsonify({
                'success': False,
                'error': 'Decryption failed - invalid ciphertext or key'
            }), 400
        
        return jsonify({
            'success': True,
            'decrypted_message': decrypted_message,
            'algorithm': 'RSA'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'RSA decryption failed: {str(e)}'
        }), 500

@app.route('/api/rsa/sign', methods=['POST'])
@handle_errors
def rsa_sign():
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    try:
        keys = rsa_cipher.load_keys()
        private_key = keys['private_key']
        
        # Sign with private key
        signature_data = rsa_cipher.sign(message, private_key)
        
        # Convert to base64 string if it's bytes
        if isinstance(signature_data, bytes):
            signature = base64.b64encode(signature_data).decode('utf-8')
        else:
            signature = str(signature_data)
        
        return jsonify({
            'success': True,
            'signature': signature,
            'message': message,
            'algorithm': 'RSA'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'RSA signing failed: {str(e)}'
        }), 500

@app.route('/api/rsa/verify', methods=['POST'])
@handle_errors
def rsa_verify():
    data = request.json
    message = data.get('message', '')
    signature = data.get('signature', '')
    
    if not message or not signature:
        return jsonify({'error': 'Message and signature are required'}), 400
    
    try:
        keys = rsa_cipher.load_keys()
        public_key = keys['public_key']
        
        # Convert from base64 if needed
        try:
            signature_bytes = base64.b64decode(signature)
        except:
            signature_bytes = signature
        
        # Verify with public key
        is_verified = rsa_cipher.verify(message, signature_bytes, public_key)
        
        return jsonify({
            'success': True,
            'is_verified': bool(is_verified),
            'message': message,
            'algorithm': 'RSA'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'RSA verification failed: {str(e)}',
            'is_verified': False
        }), 500

# =====================================
# ECC CIPHER ROUTES
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

# =====================================
# LEGACY CIPHER ROUTES (for backward compatibility)
# =====================================

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

# =====================================
# UTILITY ROUTES
# =====================================

@app.route('/api/info', methods=['GET'])
def api_info():
    return jsonify({
        'name': 'Lab2 & Lab3 Cryptography API',
        'version': '3.0 - Complete Edition',
        'supported_algorithms': [
            'Caesar Cipher',
            'Vigenere Cipher', 
            'Rail Fence Cipher',
            'PlayFair Cipher',
            'Transposition Cipher',
            'RSA Cipher',
            'ECC Cipher'
        ],
        'endpoints': {
            'caesar': ['/api/caesar/encrypt', '/api/caesar/decrypt'],
            'vigenere': ['/api/vigenere/encrypt', '/api/vigenere/decrypt'],
            'railfence': ['/api/railfence/encrypt', '/api/railfence/decrypt'],
            'playfair': ['/api/playfair/encrypt', '/api/playfair/decrypt'],
            'transposition': ['/api/transposition/encrypt', '/api/transposition/decrypt'],
            'rsa': [
                '/api/rsa/generate_keys',
                '/api/rsa/encrypt', 
                '/api/rsa/decrypt',
                '/api/rsa/sign',
                '/api/rsa/verify'
            ],
            'ecc': [
                '/api/ecc/generate_keys',
                '/api/ecc/encrypt',
                '/api/ecc/decrypt',
                '/api/ecc/sign',
                '/api/ecc/verify'
            ]
        },
        'features': [
            'symmetric_encryption', 
            'asymmetric_encryption', 
            'digital_signatures',
            'elliptic_curve_cryptography',
            'lab2_compatibility',
            'lab3_compatibility'
        ]
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'message': 'Cryptography API is running'
    })

@app.route('/routes', methods=['GET'])
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        output.append(f"{rule.endpoint}: {rule.rule} [{methods}]")
    return '<br>'.join(sorted(output))

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

# =====================================
# MAIN
# =====================================
if __name__ == "__main__":
    print("🚀 Starting Complete Cryptography API Server...")
    print("📡 Supporting: Caesar, Vigenere, RailFence, PlayFair, Transposition, RSA, ECC")
    print("🌐 Access at: http://localhost:5000")
    print("📋 API Info: http://localhost:5000/api/info")
    print("🧪 Test Lab3: http://localhost:5000/test/lab3")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True)