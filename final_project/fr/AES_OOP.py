from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class AES(object):
	def __init__(self, secret_key):
		self.aesgcm = AESGCM(secret_key)

	def encrypt(self, nonce, original_text, associated_data=None):
		data_in_bytes = original_text.encode('latin-1')
		cipher_text = self.aesgcm.encrypt(nonce, data_in_bytes, associated_data)
		return cipher_text.decode('latin-1'), cipher_text

	def decrypt(self, nonce, cipher_text, associated_data=None):
		data_in_bytes = cipher_text.encode('latin-1')
		decoded_text = self.aesgcm.decrypt(nonce, data_in_bytes, associated_data)
		return decoded_text.decode('latin-1'), decoded_text
