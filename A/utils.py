from django.contrib.auth.mixins import UserPassesTestMixin
from kavenegar import *


def send_otp_code(phone_number, code):
	try:
		api = KavenegarAPI('2B37746D344D744E67676E734C4139576747554A67716E3869557465427735543076787963716A6F4C486F3D')
		params = {
			'sender': '',
			'receptor': phone_number,
			'message': f'{code} کد تایید شما '
		}
		response = api.sms_send(params)
		print(response)
	except APIException as e:
		print(e)
	except HTTPException as e:
		print(e)        
  
  
class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
	    return self.request.user.is_authenticated and self.request.user.is_admin