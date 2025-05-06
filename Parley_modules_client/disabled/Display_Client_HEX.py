# Module : Display Client HEX

from datetime import datetime
from log_utils import write_to_log

module_description = "print HEX data on the screen from the client in hex dump format"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):

    # Construct the output string
    output = []
    
    # Header
    output.append(f"[{source_ip}:{source_port}->{dest_ip}:{dest_port}] {datetime.now().isoformat()} ------- Client to Server ({message_num}) -------")
    
    # Convert bytes to HEX and ASCII
    for i in range(0, len(message_data), 16):
        hex_part = ' '.join(f'{byte:02x}' for byte in message_data[i:i+16])
        ascii_part = ''.join(chr(byte) if 32 <= byte <= 126 else '.' for byte in message_data[i:i+16])
        output.append(f"{hex_part:<48} | {ascii_part}")
    
    # Join all lines with newline characters
    full_output = '\n'.join(output)

    # Atomic writes to screen and log file
    print(full_output)
    write_to_log(source_ip, source_port, dest_ip, dest_port, full_output)

    return message_data
