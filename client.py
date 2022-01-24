from session import CompanySession
from loguru import logger
import inspect, sys

class CompanyClient:
    
    send_command_endpoint = "https://api.companylistener.com/v1/devices/command/{imei}/send"
    headers = {"Content-Type": "application/json"}
    QMS_COMMAND = f"AT+GTDMS={env.get("PASSWORD"),2,env.get("PASSWORD"),1,env.get("IPADDR"),env.get("PORT"),,,360,7F9F,,0,,0,30,,FFFF$"
    
    def __init__(self, logging_enabled=True):
        self.session = CompanySession()
        self.logging_enabled = logging_enabled
        # get filename/module and calling func
        func_name = inspect.stack()[-1].function
        module_name = inspect.stack()[-1].filename
        # build filename for logger without needing partial()
        log_name = module_name + "_" + func_name + "_{time}.log"
        if logging_enabled:
            logger.add(log_name)
        else:
            logger.add(sys.stderr)
        self.log = logger
        self.log.debug(f"logger init, filename = {module_name}, function name = {func_name}")
        try:
            self.devkey = env.get("DEVKEY")
        except:
            self.devkey = "False"
        
    def send_command(self, command=QMS_COMMAND, endpoint=send_command_endpoint, custom_body=None, imei=None, attempts=3):
        # add argument above for imei as req arg, then retries and count as optional args
        self.log.debug(f"imei: {imei}")
        if not imei:
            if not custom_body:
                raise ValueError
        attempts = range(attempts)
        if not custom_body:
            body = {"command": command,
                    "development": self.devkey
                    }
        else:
            body = custom_body
        for _ in attempts:
            try:
                resp = self.session.session.post(url=endpoint.format(imei=imei),
                                         headers=self.session.headers,
                                         json=body)
            except TokenExpiredError:
                self.log.error(f"auth token expired")
                self.session.reauthenticate()
                self.log.debug(f"reauthenticated, continuing")
                continue
            # handle reauth for a 401
            if resp.status_code == 401 or resp.json()["statusCode"] == 401:
                self.log.error(f"auth token expired")
                self.session.reauthenticate()
                self.log.debug(f"reauthenticated, continuing")
                continue
            # log successes and failures via log method
            if resp.json()["statusCode"] == 200:
                self.log.success(f"attempt {_} success")
            else:
                self.log.error(f"attempt {_} failed with {resp.json()['statusCode']}")
        
    def sms_command(self, command=QMS_COMMAND, phone=None, imei=None, attempts=2):
        # add argument above for imei as req arg, then retries and count as optional args
        endpoint = "https://api.companylistener.com/v2/aws/sms/send"
        if type(phone) is str:
            phone = [ phone ]
        elif type(phone) is not list:
            raise ValueError
        
        # consider prepending +1 for us phones ??
        
        body = {"message": command,
                "phoneNumbers": phone,
                "source": 2,
                "development": self.devkey
                }
        
        self.log.debug(f"phone: {phone}")
        attempts = range(attempts)
        
        for _ in attempts:
            try:
                resp = self.session.session.post(url=endpoint,
                                         headers=self.session.headers,
                                         json=body)
            except TokenExpiredError:
                self.log.error(f"auth token expired")
                self.session.reauthenticate()
                self.log.debug(f"reauthenticated, continuing")
                continue
            # handle reauth for a 401
            if resp.status_code == 401 or resp.json()["statusCode"] == 401:
                self.log.error(f"auth token expired")
                self.session.reauthenticate()
                self.log.debug(f"reauthenticated, continuing")
                continue
            # log successes and failures via log method
            if resp.json()["statusCode"] == 200:
                self.log.success(f"attempt {_} success")
            else:
                self.log.error(f"attempt {_} failed with {resp.json()['statusCode']}")