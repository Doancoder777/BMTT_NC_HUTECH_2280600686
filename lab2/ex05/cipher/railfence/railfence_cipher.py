class RailFenceCipher:
    def __init__(self):
        pass
    
    def rail_fence_encrypt(self, plain_text, num_rails):
        if num_rails <= 1:
            return plain_text
            
        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1  # 1: down, -1: up
        
        for char in plain_text:
            rails[rail_index].append(char)
            
            # Update direction BEFORE changing rail_index
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


# Test function để verify
def test_railfence_fixed():
    cipher = RailFenceCipher()
    
    # Test case 1: Input của bạn
    text1 = "232wsada"
    key1 = 3
    encrypted1 = cipher.rail_fence_encrypt(text1, key1)
    decrypted1 = cipher.rail_fence_decrypt(encrypted1, key1)
    
    print(f"Test 1:")
    print(f"Original:  '{text1}'")
    print(f"Encrypted: '{encrypted1}'")
    print(f"Decrypted: '{decrypted1}'")
    print(f"Match: {text1 == decrypted1}")
    print()
    
    # Test case 2: Simple example
    text2 = "HELLO"
    key2 = 3
    encrypted2 = cipher.rail_fence_encrypt(text2, key2)
    decrypted2 = cipher.rail_fence_decrypt(encrypted2, key2)
    
    print(f"Test 2:")
    print(f"Original:  '{text2}'")
    print(f"Encrypted: '{encrypted2}'")
    print(f"Decrypted: '{decrypted2}'")
    print(f"Match: {text2 == decrypted2}")
    print()
    
    # Test case 3: Longer text
    text3 = "HELLO WORLD"
    key3 = 3
    encrypted3 = cipher.rail_fence_encrypt(text3, key3)
    decrypted3 = cipher.rail_fence_decrypt(encrypted3, key3)
    
    print(f"Test 3:")
    print(f"Original:  '{text3}'")
    print(f"Encrypted: '{encrypted3}'")
    print(f"Decrypted: '{decrypted3}'")
    print(f"Match: {text3 == decrypted3}")
    
    # Visualize rails for first test
    print(f"\nVisualization for '{text1}' with {key1} rails:")
    visualize_rails(text1, key1)


def visualize_rails(text, num_rails):
    """Helper function to visualize rail pattern"""
    rails = [[] for _ in range(num_rails)]
    rail_index = 0
    direction = 1
    
    for i, char in enumerate(text):
        rails[rail_index].append(f"{char}({i})")
        
        if rail_index == 0:
            direction = 1
        elif rail_index == num_rails - 1:
            direction = -1
            
        rail_index += direction
    
    for i, rail in enumerate(rails):
        print(f"Rail {i}: {rail} -> '{''.join([c.split('(')[0] for c in rail])}'")


# Uncomment để test
# test_railfence_fixed()