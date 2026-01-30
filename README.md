# Parley - TCP/TLS Application Proxy

**Version:** 1.2.0  
**Author:** Garland Glessner  
**License:** GNU General Public License v3.0  
**Part of:** HACKtiveMQ Suite

---

## Overview

**Parley** is a multithreaded TCP/TLS application proxy module for the Ningu framework. It allows you to intercept, inspect, decode, and modify network traffic between a client and server in real-time.

Designed for penetration testing and security research, Parley supports:
- Plain TCP and TLS connections (both client and server side)
- Modular traffic processing pipelines
- On-the-fly data modification
- Credential extraction from multiple protocols
- Connection logging with per-session log files

---

## Features

- **Bidirectional Proxy**: Intercept traffic in both directions (client-to-server and server-to-client)
- **TLS Support**: Optional SSL/TLS on local (client-facing) and remote (server-facing) connections
- **Certificate Loading**: Load custom certificates for client and server TLS
- **Skip TLS Verification**: Bypass certificate validation for self-signed or invalid certs
- **Modular Processing**: Enable/disable traffic processing modules by clicking in the UI
- **Per-Connection Logging**: Automatic logging to dated directories with connection-specific files
- **Multithreaded**: Each client connection handled in its own thread

---

## Directory Structure

```
modules/
    3_Parley.py                    # Main Parley module
    README.md                      # This file
    Parley_module_libs/            # Shared libraries for sub-modules
        lib3270.py                 # EBCDIC/3270 terminal support
        lib8583.py                 # ISO 8583 payment message parsing
        lib_fix.py                 # FIX financial protocol parsing
        lib_http_basic.py          # HTTP Basic Auth decoding
        lib_jwt.py                 # JWT token decoding
        lib_ldap_bind.py           # LDAP Simple Bind decoding
        lib_smtp_auth.py           # SMTP/IMAP AUTH decoding
        log_utils.py               # Logging utilities
        solace_auth.py             # Solace message broker auth decoding
    Parley_modules_client/         # Client-to-server traffic modules
        enabled/                   # Active modules
        disabled/                  # Inactive modules
    Parley_modules_server/         # Server-to-client traffic modules
        enabled/                   # Active modules
        disabled/                  # Inactive modules
    Parley_logs/                   # Connection logs (auto-created)
        MM-DD-YYYY/                # Date-based subdirectories
```

---

## Usage

1. Launch Ningu: `python ningu-v1.0.0.py`
2. Select the **Parley** tab
3. Configure connection settings:
   - **Local IP/Port**: Where Parley listens for client connections
   - **Remote IP/Port**: The target server to proxy to
   - **TCP/SSL buttons**: Toggle TLS for each side
   - **Verify/No Verify**: Toggle TLS certificate validation (when using SSL)
   - **Load Cert buttons**: Load certificates for TLS connections
4. Click modules in the lists to enable/disable them
5. Click **Start** to begin proxying

---

## Sub-Module Development

Each sub-module must define:

```python
module_description = "Brief description of what this module does"

def module_function(message_num, source_ip, source_port, dest_ip, dest_port, message_data):
    """
    Process a message passing through the proxy.
    
    Args:
        message_num: Sequential message number for this connection
        source_ip: Source IP address
        source_port: Source port number
        dest_ip: Destination IP address
        dest_port: Destination port number
        message_data: The raw message bytes (bytearray)
    
    Returns:
        The message data to forward (can be modified)
    """
    # Process/display/modify message_data
    return message_data
```

---

## Included Sub-Modules

### Display Modules (Read-Only Inspection)

| Module | Description |
|--------|-------------|
| `Display_Client_Python` / `Display_Server_Python` | Raw Python bytes representation |
| `Display_Client_HEX` / `Display_Server_HEX` | Hex dump with ASCII sidebar |
| `Display_Client_UTF8` / `Display_Server_UTF8` | UTF-8 string display |
| `Display_Client_EBCDIC` / `Display_Server_EBCDIC` | EBCDIC to ASCII (mainframe) |
| `Display_Client_ISO8583` / `Display_Server_ISO8583` | ISO 8583 payment messages |
| `Display_Client_FIX` / `Display_Server_FIX` | FIX financial protocol |
| `Display_Client_JWT` / `Display_Server_JWT` | JWT token decode with expiration |

### Credential Capture Modules

| Module | Protocol | What it Captures |
|--------|----------|------------------|
| `Creds_Client_HTTP_Basic` | HTTP | Basic Auth and Proxy-Auth headers |
| `Creds_Client_SMTP_Auth` | SMTP/IMAP | AUTH PLAIN and AUTH LOGIN |
| `Creds_Client_LDAP_Bind` | LDAP | Simple Bind DN and password |
| `Creds_Client_Solace_Auth` | Solace | Message broker credentials |

### Modification Modules

| Module | Description |
|--------|-------------|
| `0-Modify_Client_HTTP_Headers` | Example HTTP header rewriting |
| `0-Modify_URL` | Example URL modification |

---

## Libraries

| Library | Description |
|---------|-------------|
| `lib3270.py` | EBCDIC to ASCII conversion table for IBM 3270 terminals |
| `lib8583.py` | ISO 8583 payment message parser |
| `lib_fix.py` | FIX protocol decoder with 600+ tag definitions |
| `lib_http_basic.py` | HTTP Basic/Proxy Authorization decoder |
| `lib_jwt.py` | JWT token parser with claim descriptions and expiry check |
| `lib_ldap_bind.py` | LDAP ASN.1/BER parser for Simple Bind requests |
| `lib_smtp_auth.py` | SMTP/IMAP AUTH PLAIN and LOGIN decoder |
| `log_utils.py` | Connection-specific logging utilities |
| `solace_auth.py` | Solace SMF authentication decoder |

---

## Changelog

### v1.2.0
- Added TLS certificate verification toggle ("Verify" / "No Verify" button)
- Added FIX protocol decoder (Display_Client_FIX, Display_Server_FIX)
- Added JWT token decoder (Display_Client_JWT, Display_Server_JWT)
- Added credential capture modules:
  - HTTP Basic Auth (Creds_Client_HTTP_Basic)
  - SMTP/IMAP AUTH (Creds_Client_SMTP_Auth)
  - LDAP Simple Bind (Creds_Client_LDAP_Bind)
- Renamed Solace_Auth_Decode to Creds_Client_Solace_Auth
- Code cleanup and dead code removal

### v1.1.2
- Initial public release
- Bidirectional TCP/TLS proxy
- Modular client and server traffic processing
- Per-connection logging

---

## Contact

Garland Glessner  
Email: gglessner@gmail.com
