# cipher_configs.py - Configuration cho tất cả thuật toán mã hóa

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