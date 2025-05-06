# Module : Solace Auth Decode

from datetime import datetime
from solace_auth import decode_base64_credentials
from log_utils import write_to_log

module_description = "Automatically Base64 Decode Solace Authentication Credentials"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):

    if(message_num != 1):
        return message_data

    # Construct the output string
    output = []
    
    # Header
    output.append(f"[{source_ip}:{source_port}->{dest_ip}:{dest_port}] {datetime.now().isoformat()} ------- Client to Server ({message_num}) Solace Auth Decode -------")

    # Decode Base64 Authentication Credentials
    decoded_creds = decode_base64_credentials(message_data)
    output.append(decoded_creds)

    # Join all lines with newline characters
    full_output = '\n'.join(output)

    # Atomic writes to screen and log file
    print(full_output)
    write_to_log(source_ip, source_port, dest_ip, dest_port, full_output)

    return message_data
