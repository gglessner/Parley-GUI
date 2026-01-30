# Module : SMTP/IMAP Auth Credential Capture

from datetime import datetime
from log_utils import write_to_log
from lib_smtp_auth import format_smtp_auth

module_description = "capture and decode SMTP/IMAP AUTH credentials from client"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):

    # Try to find and decode SMTP/IMAP auth
    auth_output = format_smtp_auth(message_data)
    
    # Only output if we found credentials
    if auth_output:
        # Construct the output string
        output = []
        
        # Header
        output.append(f"[{source_ip}:{source_port}->{dest_ip}:{dest_port}] {datetime.now().isoformat()} ------- Client to Server ({message_num}) CREDS CAPTURED -------")
        output.append(auth_output)

        # Join all lines with newline characters
        full_output = '\n'.join(output)

        # Atomic writes to screen and log file
        print(full_output)
        write_to_log(source_ip, source_port, dest_ip, dest_port, full_output)

    return message_data
