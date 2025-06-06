import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QTextEdit, 
                           QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton,
                           QTabWidget, QScrollArea, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ui.rsa_cipher import Ui_RSA_Cipher
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RSA_Cipher()
        self.ui.setupUi(self)
        
        # Connect buttons
        self.ui.btn_generate_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)
        
        # Add key display section to the UI
        self.setup_key_display()
        
        # Load existing keys if available
        self.load_and_display_keys()

    def setup_key_display(self):
        """Add key display widgets to the existing UI"""
        try:
            # Create a new widget for key display
            self.key_widget = QWidget()
            key_layout = QVBoxLayout()
            
            # Title
            title_label = QLabel("🔑 RSA Key Information")
            title_label.setFont(QFont("Arial", 12, QFont.Bold))
            title_label.setAlignment(Qt.AlignCenter)
            key_layout.addWidget(title_label)
            
            # Public Key Section
            pub_label = QLabel("📂 Public Key:")
            pub_label.setFont(QFont("Arial", 10, QFont.Bold))
            key_layout.addWidget(pub_label)
            
            self.public_key_display = QTextEdit()
            self.public_key_display.setMaximumHeight(120)
            self.public_key_display.setFont(QFont("Courier", 8))
            self.public_key_display.setReadOnly(True)
            self.public_key_display.setPlaceholderText("Public key will be displayed here after generation...")
            key_layout.addWidget(self.public_key_display)
            
            # Private Key Section
            priv_label = QLabel("🔐 Private Key:")
            priv_label.setFont(QFont("Arial", 10, QFont.Bold))
            key_layout.addWidget(priv_label)
            
            self.private_key_display = QTextEdit()
            self.private_key_display.setMaximumHeight(120)
            self.private_key_display.setFont(QFont("Courier", 8))
            self.private_key_display.setReadOnly(True)
            self.private_key_display.setPlaceholderText("Private key will be displayed here after generation...")
            key_layout.addWidget(self.private_key_display)
            
            # Key Status
            self.key_status_label = QLabel("Status: No keys found")
            self.key_status_label.setFont(QFont("Arial", 9))
            self.key_status_label.setStyleSheet("color: orange;")
            key_layout.addWidget(self.key_status_label)
            
            # Buttons for key management
            button_layout = QHBoxLayout()
            
            self.refresh_keys_btn = QPushButton("🔄 Refresh Keys")
            self.refresh_keys_btn.clicked.connect(self.load_and_display_keys)
            button_layout.addWidget(self.refresh_keys_btn)
            
            self.copy_public_btn = QPushButton("📋 Copy Public Key")
            self.copy_public_btn.clicked.connect(self.copy_public_key)
            button_layout.addWidget(self.copy_public_btn)
            
            self.copy_private_btn = QPushButton("📋 Copy Private Key")
            self.copy_private_btn.clicked.connect(self.copy_private_key)
            button_layout.addWidget(self.copy_private_btn)
            
            key_layout.addLayout(button_layout)
            
            self.key_widget.setLayout(key_layout)
            
            # Add to main window (try different approaches)
            try:
                # Method 1: Add as a separate window
                self.key_window = QWidget()
                self.key_window.setLayout(key_layout)
                self.key_window.setWindowTitle("RSA Keys Display")
                self.key_window.setGeometry(800, 100, 600, 400)
                self.key_window.show()
                
            except Exception as e:
                print(f"Could not add key display to main UI: {e}")
                # Create standalone key window
                self.show_key_window()
                
        except Exception as e:
            print(f"Error setting up key display: {e}")

    def show_key_window(self):
        """Show keys in a separate window"""
        try:
            self.key_window = QWidget()
            self.key_window.setWindowTitle("🔑 RSA Keys Display")
            self.key_window.setGeometry(800, 100, 600, 500)
            
            layout = QVBoxLayout()
            
            # Title
            title = QLabel("🔑 RSA Key Management")
            title.setFont(QFont("Arial", 14, QFont.Bold))
            title.setAlignment(Qt.AlignCenter)
            title.setStyleSheet("color: #2E86AB; margin: 10px;")
            layout.addWidget(title)
            
            # Public Key
            pub_frame = QFrame()
            pub_frame.setFrameStyle(QFrame.Box)
            pub_layout = QVBoxLayout()
            
            pub_label = QLabel("📂 Public Key")
            pub_label.setFont(QFont("Arial", 11, QFont.Bold))
            pub_layout.addWidget(pub_label)
            
            self.public_key_display = QTextEdit()
            self.public_key_display.setMaximumHeight(100)
            self.public_key_display.setFont(QFont("Courier", 8))
            self.public_key_display.setReadOnly(True)
            pub_layout.addWidget(self.public_key_display)
            
            pub_frame.setLayout(pub_layout)
            layout.addWidget(pub_frame)
            
            # Private Key  
            priv_frame = QFrame()
            priv_frame.setFrameStyle(QFrame.Box)
            priv_layout = QVBoxLayout()
            
            priv_label = QLabel("🔐 Private Key")
            priv_label.setFont(QFont("Arial", 11, QFont.Bold))
            priv_layout.addWidget(priv_label)
            
            self.private_key_display = QTextEdit()
            self.private_key_display.setMaximumHeight(100)
            self.private_key_display.setFont(QFont("Courier", 8))
            self.private_key_display.setReadOnly(True)
            priv_layout.addWidget(self.private_key_display)
            
            priv_frame.setLayout(priv_layout)
            layout.addWidget(priv_frame)
            
            # Status
            self.key_status_label = QLabel("Status: Checking for keys...")
            self.key_status_label.setFont(QFont("Arial", 10))
            layout.addWidget(self.key_status_label)
            
            # Buttons
            button_layout = QHBoxLayout()
            
            refresh_btn = QPushButton("🔄 Refresh")
            refresh_btn.clicked.connect(self.load_and_display_keys)
            button_layout.addWidget(refresh_btn)
            
            copy_pub_btn = QPushButton("📋 Copy Public")
            copy_pub_btn.clicked.connect(self.copy_public_key)
            button_layout.addWidget(copy_pub_btn)
            
            copy_priv_btn = QPushButton("📋 Copy Private")
            copy_priv_btn.clicked.connect(self.copy_private_key)
            button_layout.addWidget(copy_priv_btn)
            
            layout.addLayout(button_layout)
            
            self.key_window.setLayout(layout)
            self.key_window.show()
            
        except Exception as e:
            print(f"Error creating key window: {e}")

    def load_and_display_keys(self):
        """Load RSA keys from files and display them"""
        try:
            public_key_path = 'cipher/rsa/keys/publicKey.pem'
            private_key_path = 'cipher/rsa/keys/privateKey.pem'
            
            public_key_exists = os.path.exists(public_key_path)
            private_key_exists = os.path.exists(private_key_path)
            
            if public_key_exists and private_key_exists:
                # Read public key
                try:
                    with open(public_key_path, 'r') as f:
                        public_key_content = f.read()
                    self.public_key_display.setPlainText(public_key_content)
                except Exception as e:
                    self.public_key_display.setPlainText(f"Error reading public key: {e}")
                
                # Read private key
                try:
                    with open(private_key_path, 'r') as f:
                        private_key_content = f.read()
                    self.private_key_display.setPlainText(private_key_content)
                except Exception as e:
                    self.private_key_display.setPlainText(f"Error reading private key: {e}")
                
                self.key_status_label.setText("✅ Status: RSA keys loaded successfully")
                self.key_status_label.setStyleSheet("color: green;")
                
                print("✅ RSA keys loaded and displayed in GUI")
                
            else:
                self.public_key_display.setPlainText("No public key found. Please generate keys first.")
                self.private_key_display.setPlainText("No private key found. Please generate keys first.")
                self.key_status_label.setText("⚠️ Status: No RSA keys found")
                self.key_status_label.setStyleSheet("color: orange;")
                
                print("⚠️ No RSA keys found")
                
        except Exception as e:
            error_msg = f"Error loading keys: {e}"
            self.public_key_display.setPlainText(error_msg)
            self.private_key_display.setPlainText(error_msg)
            self.key_status_label.setText(f"❌ Status: {error_msg}")
            self.key_status_label.setStyleSheet("color: red;")
            print(f"❌ {error_msg}")

    def copy_public_key(self):
        """Copy public key to clipboard"""
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.public_key_display.toPlainText())
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("📋 Public key copied to clipboard!")
            msg.exec_()
        except Exception as e:
            print(f"Error copying public key: {e}")

    def copy_private_key(self):
        """Copy private key to clipboard"""
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.private_key_display.toPlainText())
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("🔐 Private key copied to clipboard!\n⚠️ Keep it secure!")
            msg.exec_()
        except Exception as e:
            print(f"Error copying private key: {e}")

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            response = requests.get(url)
            print(f"Generate Keys Response: {response.status_code}")
            print(f"Response text: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Display success message
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data.get("message", "RSA Keys generated successfully!"))
                msg.exec_()
                
                # Refresh the key display
                self.load_and_display_keys()
                
                # Show key window if not visible
                if not hasattr(self, 'key_window') or not self.key_window.isVisible():
                    self.show_key_window()
                    
            else:
                print("Error while calling API")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"API Error: {response.status_code}")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print("Error: %s" % str(e))
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Connection Error: {str(e)}")
            msg.exec_()

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        
        message = self.ui.txt_plain_text.toPlainText().strip()
        if not message:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please enter plain text to encrypt!")
            msg.exec_()
            return
        
        payload = {
            "message": message,
            "key_type": "public"
        }
        
        try:
            response = requests.post(url, json=payload)
            print(f"Encrypt Response: {response.status_code}")
            print(f"Response text: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                encrypted_message = data.get("encrypted_message", "")
                self.ui.txt_cipher_text.setPlainText(encrypted_message)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("🔐 Encrypted Successfully!")
                msg.exec_()
            else:
                print("Error while calling API")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"API Error: {response.status_code}")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print("Error: %s" % str(e))
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Connection Error: {str(e)}")
            msg.exec_()

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        
        ciphertext = self.ui.txt_cipher_text.toPlainText().strip()
        if not ciphertext:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please enter cipher text to decrypt!")
            msg.exec_()
            return
        
        payload = {
            "ciphertext": ciphertext,
            "key_type": "private"
        }
        
        try:
            response = requests.post(url, json=payload)
            print(f"Decrypt Response: {response.status_code}")
            print(f"Response text: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                decrypted_message = data.get("decrypted_message", "")
                self.ui.txt_plain_text.setPlainText(decrypted_message)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("🔓 Decrypted Successfully!")
                msg.exec_()
            else:
                print("Error while calling API")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"API Error: {response.status_code}")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print("Error: %s" % str(e))
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Connection Error: {str(e)}")
            msg.exec_()

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        
        message = self.ui.txt_information.toPlainText().strip()
        if not message:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please enter information to sign!")
            msg.exec_()
            return
        
        payload = {
            "message": message
        }
        
        try:
            response = requests.post(url, json=payload)
            print(f"Sign Response: {response.status_code}")
            print(f"Response text: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                signature = data.get("signature", "")
                self.ui.txt_signature.setPlainText(signature)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("✍️ Signed Successfully!")
                msg.exec_()
            else:
                print("Error while calling API")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"API Error: {response.status_code}")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print("Error: %s" % str(e))
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Connection Error: {str(e)}")
            msg.exec_()

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        
        message = self.ui.txt_information.toPlainText().strip()
        signature = self.ui.txt_signature.toPlainText().strip()
        
        if not message or not signature:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please enter both information and signature!")
            msg.exec_()
            return
        
        payload = {
            "message": message,
            "signature": signature
        }
        
        try:
            response = requests.post(url, json=payload)
            print(f"Verify Response: {response.status_code}")
            print(f"Response text: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                is_verified = data.get("is_verified", False)
                
                msg = QMessageBox()
                if is_verified:
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("✅ Signature Verified Successfully!")
                else:
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("❌ Signature Verification Failed!")
                msg.exec_()
            else:
                print("Error while calling API")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"API Error: {response.status_code}")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print("Error: %s" % str(e))
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Connection Error: {str(e)}")
            msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())