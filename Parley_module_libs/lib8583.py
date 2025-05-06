# NOTE: Be sure to 'pip3 install iso8583' before using...

import iso8583
from iso8583.specs import default_ascii as spec

def decode_iso8583(raw_data):
    try:
        # Since decode() might return a tuple, we'll unpack it if it does
        decoded, _ = iso8583.decode(raw_data, spec=spec)  # Assuming the second item in the tuple isn't needed
    except iso8583.DecodeError as e:
        if "Extra data after last field" in str(e):
            print(f"Warning: Extra data detected - {e}")
            decoded, _ = iso8583.decode(raw_data, spec=spec)
        else:
            raise  # Re-raise any other DecodeError

    readable_output = {}
    readable_output['MTI'] = decoded['t']
    
    for field in decoded.keys():
        if field != 't':
            if decoded[field] is not None:
                readable_output[field] = decoded[field]

    return readable_output
