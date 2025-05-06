# Module : Display Client ISO8583

from datetime import datetime
from log_utils import write_to_log
from lib8583 import decode_iso8583

module_description = "print ISO8583 data on the screen from the client"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):

    # Construct the output string
    output = []
    
    # Header
    output.append(f"[{source_ip}:{source_port}->{dest_ip}:{dest_port}] {datetime.now().isoformat()} ------- Client to Server ({message_num}) -------")

    # Convert ISO8583 to ASCII
    iso8583_data = decode_iso8583(message_data)
    output.append(iso8583_data)

    # Join all lines with newline characters
    full_output = '\n'.join(output)

    # Atomic writes to screen and log file
    print(full_output)
    write_to_log(source_ip, source_port, dest_ip, dest_port, full_output)

    return message_data
