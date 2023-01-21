from cryptography.fernet import Fernet

class Crypt():

    def generate_key():
        key = Fernet.generate_key()
        with open("encrypt.key", "wb") as key_file:
            key_file.write(key)

    def encrypt_string(data):
        f = Fernet(open("encrypt.key", "rb").read())
        encrypted_data = f.encrypt(bytes(data, 'utf-8'))
        encrypted_string = encrypted_data.decode("utf-8")

        return encrypted_string

    def decrypt_string(data):
        f = Fernet(open("encrypt.key", "rb").read())
        decrypted_data = f.decrypt(bytes(data, 'utf-8'))
        decrypted_string = decrypted_data.decode("utf-8")

        return decrypted_string