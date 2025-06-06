import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow
import requests
import json

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_Encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_Decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        
        # Lấy data từ UI
        plaintext = self.ui.txt_Plaintext.toPlainText().strip()
        key_text = self.ui.txt_Key.toPlainText().strip()
        
        print(f"Debug - Plaintext: '{plaintext}'")
        print(f"Debug - Key text: '{key_text}'")
        
        # Validate input
        if not plaintext:
            self.show_error("Vui lòng nhập plaintext!")
            return
            
        if not key_text:
            self.show_error("Vui lòng nhập key!")
            return
            
        try:
            key = int(key_text)
            if key < 0 or key > 25:
                self.show_error("Key phải từ 0-25!")
                return
        except ValueError:
            self.show_error("Key phải là số nguyên!")
            return
        
        # Tạo payload với cả 2 format để đảm bảo tương thích
        payload = {
            # Lab3 format
            "txt_Plaintext": plaintext,
            "txt_Key": str(key),
            # Standard format backup
            "plain_text": plaintext,
            "key": key
        }
        
        print(f"Debug - Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(url, json=payload, timeout=5)
            print(f"Debug - Response status: {response.status_code}")
            print(f"Debug - Response text: {response.text}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"Debug - Response data: {json.dumps(data, indent=2)}")
                    
                    # Thử các field name khác nhau
                    encrypted_text = (data.get("encrypted_message") or 
                                    data.get("encrypted_text") or 
                                    data.get("result") or "")
                    
                    if encrypted_text:
                        # ✅ THỬ CÁC TÊN COMPONENT KHÁC NHAU
                        try:
                            # Thử các tên có thể có
                            if hasattr(self.ui, 'textEdit_3'):
                                self.ui.textEdit_3.setPlainText(encrypted_text)
                            elif hasattr(self.ui, 'txt_Ciphertext'):
                                self.ui.txt_Ciphertext.setPlainText(encrypted_text)
                            elif hasattr(self.ui, 'textEdit_Encrypted'):
                                self.ui.textEdit_Encrypted.setPlainText(encrypted_text)
                            elif hasattr(self.ui, 'txt_Encrypted'):
                                self.ui.txt_Encrypted.setPlainText(encrypted_text)
                            elif hasattr(self.ui, 'textEdit'):
                                self.ui.textEdit.setPlainText(encrypted_text)
                            else:
                                # Nếu không tìm thấy, list tất cả attributes
                                print("Available UI attributes:")
                                ui_attrs = [attr for attr in dir(self.ui) if not attr.startswith('_') and 'text' in attr.lower()]
                                for attr in ui_attrs:
                                    print(f"  - {attr}")
                                self.show_error(f"Không tìm thấy textbox output!\nKết quả: {encrypted_text}")
                                return
                            
                            self.show_success("Mã hóa thành công!")
                            
                        except Exception as e:
                            self.show_error(f"Lỗi set text: {str(e)}")
                    else:
                        self.show_error(f"Không tìm thấy kết quả mã hóa. Response: {data}")
                        
                except json.JSONDecodeError as e:
                    self.show_error(f"Lỗi parse JSON: {e}")
                    
            else:
                error_msg = f"API Error {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('error', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                    
                self.show_error(error_msg)
                
        except requests.exceptions.ConnectionError:
            self.show_error("Không thể kết nối đến API server!\nHãy kiểm tra server có chạy không.")
        except requests.exceptions.Timeout:
            self.show_error("Timeout khi gọi API!")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Lỗi request: {str(e)}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        
        # Lấy data từ UI
        # ✅ THỬ CÁC CÁCH LẤY CIPHERTEXT
        ciphertext = ""
        if hasattr(self.ui, 'txt_Ciphertext'):
            ciphertext = self.ui.txt_Ciphertext.toPlainText().strip()
        elif hasattr(self.ui, 'textEdit_3'):
            ciphertext = self.ui.textEdit_3.toPlainText().strip()
        elif hasattr(self.ui, 'textEdit_Encrypted'):
            ciphertext = self.ui.textEdit_Encrypted.toPlainText().strip()
        else:
            self.show_error("Không tìm thấy textbox ciphertext!")
            return
            
        key_text = self.ui.txt_Key.toPlainText().strip()
        
        print(f"Debug - Ciphertext: '{ciphertext}'")
        print(f"Debug - Key text: '{key_text}'")
        
        # Validate input
        if not ciphertext:
            self.show_error("Vui lòng nhập ciphertext!")
            return
            
        if not key_text:
            self.show_error("Vui lòng nhập key!")
            return
            
        try:
            key = int(key_text)
            if key < 0 or key > 25:
                self.show_error("Key phải từ 0-25!")
                return
        except ValueError:
            self.show_error("Key phải là số nguyên!")
            return
        
        # Tạo payload
        payload = {
            # Lab3 format
            "txt_Ciphertext": ciphertext,
            "txt_Key": str(key),
            # Standard format backup
            "cipher_text": ciphertext,
            "key": key
        }
        
        print(f"Debug - Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(url, json=payload, timeout=5)
            print(f"Debug - Response status: {response.status_code}")
            print(f"Debug - Response text: {response.text}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"Debug - Response data: {json.dumps(data, indent=2)}")
                    
                    # Thử các field name khác nhau
                    decrypted_text = (data.get("decrypted_message") or 
                                    data.get("decrypted_text") or 
                                    data.get("result") or "")
                    
                    if decrypted_text:
                        # ✅ THỬ CÁC TÊN COMPONENT OUTPUT
                        try:
                            if hasattr(self.ui, 'textEdit'):
                                self.ui.textEdit.setPlainText(decrypted_text)
                            elif hasattr(self.ui, 'txt_Plaintext_Output'):
                                self.ui.txt_Plaintext_Output.setPlainText(decrypted_text)
                            elif hasattr(self.ui, 'textEdit_Decrypted'):
                                self.ui.textEdit_Decrypted.setPlainText(decrypted_text)
                            else:
                                print("Available UI attributes for decrypt output:")
                                ui_attrs = [attr for attr in dir(self.ui) if not attr.startswith('_') and 'text' in attr.lower()]
                                for attr in ui_attrs:
                                    print(f"  - {attr}")
                                self.show_error(f"Không tìm thấy textbox decrypt output!\nKết quả: {decrypted_text}")
                                return
                                
                            self.show_success("Giải mã thành công!")
                            
                        except Exception as e:
                            self.show_error(f"Lỗi set text: {str(e)}")
                    else:
                        self.show_error(f"Không tìm thấy kết quả giải mã. Response: {data}")
                        
                except json.JSONDecodeError as e:
                    self.show_error(f"Lỗi parse JSON: {e}")
                    
            else:
                error_msg = f"API Error {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('error', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                    
                self.show_error(error_msg)
                
        except requests.exceptions.ConnectionError:
            self.show_error("Không thể kết nối đến API server!\nHãy kiểm tra server có chạy không.")
        except requests.exceptions.Timeout:
            self.show_error("Timeout khi gọi API!")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Lỗi request: {str(e)}")

    def show_success(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Thành công")
        msg.setText(message)
        msg.exec_()

    def show_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Lỗi")
        msg.setText(message)
        msg.exec_()
        print(f"Error: {message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())