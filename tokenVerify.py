import jwt
import base64

def verify(token):
    SECRET_KEY = 'django-insecure-8i5s2+*^w!+1u((4qpbbvnlnep)gldib!wt(dxbj&615ni_+ln'

    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])        
    except jwt.exceptions.ExpiredSignatureError:
        
        return False
    except Exception:
        print('알 수 없음')
        return False
    else: # 정상 실행시, 토큰 유효시
        return True