# Module : LDAP Simple Bind Credential Capture

from datetime import datetime
from log_utils import write_to_log
from lib_ldap_bind import format_ldap_bind

module_description = "capture and decode LDAP Simple Bind credentials from client"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):

    # Try to find and decode LDAP Simple Bind
    bind_output = format_ldap_bind(message_data)
    
    # Only output if we found credentials
    if bind_output:
        # Construct the output string
        output = []
        
        # Header
        output.append(f"[{source_ip}:{source_port}->{dest_ip}:{dest_port}] {datetime.now().isoformat()} ------- Client to Server ({message_num}) CREDS CAPTURED -------")
        output.append(bind_output)

        # Join all lines with newline characters
        full_output = '\n'.join(output)

        # Atomic writes to screen and log file
        print(full_output)
        write_to_log(source_ip, source_port, dest_ip, dest_port, full_output)

    return message_data
