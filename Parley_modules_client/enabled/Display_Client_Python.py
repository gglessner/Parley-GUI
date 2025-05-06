# Module : Display Client Python

from datetime import datetime
from log_utils import write_to_log

module_description = "print Python binary data on the screen from the client"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):

    # Convert bytearray to bytes if necessary
    if isinstance(message_data, bytearray):
        message_data = bytes(message_data)

    # Construct the output string
    output = []
    
    #Header
    output.append(f"[{source_ip}:{source_port}->{dest_ip}:{dest_port}] {datetime.now().isoformat()} ------- Client to Server ({message_num}) -------")
    output.append(repr(message_data))  # Now this gives the 'b'...' format for bytes

    # Join all lines with newline characters
    full_output = '\n'.join(output)

    # Atomic writes to screen and log file
    print(full_output)
    write_to_log(source_ip, source_port, dest_ip, dest_port, full_output)

    return message_data
