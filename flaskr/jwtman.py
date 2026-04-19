import os
import jwt
import dotenv
import datetime
from datetime import timezone
dotenv.load_dotenv()
JWT_SECRET = os.environ['JWT_SECRET']

def jwt_tok_generate (user_id, valid_for_days=3):
	now = datetime.datetime.now(tz=timezone.utc)
	generated_jwt = jwt.encode({
		'iat': now,
		'exp': now + datetime.timedelta(valid_for_days),
		'sub': user_id,
	}, JWT_SECRET, algorithm='HS256')
	return generated_jwt

def jwt_tok_validate (jwt_tok, user_id=None):
	decoded = None
	
	try:
		decoded = jwt.decode(jwt_tok, JWT_SECRET, algorithms='HS256')
	except jwt.InvalidIssuedAtError:
		return False if user_id else None
	except jwt.ExpiredSignatureError:
		return False if user_id else None
	except jwt.DecodeError:
		return False if user_id else None
	
	if user_id == None:
		return decoded['sub']
	else:
		return decoded['sub'] == user_id
