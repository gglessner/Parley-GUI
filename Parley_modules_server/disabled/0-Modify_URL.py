# Module : Modify URL Example

# This is an example of modifying server application data on-the-fly

from datetime import datetime
from log_utils import write_to_log

module_description = "Modify some text"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):

    # Construct the output string
    output = []
    
    # Header
    output.append(f"[{source_ip}:{source_port}->{dest_ip}:{dest_port}] {datetime.now().isoformat()} ------- Server to Client ({message_num}) Modify URL -------")

    # Modify Text
    message_data = message_data.replace(b'https://www.cnn.com/', b'http://127.0.0.1/')

    # Join all lines with newline characters
    full_output = '\n'.join(output)

    # Atomic writes to screen and log file
    print(full_output)
    write_to_log(dest_ip, dest_port, source_ip, source_port, full_output)

    return message_data
