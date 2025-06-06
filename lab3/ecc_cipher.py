import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.ecc import Ui_ECCCipher
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ECCCipher()
        self.ui.setupUi(self)

        self.ui.btn_generate_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/ecc/generate_keys"
        try:
            print(f"🔄 Calling ECC generate keys API...")
            response = requests.get(url)
            print(f"Generate Keys Response: {response.status_code}")
            print(f"Response text: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("🔑 " + data.get("message", "ECC Keys generated successfully!"))
                msg.exec_()
            else:
                print("❌ Error while calling API")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"API Error: {response.status_code}")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print("❌ Connection Error: %s" % str(e))
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Connection Error: {str(e)}")
            msg.exec_()

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/ecc/sign"
        
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
        
        print(f"🔄 Calling ECC sign API...")
        print(f"Sign payload: {payload}")
        
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
                msg.setText("✍️ ECC Signed Successfully!")
                msg.exec_()
            else:
                print("❌ Error while calling API")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"API Error: {response.status_code}")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print("❌ Connection Error: %s" % str(e))
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Connection Error: {str(e)}")
            msg.exec_()

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/ecc/verify"
        
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
        
        print(f"🔄 Calling ECC verify API...")
        print(f"Verify payload: {payload}")
        
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
                    msg.setText("✅ ECC Signature Verified Successfully!")
                else:
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("❌ ECC Signature Verification Failed!")
                msg.exec_()
            else:
                print("❌ Error while calling API")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"API Error: {response.status_code}")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print("❌ Connection Error: %s" % str(e))
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Connection Error: {str(e)}")
            msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())