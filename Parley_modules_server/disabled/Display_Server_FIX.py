# Module : Display Server FIX

from datetime import datetime
from log_utils import write_to_log
from lib_fix import format_fix_message

module_description = "decode and display FIX protocol messages from the server"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):

    # Construct the output string
    output = []
    
    # Header
    output.append(f"[{source_ip}:{source_port}->{dest_ip}:{dest_port}] {datetime.now().isoformat()} ------- Server to Client ({message_num}) -------")

    # Decode FIX message
    try:
        fix_output = format_fix_message(message_data)
        output.append(fix_output)
    except Exception as e:
        output.append(f"FIX decode error: {e}")
        output.append(repr(message_data))

    # Join all lines with newline characters
    full_output = '\n'.join(output)

    # Atomic writes to screen and log file
    print(full_output)
    write_to_log(dest_ip, dest_port, source_ip, source_port, full_output)

    return message_data
