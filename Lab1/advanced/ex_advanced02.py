import re

def extract_and_sum_numbers(input_string):
    """
    Tách và tính tổng các số dương và âm trong chuỗi
    """
    # Sử dụng regex để tìm tất cả các số (bao gồm số âm)
    numbers = re.findall(r'-?\d+', input_string)
    
    positive_sum = 0
    negative_sum = 0
    found_numbers = []
    
    for num_str in numbers:
        num = int(num_str)
        found_numbers.append(num)
        
        if num >= 0:
            positive_sum += num
        else:
            negative_sum += num
    
    return found_numbers, positive_sum, negative_sum

# Nhập chuỗi từ người dùng
input_string = input("Nhập chuỗi: ")

print(f"Chuỗi ban đầu là \"{input_string}\"")

# Tìm và tính tổng các số
numbers, positive_sum, negative_sum = extract_and_sum_numbers(input_string)

print(f"Các số tìm được: {numbers}")
print(f"Kết quả: Giá trị dương: {positive_sum}. Giá trị âm: {negative_sum}.")