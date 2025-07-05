import sys 
from Newtworksecurity.logging.logger import logger
class NetworkSecuirtyException(Exception):
    def __init__(self, error_message,error_details:sys):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        self.line_no = exc_tb.tb_lineno
        
    def __str__(self):
        return "Error Occured in ({0}) at line number ({1}) ({2})".format(self.file_name,self.line_no,str(self.error_message))