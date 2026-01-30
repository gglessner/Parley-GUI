# Module : Display Client JWT

from datetime import datetime
from log_utils import write_to_log
from lib_jwt import find_and_format_jwts

module_description = "extract and decode JWT Bearer tokens from client requests"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):

    # Try to find and decode JWT tokens
    jwt_output = find_and_format_jwts(message_data)
    
    # Only output if we found tokens
    if jwt_output:
        # Construct the output string
        output = []
        
        # Header
        output.append(f"[{source_ip}:{source_port}->{dest_ip}:{dest_port}] {datetime.now().isoformat()} ------- Client to Server ({message_num}) JWT Found -------")
        output.append(jwt_output)

        # Join all lines with newline characters
        full_output = '\n'.join(output)

        # Atomic writes to screen and log file
        print(full_output)
        write_to_log(source_ip, source_port, dest_ip, dest_port, full_output)

    return message_data
