# Module : Modify Client HTTP Headers

# This is an example of modifying client application data on-the-fly

from datetime import datetime
from log_utils import write_to_log

module_description = "Modify Client HTTP Headers"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):

    # Construct the output string
    output = []
    
    # Header
    output.append(f"[{source_ip}:{source_port}->{dest_ip}:{dest_port}] {datetime.now().isoformat()} ------- Client to Server ({message_num}) Modify HTTP Headers -------")

    # Modify HTTP Headers
    message_data = message_data.replace(b'Host: 127.0.0.1', b'Host: www.cnn.com')
    message_data = message_data.replace(b'If-Modified-Since:', b'Invalid:')
    message_data = message_data.replace(b'Accept-Encoding:', b'Invalid:')

    # Join all lines with newline characters
    full_output = '\n'.join(output)

    # Atomic writes to screen and log file
    print(full_output)
    write_to_log(source_ip, source_port, dest_ip, dest_port, full_output)

    return message_data
