# Module : Display Server UTF8

from datetime import datetime
from log_utils import write_to_log

module_description = "print Python UTF-8 data on the screen from the server"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):

    # Construct the output string
    output = []
    
    # Header
    output.append(f"[{source_ip}:{source_port}->{dest_ip}:{dest_port}] {datetime.now().isoformat()} ------- Server to Client ({message_num}) -------")
    
    # Decode the bytes to UTF-8 string
    try:
        message_data_str = message_data.decode('utf-8')
        output.append(message_data_str)  # Directly append the decoded string
    except UnicodeDecodeError:
        output.append(f"b'{message_data.hex()}'")  # If not UTF-8, print in hex format

    # Join all lines with newline characters
    full_output = '\n'.join(output)

    # Atomic writes to screen and log file
    print(full_output)
    write_to_log(dest_ip, dest_port, source_ip, source_port, full_output)

    return message_data
