import itertools

# Danh sách cần tìm hoán vị
numbers = [1, 2, 3]

print(f"Danh sách gốc: {numbers}")
print("Tất cả các hoán vị:")
print("-" * 20)

# Sử dụng itertools.permutations() để tạo hoán vị
permutations = list(itertools.permutations(numbers))

# In từng hoán vị
for i, perm in enumerate(permutations, 1):
    print(f"Hoán vị {i}: {list(perm)}")

print(f"\nTổng cộng có {len(permutations)} hoán vị")