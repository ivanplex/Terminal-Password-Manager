import hashlib, uuid

class Auth:

	def hash_password(self, password):
	    # uuid is used to generate a random number
		salt = uuid.uuid4().hex
		return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
	def check_password(self, input):

		with open('__pwd__', 'r') as f:
			hashed_password = f.readline()

		password, salt = hashed_password.split(':')
		return password == hashlib.sha256(salt.encode() + input.encode()).hexdigest()