# Parley Module

The `Parley` module is a component of the **HACKtiveMQ Suite** and **ningu framework**, designed to act as a TCP/SSL proxy for intercepting and manipulating network traffic. It provides a graphical interface to configure proxy settings, load client and server certificates, and apply pluggable modules for processing network data.

## Overview

The `Parley` module enables users to:
- Set up a proxy server to relay traffic between a local endpoint (client-facing) and a remote endpoint (server-facing).
- Toggle TCP or SSL for both local and remote connections, with support for loading server and client certificates.
- Load and toggle pluggable client and server modules to process network traffic (e.g., display data in HEX, UTF-8, or modify HTTP headers).
- Log all proxy activity, including connection details and module outputs, to a status window and connection-specific log files in `modules/Parley_logs/<date>/`.
- Manage modules by enabling or disabling them via a GUI, moving module files between `enabled` and `disabled` directories.

The module dynamically loads Python modules from `modules/Parley_modules_client/enabled` and `modules/Parley_modules_server/enabled`, which are created automatically if they do not exist.

## Requirements

### Software
- **Python**: Version 3.8 or later recommended.
- **Operating System**: Compatible with Windows, Linux, and macOS.

### Python Dependencies
The following Python packages are required, as specified in `requirements.txt`:
PySide6>=6.0.0

## Installation

1. **Obtain the Module**:
   - The `Parley` module is part of the HACKtiveMQ Suite. Clone or download the suite repository, or extract the `3_Parley.py` file and its dependencies.

2. **Install Python Dependencies**:
   - Create a virtual environment (optional but recommended):
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Linux/macOS
     venv\Scripts\activate     # On Windows
     ```
   - Install the required packages:
     ```bash
     pip install -r requirements.txt
     ```
   - Alternatively, install directly:
     ```bash
     pip install PySide6>=6.0.0
     ```

3. **Set Up Module Directories**:
   - Ensure the following directories exist (created automatically if missing):
     - `modules/Parley_modules_client/enabled`: For enabled client modules.
     - `modules/Parley_modules_client/disabled`: For disabled client modules.
     - `modules/Parley_modules_server/enabled`: For enabled server modules.
     - `modules/Parley_modules_server/disabled`: For disabled server modules.
     - `modules/Parley_module_libs`: For shared library modules (e.g., `lib3270.py`, `lib8583.py`).
   - Place client and server module files (e.g., `Display_Client_HEX.py`, `Display_Server_Python.py`) in the appropriate `enabled` or `disabled` directories.
   - Place shared library modules in `modules/Parley_module_libs`.

4. **Prepare Certificates** (if using SSL):
   - Obtain server and client certificates (`.pem` or `.crt` files) if enabling SSL for local or remote connections.
   - Certificates can be loaded via the GUI during configuration.

## Usage

1. **Launch the Module**:
   - Run the `Parley` module via the HACKtiveMQ Suite or the ningu framework.

2. **Configure Proxy Settings**:
   - **Local IP/Port**: Enter the IP address (e.g., `127.0.0.1`) and port (e.g., `8080`) for the proxy to listen on.
   - **Remote IP/Port**: Enter the target server’s IP address and port (e.g., `80` for HTTP).
   - **Local TLS**: Toggle the `Local TLS` button to enable SSL (`SSL`) or use TCP (`TCP`) for client connections. Load a server certificate if using SSL.
   - **Remote TLS**: Toggle the `Remote TLS` button to enable SSL (`SSL`) or use TCP (`TCP`) for server connections. Load a client certificate if using SSL.
   - **Certificates**:
     - Click `Load Server Cert` to select a server certificate (`.pem` or `.crt`) for local SSL.
     - Click `Load Client Cert` to select a client certificate for remote SSL.
     - Click `Clear` to remove certificate paths.

3. **Manage Modules**:
   - **Client Modules**: View available client modules in the `Client Modules` list. Click a module to toggle it between `enabled` and `disabled`, moving its `.py` file between `modules/Parley_modules_client/enabled` and `modules/Parley_modules_client/disabled`.
   - **Server Modules**: View available server modules in the `Server Modules` list. Click a module to toggle its status, moving its `.py` file between `modules/Parley_modules_server/enabled` and `modules/Parley_modules_server/disabled`.
   - Enabled modules are bolded in the lists and loaded automatically when starting the proxy.

4. **Start/Stop Proxy**:
   - Click the `Start` button to launch the proxy, which listens on the specified local IP/port and forwards traffic to the remote IP/port.
   - The `Status` text box logs events (e.g., `Started proxy: 127.0.0.1:8080 -> example.com:80`, `New server socket thread started for 127.0.0.1:12345`).
   - Connection-specific logs are saved to `modules/Parley_logs/<date>/<src_ip>-<src_port>-<dst_ip>-<dst_port>.log`.
   - Click `Stop` to halt the proxy and clean up resources.

5. **Monitor and Debug**:
   - The `Status` text box displays real-time logs, including module loading, connection details, and errors.
   - Check log files in `modules/Parley_logs/<date>/` for detailed connection-specific logs.

## Directory Structure
```
HACKtiveMQ_Suite/
├── modules/
│   ├── Parley_module_libs/         # Shared library modules
│   │   ├── lib3270.py
│   │   ├── lib8583.py
│   │   ├── log_utils.py
│   │   ├── solace_auth.py
│   │   └── ...
│   ├── Parley_modules_client/      # Client modules
│   │   ├── enabled/
│   │   │   ├── Display_Client_Python.py
│   │   │   └── ...
│   │   ├── disabled/
│   │   │   ├── Display_Client_HEX.py
│   │   │   ├── Display_Client_UTF8.py
│   │   │   └── ...
│   ├── Parley_modules_server/      # Server modules
│   │   ├── enabled/
│   │   │   ├── Display_Server_Python.py
│   │   │   └── ...
│   │   ├── disabled/
│   │   │   ├── Display_Server_HEX.py
│   │   │   ├── Display_Server_UTF8.py
│   │   │   └── ...
│   ├── Parley_logs/                # Log files (created automatically)
│   │   ├── <MM-DD-YYYY>/
│   │   │   ├── <src_ip>-<src_port>-<dst_ip>-<dst_port>.log
│   │   │   └── ...
└── 3_Parley.py                    # Parley module
```

## Limitations
- **Module Compatibility**: Modules must have a `module_function` that processes data and a `module_description` attribute, as expected by the `Parley` module.
- **SSL Certificates**: SSL connections require valid certificates. Missing or invalid certificates may cause connection failures.
- **Port Conflicts**: Ensure the local port is not in use by another application to avoid binding errors.
- **Thread Safety**: Modules must be thread-safe, as they are called in separate client threads.

## Troubleshooting
- **Proxy Fails to Start**:
  - Verify that the local and remote IP/port inputs are valid (e.g., numeric port, non-empty remote IP).
  - Check for port conflicts (`Error starting proxy: Address already in use`).
  - Ensure certificates are valid if using SSL (`Error in connection: [SSL: CERTIFICATE_VERIFY_FAILED]`).
- **Modules Not Loaded**:
  - Confirm that module files are in `modules/Parley_modules_client/enabled` or `modules/Parley_modules_server/enabled`.
  - Check the `Status` text box for errors (e.g., `Error loading module: ...`).
- **No Logs in Files**:
  - Ensure the `modules/Parley_logs/<date>/` directory is writable.
  - Check for errors in the `Status` text box (e.g., `Error writing to log file ...`).
- **Connection Issues**:
  - Verify remote server availability (`Error: Connection refused`).
  - Check TLS settings and certificate paths for SSL connections.

## Contributing
Contributions to the `Parley` module are welcome! To contribute:
1. Fork the HACKtiveMQ Suite repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please test changes on your operating system (Windows, Linux, or macOS) and ensure compatibility with the module’s functionality and module interface.

## License
This module is licensed under the GNU General Public License v3.0. See the [LICENSE](https://www.gnu.org/licenses/) file for details.

## Contact
For issues, questions, or suggestions, contact Garland Glessner at gglesner@gmail.com.
