from PIL import Image

def encode_message(image_path, message, output_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    if len(binary_message) > len(pixels):
        raise ValueError("Message is too long for the given image")

    encoded_pixels = []
    for i in range(len(binary_message)):
        pixel = list(pixels[i])
        pixel[-1] = int(binary_message[i])
        encoded_pixels.append(tuple(pixel))

    for j in range(len(binary_message), len(pixels)):
        encoded_pixels.append(pixels[j])

    encoded_image = Image.new('RGB', img.size)
    encoded_image.putdata(encoded_pixels)
    encoded_image.save(output_path)
    print("Message encoded successfully!")

def decode_message(encoded_image_path):
    encoded_image = Image.open(encoded_image_path)
    pixels = list(encoded_image.getdata())

    binary_message = ''
    for pixel in pixels:
        binary_message += str(pixel[-1])

    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        try:
            char = chr(int(byte, 2))
            message += char
            if char == '\0':  # Check for null terminator indicating the end of the message
                break
        except ValueError:  # Catch any decoding errors
            break

    return message.rstrip('\x00')  # Remove any null characters at the end

# Example Usage
image_path = "/stegono/image.png"
message_to_encode = "Hello, this is a secret message!"
output_path = "/stegono/encoded_image.png"

# Encode
encode_message(image_path, message_to_encode, output_path)

# Decode
decoded_message = decode_message(output_path)
print("Decoded Message:", decoded_message)
