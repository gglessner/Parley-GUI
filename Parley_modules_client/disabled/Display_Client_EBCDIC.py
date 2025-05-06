# Module : Display Client EBCDIC

from datetime import datetime
from log_utils import write_to_log
from lib3270 import ebcdic_to_ascii

module_description = "print EBCDIC data on the screen from the client"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):

    # Construct the output string
    output = []
    
    # Header
    output.append(f"[{source_ip}:{source_port}->{dest_ip}:{dest_port}] {datetime.now().isoformat()} ------- Client to Server ({message_num}) -------")

    # Convert EBCDIC to ASCII
    ebcdic_data = ebcdic_to_ascii(message_data)
    output.append(ebcdic_data)

    # Join all lines with newline characters
    full_output = '\n'.join(output)

    # Atomic writes to screen and log file
    print(full_output)
    write_to_log(source_ip, source_port, dest_ip, dest_port, full_output)

    return message_data
