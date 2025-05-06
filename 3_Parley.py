# Parley - part of the HACKtiveMQ Suite
# Copyright (C) 2025 Garland Glessner - gglesner@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PySide6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QFileDialog, QSpacerItem, QSizePolicy, QListWidget, QListWidgetItem
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtCore import Qt
import importlib.util
import os
import shutil
import socket
import ssl
import sys
import threading
import select
import io
from contextlib import redirect_stdout
import datetime

# Define the version number at the top
VERSION = "1.1.1"

# Define the tab label for the tab widget
TAB_LABEL = f"Parley v{VERSION}"

class PrintRedirector(io.StringIO):
    """Redirect print statements to the StatusTextBox and connection-specific log files."""
    def __init__(self, status_textbox, root_log_dir):
        super().__init__()
        self.status_textbox = status_textbox
        self.root_log_dir = root_log_dir
        self.log_files = {}  # Dictionary to store open log files for connections

    def write(self, text, connection_info=None):
        """Write text to StatusTextBox and connection-specific log file if connection_info is provided."""
        # Append to StatusTextBox
        self.status_textbox.appendPlainText(text.rstrip())

        # Write to connection-specific log file if connection_info is provided
        if connection_info:
            src_ip, src_port, dst_ip, dst_port = connection_info
            # Create date-based subdirectory (e.g., modules/Parley_logs/05-01-2025)
            today = datetime.date.today()
            log_dir = os.path.join(self.root_log_dir, today.strftime('%m-%d-%Y'))
            os.makedirs(log_dir, exist_ok=True)

            # Create log file name (e.g., 127.0.0.1-8080-example.com-80.log)
            log_filename = f"{src_ip}-{src_port}-{dst_ip}-{dst_port}.log"
            log_file_path = os.path.join(log_dir, log_filename)

            try:
                # Open the log file if not already open
                if log_file_path not in self.log_files:
                    self.log_files[log_file_path] = open(log_file_path, 'a', encoding='utf-8')
                # Write to the log file
                self.log_files[log_file_path].write(text + '\n')  # Add newline for consistency with logging utility
                self.log_files[log_file_path].flush()
            except Exception as e:
                self.status_textbox.appendPlainText(f"Error writing to log file {log_file_path}: {e}")

    def write_general(self, text):
        """Write general (non-connection-specific) text to StatusTextBox only."""
        self.status_textbox.appendPlainText(text.rstrip())

    def flush(self):
        """Flush all open log files."""
        for log_file in self.log_files.values():
            log_file.flush()

    def close(self):
        """Close all open log files."""
        for log_file in self.log_files.values():
            log_file.close()
        self.log_files.clear()

class Ui_TabContent:
    def setupUi(self, widget):
        """Set up the UI components for the Parley proxy tab."""
        widget.setObjectName("TabContent")

        # Main vertical layout with reduced spacing
        self.verticalLayout_3 = QVBoxLayout(widget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setSpacing(5)

        self.verticalLayout_3.addSpacerItem(QSpacerItem(0, 1, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Header frame with title and input fields
        self.frame_8 = QFrame(widget)
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.frame_5 = QFrame(self.frame_8)
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.horizontalLayout_3.addWidget(self.frame_5)

        self.label_3 = QLabel(self.frame_8)
        font = QFont("Courier New", 14)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.horizontalLayout_3.addWidget(self.label_3)

        # Add spacer to push input fields to the right
        self.horizontalSpacer_inputs = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_inputs)

        self.frame_10 = QFrame(self.frame_8)
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.gridLayout_2 = QGridLayout(self.frame_10)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setVerticalSpacing(0)

        # Local connection input frame
        self.frame_11 = QFrame(self.frame_10)
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)

        self.label_local_ip = QLabel(self.frame_11)
        self.label_local_ip.setText("Local IP:  ")
        self.horizontalLayout_5.addWidget(self.label_local_ip)

        self.LocalIPLine = QLineEdit(self.frame_11)
        self.LocalIPLine.setText("127.0.0.1")
        self.horizontalLayout_5.addWidget(self.LocalIPLine)

        # Add larger gap between Local IP text entry and Local Port label
        self.spacer_local_gap = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(self.spacer_local_gap)

        self.label_local_port = QLabel(self.frame_11)
        self.label_local_port.setText("Local Port:  ")
        self.horizontalLayout_5.addWidget(self.label_local_port)

        self.LocalPortLine = QLineEdit(self.frame_11)
        self.LocalPortLine.setText("8080")
        self.horizontalLayout_5.addWidget(self.LocalPortLine)

        self.LocalTLSButton = QPushButton(self.frame_11)
        self.LocalTLSButton.setText("TCP")
        self.LocalTLSButton.setCheckable(True)
        self.horizontalLayout_5.addWidget(self.LocalTLSButton)

        self.gridLayout_2.addWidget(self.frame_11, 0, 0, 1, 1)

        # Server certificate input frame
        self.frame_server_cert = QFrame(self.frame_10)
        self.frame_server_cert.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_server_cert = QHBoxLayout(self.frame_server_cert)
        self.horizontalLayout_server_cert.setContentsMargins(0, 0, 0, 0)

        self.ServerCertButton = QPushButton(self.frame_server_cert)
        self.ServerCertButton.setText("Load Server Cert")
        self.horizontalLayout_server_cert.addWidget(self.ServerCertButton)

        self.ServerCertPath = QLineEdit(self.frame_server_cert)
        self.ServerCertPath.setReadOnly(True)
        self.horizontalLayout_server_cert.addWidget(self.ServerCertPath)

        self.ServerCertClearButton = QPushButton(self.frame_server_cert)
        self.ServerCertClearButton.setText("Clear")
        self.horizontalLayout_server_cert.addWidget(self.ServerCertClearButton)

        self.gridLayout_2.addWidget(self.frame_server_cert, 1, 0, 1, 1)

        # Remote connection input frame
        self.frame_12 = QFrame(self.frame_10)
        self.frame_12.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)

        self.label_remote_ip = QLabel(self.frame_12)
        self.label_remote_ip.setText("Remote IP:  ")
        self.horizontalLayout_6.addWidget(self.label_remote_ip)

        self.RemoteIPLine = QLineEdit(self.frame_12)
        self.horizontalLayout_6.addWidget(self.RemoteIPLine)

        # Add larger gap between Remote IP text entry and Remote Port label
        self.spacer_remote_gap = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(self.spacer_remote_gap)

        self.label_remote_port = QLabel(self.frame_12)
        self.label_remote_port.setText("Remote Port:  ")
        self.horizontalLayout_6.addWidget(self.label_remote_port)

        self.RemotePortLine = QLineEdit(self.frame_12)
        self.RemotePortLine.setText("80")
        self.horizontalLayout_6.addWidget(self.RemotePortLine)

        self.RemoteTLSButton = QPushButton(self.frame_12)
        self.RemoteTLSButton.setText("TCP")
        self.RemoteTLSButton.setCheckable(True)
        self.horizontalLayout_6.addWidget(self.RemoteTLSButton)

        self.gridLayout_2.addWidget(self.frame_12, 2, 0, 1, 1)

        # Client certificate input frame
        self.frame_client_cert = QFrame(self.frame_10)
        self.frame_client_cert.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_client_cert = QHBoxLayout(self.frame_client_cert)
        self.horizontalLayout_client_cert.setContentsMargins(0, 0, 0, 0)

        self.ClientCertButton = QPushButton(self.frame_client_cert)
        self.ClientCertButton.setText("Load Client Cert")
        self.horizontalLayout_client_cert.addWidget(self.ClientCertButton)

        self.ClientCertPath = QLineEdit(self.frame_client_cert)
        self.ClientCertPath.setReadOnly(True)
        self.horizontalLayout_client_cert.addWidget(self.ClientCertPath)

        self.ClientCertClearButton = QPushButton(self.frame_client_cert)
        self.ClientCertClearButton.setText("Clear")
        self.horizontalLayout_client_cert.addWidget(self.ClientCertClearButton)

        self.gridLayout_2.addWidget(self.frame_client_cert, 3, 0, 1, 1)

        # Start/Stop button frame
        self.frame_start_stop = QFrame(self.frame_10)
        self.frame_start_stop.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_start_stop = QHBoxLayout(self.frame_start_stop)
        self.horizontalLayout_start_stop.setContentsMargins(0, 0, 0, 0)

        self.StartStopButton = QPushButton(self.frame_start_stop)
        self.StartStopButton.setText("Start")
        font1 = QFont()
        font1.setBold(True)
        self.StartStopButton.setFont(font1)
        self.horizontalLayout_start_stop.addWidget(self.StartStopButton)

        self.horizontalSpacer_start_stop = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_start_stop.addItem(self.horizontalSpacer_start_stop)

        self.gridLayout_2.addWidget(self.frame_start_stop, 4, 0, 1, 1)

        self.horizontalLayout_3.addWidget(self.frame_10)
        self.verticalLayout_3.addWidget(self.frame_8)

        self.verticalLayout_3.addSpacerItem(QSpacerItem(0, 1, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Main content frame for module lists
        self.frame_3 = QFrame(widget)
        self.gridLayout = QGridLayout(self.frame_3)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        # Client modules list
        self.frame_client = QFrame(self.frame_3)
        self.frame_client.setFrameShape(QFrame.Box)
        self.frame_client.setStyleSheet("QFrame { border: 2px solid black; }")
        self.verticalLayout_client = QVBoxLayout(self.frame_client)
        self.verticalLayout_client.setContentsMargins(5, 5, 5, 5)

        self.label_client = QLabel(self.frame_client)
        self.label_client.setText("Client Modules:")
        self.verticalLayout_client.addWidget(self.label_client)

        self.ClientModulesList = QListWidget(self.frame_client)
        self.verticalLayout_client.addWidget(self.ClientModulesList)

        self.gridLayout.addWidget(self.frame_client, 0, 0, 1, 1)

        # Server modules list
        self.frame_server = QFrame(self.frame_3)
        self.frame_server.setFrameShape(QFrame.Box)
        self.frame_server.setStyleSheet("QFrame { border: 2px solid black; }")
        self.verticalLayout_server = QVBoxLayout(self.frame_server)
        self.verticalLayout_server.setContentsMargins(5, 5, 5, 5)

        self.label_server = QLabel(self.frame_server)
        self.label_server.setText("Server Modules:")
        self.verticalLayout_server.addWidget(self.label_server)

        self.ServerModulesList = QListWidget(self.frame_server)
        self.verticalLayout_server.addWidget(self.ServerModulesList)

        self.gridLayout.addWidget(self.frame_server, 0, 1, 1, 1)

        # Adjust column widths to split screen evenly
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)

        self.verticalLayout_3.addWidget(self.frame_3)

        # Status frame at the bottom
        self.frame_4 = QFrame(widget)
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.verticalLayout = QVBoxLayout(self.frame_4)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.StatusTextBox = QPlainTextEdit(self.frame_4)
        self.StatusTextBox.setReadOnly(True)
        # Set fixed-width font for StatusTextBox
        status_font = QFont("Courier New", 10)
        status_font.setFixedPitch(True)
        self.StatusTextBox.setFont(status_font)
        self.verticalLayout.addWidget(self.StatusTextBox)

        self.verticalLayout_3.addWidget(self.frame_4)

        # Adjust spacing
        self.gridLayout.setVerticalSpacing(0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_server_cert.setSpacing(0)
        self.horizontalLayout_client_cert.setSpacing(0)
        self.horizontalLayout_start_stop.setSpacing(0)

        self.retranslateUi(widget)

    def retranslateUi(self, widget):
        self.label_3.setText(f"""
 ___    __    ___   _     ____  _    
| |_)  / /\\  | |_) | |   | |_  \\ \\_/ 
|_|   /_/--\\ |_| \\ |_|__ |_|__  |_|  

 Version: {VERSION}""")
        self.label_local_ip.setText("Local IP:  ")
        self.label_local_port.setText("Local Port:  ")
        self.label_remote_ip.setText("Remote IP:  ")
        self.label_remote_port.setText("Remote Port:  ")
        self.ServerCertButton.setText("Load Server Cert")
        self.ClientCertButton.setText("Load Client Cert")
        self.StartStopButton.setText("Start")
        self.ServerCertClearButton.setText("Clear")
        self.ClientCertClearButton.setText("Clear")

class TabContent(QWidget):
    def __init__(self):
        """Initialize the TabContent widget with custom adjustments."""
        super().__init__()
        self.ui = Ui_TabContent()
        self.ui.setupUi(self)

        # Proxy state
        self.proxy_thread = None
        self.proxy_running = False
        self.server_socket = None
        self.client_threads = []
        self.client_sockets = []
        self.loaded_modules_client = {}
        self.loaded_modules_server = {}

        # Add module_libs to sys.path
        module_libs_path = os.path.join('modules', 'Parley_module_libs')
        if module_libs_path not in sys.path:
            sys.path.insert(0, module_libs_path)

        # Initialize logging
        log_dir = os.path.join('modules', 'Parley_logs')
        # --- START MODIFIED SECTION ---
        # Create the Parley_logs directory if it doesn't exist
        try:
            os.makedirs(log_dir, exist_ok=True)
            self.ui.StatusTextBox.appendPlainText(f"Ensured directory exists: {log_dir}")
        except Exception as e:
            self.ui.StatusTextBox.appendPlainText(f"Error creating directory {log_dir}: {e}")
        # --- END MODIFIED SECTION ---
        self.print_redirector = PrintRedirector(self.ui.StatusTextBox, log_dir)
        sys.stdout = self.print_redirector

        # Log initialization
        self.print_redirector.write_general(f"Parley v{VERSION} initialized.")

        # Set input field widths
        font_metrics = QFontMetrics(self.ui.LocalIPLine.font())
        char_width = font_metrics.averageCharWidth()
        width_32_chars = char_width * 32
        self.ui.LocalIPLine.setFixedWidth(width_32_chars // 2)
        self.ui.LocalPortLine.setFixedWidth(width_32_chars // 4)
        self.ui.RemoteIPLine.setFixedWidth(width_32_chars // 2)
        self.ui.RemotePortLine.setFixedWidth(width_32_chars // 4)
        self.ui.ServerCertPath.setFixedWidth(width_32_chars)
        self.ui.ClientCertPath.setFixedWidth(width_32_chars)

        # UI adjustments
        spacer_local = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.ui.horizontalLayout_5.addItem(spacer_local)
        spacer_remote = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.ui.horizontalLayout_6.addItem(spacer_remote)
        spacer_server_cert = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.ui.horizontalLayout_server_cert.addItem(spacer_server_cert)
        spacer_client_cert = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.ui.horizontalLayout_client_cert.addItem(spacer_client_cert)

        self.ui.LocalTLSButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ui.RemoteTLSButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ui.ServerCertButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ui.ClientCertButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ui.ServerCertClearButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ui.ClientCertClearButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ui.StartStopButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Initially disable server cert fields if LocalTLSButton is TCP
        self.ui.ServerCertButton.setEnabled(self.ui.LocalTLSButton.isChecked())
        self.ui.ServerCertPath.setEnabled(self.ui.LocalTLSButton.isChecked())
        self.ui.ServerCertClearButton.setEnabled(self.ui.LocalTLSButton.isChecked())

        # Initially disable client cert fields if RemoteTLSButton is TCP
        self.ui.ClientCertButton.setEnabled(self.ui.RemoteTLSButton.isChecked())
        self.ui.ClientCertPath.setEnabled(self.ui.RemoteTLSButton.isChecked())
        self.ui.ClientCertClearButton.setEnabled(self.ui.RemoteTLSButton.isChecked())

        # Connect signals
        self.ui.LocalTLSButton.clicked.connect(self.toggle_local_tls)
        self.ui.RemoteTLSButton.clicked.connect(self.toggle_remote_tls)
        self.ui.ServerCertButton.clicked.connect(self.load_server_cert)
        self.ui.ClientCertButton.clicked.connect(self.load_client_cert)
        self.ui.ServerCertClearButton.clicked.connect(self.clear_server_cert)
        self.ui.ClientCertClearButton.clicked.connect(self.clear_client_cert)
        self.ui.ClientModulesList.itemClicked.connect(self.toggle_client_module)
        self.ui.ServerModulesList.itemClicked.connect(self.toggle_server_module)
        self.ui.StartStopButton.clicked.connect(self.toggle_proxy)

        # Initialize module lists
        self.update_module_lists()

    def toggle_local_tls(self):
        """Toggle Local TLS button between TCP and SSL and update server cert fields."""
        self.ui.LocalTLSButton.setText("SSL" if self.ui.LocalTLSButton.isChecked() else "TCP")
        # Enable/disable server cert fields based on TLS state
        is_ssl = self.ui.LocalTLSButton.isChecked()
        self.ui.ServerCertButton.setEnabled(is_ssl)
        self.ui.ServerCertPath.setEnabled(is_ssl)
        self.ui.ServerCertClearButton.setEnabled(is_ssl)
        self.print_redirector.write_general(f"Local connection set to {'SSL' if is_ssl else 'TCP'}")

    def toggle_remote_tls(self):
        """Toggle Remote TLS button between TCP and SSL and update client cert fields."""
        self.ui.RemoteTLSButton.setText("SSL" if self.ui.RemoteTLSButton.isChecked() else "TCP")
        # Enable/disable client cert fields based on TLS state
        is_ssl = self.ui.RemoteTLSButton.isChecked()
        self.ui.ClientCertButton.setEnabled(is_ssl)
        self.ui.ClientCertPath.setEnabled(is_ssl)
        self.ui.ClientCertClearButton.setEnabled(is_ssl)
        self.print_redirector.write_general(f"Remote connection set to {'SSL' if is_ssl else 'TCP'}")

    def load_server_cert(self):
        """Load server certificate and display path."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Server Certificate", "", "Certificate Files (*.pem *.crt);;All Files (*)")
        if file_name:
            self.ui.ServerCertPath.setText(file_name)
            self.print_redirector.write_general(f"Server certificate loaded: {file_name}")

    def clear_server_cert(self):
        """Clear the server certificate path text box."""
        self.ui.ServerCertPath.clear()
        self.print_redirector.write_general("Server certificate path cleared")

    def load_client_cert(self):
        """Load client certificate and display path."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Client Certificate", "", "Certificate Files (*.pem *.crt);;All Files (*)")
        if file_name:
            self.ui.ClientCertPath.setText(file_name)
            self.print_redirector.write_general(f"Client certificate loaded: {file_name}")

    def clear_client_cert(self):
        """Clear the client certificate path text box."""
        self.ui.ClientCertPath.clear()
        self.print_redirector.write_general("Client certificate path cleared")

    def update_module_lists(self):
        """Update the client and server module lists with enabled/disabled status, bolding enabled modules."""
        self.ui.ClientModulesList.clear()
        self.ui.ServerModulesList.clear()

        # Client modules
        client_enabled_dir = os.path.join("modules", "Parley_modules_client", "enabled")
        client_disabled_dir = os.path.join("modules", "Parley_modules_client", "disabled")
        client_modules = []
        for dir_path, status in [(client_enabled_dir, "enabled"), (client_disabled_dir, "disabled")]:
            if os.path.exists(dir_path):
                for filename in sorted(os.listdir(dir_path)):
                    if filename.endswith(".py") and filename != "__init__.py":
                        module_name = filename[:-3]
                        client_modules.append((module_name, status))
        for module_name, status in sorted(client_modules):
            item = QListWidgetItem(f"{module_name} ({status})")
            item.setData(Qt.UserRole, (module_name, status))
            if status == "enabled":
                font = QFont()
                font.setBold(True)
                item.setFont(font)
            self.ui.ClientModulesList.addItem(item)

        # Server modules
        server_enabled_dir = os.path.join("modules", "Parley_modules_server", "enabled")
        server_disabled_dir = os.path.join("modules", "Parley_modules_server", "disabled")
        server_modules = []
        for dir_path, status in [(server_enabled_dir, "enabled"), (server_disabled_dir, "disabled")]:
            if os.path.exists(dir_path):
                for filename in sorted(os.listdir(dir_path)):
                    if filename.endswith(".py") and filename != "__init__.py":
                        module_name = filename[:-3]
                        server_modules.append((module_name, status))
        for module_name, status in sorted(server_modules):
            item = QListWidgetItem(f"{module_name} ({status})")
            item.setData(Qt.UserRole, (module_name, status))
            if status == "enabled":
                font = QFont()
                font.setBold(True)
                item.setFont(font)
            self.ui.ServerModulesList.addItem(item)

    def toggle_client_module(self, item):
        """Toggle a client module between enabled and disabled and reload client modules."""
        module_name, status = item.data(Qt.UserRole)
        src_dir = os.path.join("modules", "Parley_modules_client", "enabled" if status == "enabled" else "disabled")
        dst_dir = os.path.join("modules", "Parley_modules_client", "disabled" if status == "enabled" else "enabled")
        src_path = os.path.join(src_dir, f"{module_name}.py")
        dst_path = os.path.join(dst_dir, f"{module_name}.py")
        try:
            os.makedirs(dst_dir, exist_ok=True)
            shutil.move(src_path, dst_path)
            new_status = "disabled" if status == "enabled" else "enabled"
            self.print_redirector.write_general(f"Moved client module {module_name} to {new_status}")
            self.update_module_lists()
            # Reload client modules
            self.load_client_modules()
        except Exception as e:
            self.print_redirector.write_general(f"Error moving client module {module_name}: {e}")

    def toggle_server_module(self, item):
        """Toggle a server module between enabled and disabled and reload server modules."""
        module_name, status = item.data(Qt.UserRole)
        src_dir = os.path.join("modules", "Parley_modules_server", "enabled" if status == "enabled" else "disabled")
        dst_dir = os.path.join("modules", "Parley_modules_server", "disabled" if status == "enabled" else "enabled")
        src_path = os.path.join(src_dir, f"{module_name}.py")
        dst_path = os.path.join(dst_dir, f"{module_name}.py")
        try:
            os.makedirs(dst_dir, exist_ok=True)
            shutil.move(src_path, dst_path)
            new_status = "disabled" if status == "enabled" else "enabled"
            self.print_redirector.write_general(f"Moved server module {module_name} to {new_status}")
            self.update_module_lists()
            # Reload server modules
            self.load_server_modules()
        except Exception as e:
            self.print_redirector.write_general(f"Error moving server module {module_name}: {e}")

    def load_client_modules(self):
        """Load enabled client modules."""
        self.loaded_modules_client = {}
        client_dir = os.path.join("modules", "Parley_modules_client", "enabled")
        if os.path.exists(client_dir):
            self.print_redirector.write_general("[+] Loading Client Modules...")
            for filename in sorted(os.listdir(client_dir)):
                if filename.endswith(".py") and filename != "__init__.py":
                    module_name = filename[:-3]
                    module_path = os.path.join(client_dir, filename)
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.loaded_modules_client[module_name] = module
                    self.print_redirector.write_general(f"\t<-> {module_name} - {module.module_description}")

    def load_server_modules(self):
        """Load enabled server modules."""
        self.loaded_modules_server = {}
        server_dir = os.path.join("modules", "Parley_modules_server", "enabled")
        if os.path.exists(server_dir):
            self.print_redirector.write_general("[+] Loading Server Modules...")
            for filename in sorted(os.listdir(server_dir)):
                if filename.endswith(".py") and filename != "__init__.py":
                    module_name = filename[:-3]
                    module_path = os.path.join(server_dir, filename)
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.loaded_modules_server[module_name] = module
                    self.print_redirector.write_general(f"\t<-> {module_name} - {module.module_description}")

    def load_modules(self):
        """Load enabled client and server modules."""
        self.load_client_modules()
        self.load_server_modules()

    def handle_client(self, client_socket, target_host, target_port, use_tls_client, use_tls_server, certfile, client_certfile):
        """Handle client connection in a separate thread."""
        forward_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sockets.append(client_socket)
        self.client_sockets.append(forward_socket)
        try:
            forward_socket.connect((target_host, target_port))
            client_ip, client_port = client_socket.getpeername()
            server_ip, server_port = forward_socket.getpeername()
            connection_info = (client_ip, client_port, server_ip, server_port)
            self.print_redirector.write(f"[+] Connected to server: {client_ip}:{client_port} -> {server_ip}:{server_port}", connection_info)

            if use_tls_server:
                context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
                if client_certfile:
                    context.load_cert_chain(certfile=client_certfile)
                forward_socket = context.wrap_socket(forward_socket, server_hostname=target_host)

            if use_tls_client:
                client_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                if certfile:
                    client_context.load_cert_chain(certfile=certfile)
                client_socket = client_context.wrap_socket(client_socket, server_side=True)

            sockets = [client_socket, forward_socket]
            buffer_size = 4096
            client_msg_num = 0
            server_msg_num = 0

            while sockets and self.proxy_running:
                readable, _, errored = select.select(sockets, [], sockets, 1.0)
                for s in errored:
                    sockets.remove(s)
                    s.close()
                for s in readable:
                    full_data = bytearray()
                    try:
                        while True:
                            data = s.recv(buffer_size)
                            if not data:
                                break
                            full_data.extend(data)
                            if len(data) < buffer_size:
                                break
                    except socket.error:
                        break
                    if full_data:
                        if s is client_socket:
                            client_msg_num += 1
                            for module_name, module in self.loaded_modules_client.items():
                                full_data = module.module_function(client_msg_num, client_ip, client_port, server_ip, server_port, full_data)
                            forward_socket.sendall(full_data)
                        else:
                            server_msg_num += 1
                            for module_name, module in self.loaded_modules_server.items():
                                full_data = module.module_function(server_msg_num, server_ip, server_port, client_ip, client_port, full_data)
                            client_socket.sendall(full_data)
                    else:
                        sockets.remove(s)
                        s.close()
                        if len(sockets) == 0:
                            break
        except Exception as e:
            self.print_redirector.write(f"Error in connection: {e}", connection_info if 'connection_info' in locals() else None)
        finally:
            for sock in [client_socket, forward_socket]:
                if sock in self.client_sockets:
                    self.client_sockets.remove(sock)
                try:
                    sock.close()
                except:
                    pass

    def start_proxy(self, listen_host, listen_port, target_host, target_port, use_tls_client, use_tls_server, certfile, client_certfile):
        """Start the proxy server in a loop."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_socket.bind((listen_host, listen_port))
            self.server_socket.listen(5)
            self.print_redirector.write_general(f"[+] Listening on: {listen_host}:{listen_port}")
            while self.proxy_running:
                try:
                    self.server_socket.settimeout(1.0)  # Allow checking proxy_running
                    client_socket, addr = self.server_socket.accept()
                    client_ip, client_port = client_socket.getpeername()
                    self.print_redirector.write_general(f"[+] New server socket thread started for {client_ip}:{client_port}")
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket, target_host, target_port, use_tls_client, use_tls_server, certfile, client_certfile))
                    client_thread.daemon = True  # Make client threads daemon
                    client_thread.start()
                    self.client_threads.append(client_thread)
                except socket.timeout:
                    continue
                except Exception as e:
                    self.print_redirector.write_general(f"Error accepting connection: {e}")
                    break
        except Exception as e:
            self.print_redirector.write_general(f"Error starting proxy: {e}")
        finally:
            # Clean up without joining the current thread
            self.proxy_running = False
            if self.server_socket:
                try:
                    self.server_socket.close()
                except:
                    pass
                self.server_socket = None
            # Close all client sockets to unblock select
            for sock in self.client_sockets[:]:
                try:
                    sock.close()
                except:
                    pass
                if sock in self.client_sockets:
                    self.client_sockets.remove(sock)
            # Clear client threads list (daemon threads will terminate on exit)
            self.client_threads.clear()
            self.print_redirector.write_general("[-] Proxy stopped")

    def stop_proxy(self):
        """Stop the proxy and clean up resources."""
        self.print_redirector.write_general("Exiting and closing threads")
        self.proxy_running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
            self.server_socket = None
        # Close all client sockets to unblock select
        for sock in self.client_sockets[:]:
            try:
                sock.close()
            except:
                pass
            if sock in self.client_sockets:
                self.client_sockets.remove(sock)
        # Wait for client threads to terminate
        for thread in self.client_threads[:]:
            try:
                thread.join(timeout=1.0)
            except:
                pass
            self.client_threads.remove(thread)
        self.print_redirector.write_general("[-] Proxy stopped")
        # Close all log files
        self.print_redirector.close()

    def toggle_proxy(self):
        """Toggle the proxy start/stop state."""
        if self.proxy_running:
            self.stop_proxy()
            self.ui.StartStopButton.setText("Start")
        else:
            try:
                listen_host = self.ui.LocalIPLine.text().strip()
                listen_port = int(self.ui.LocalPortLine.text().strip())
                target_host = self.ui.RemoteIPLine.text().strip()
                target_port = int(self.ui.RemotePortLine.text().strip())
                use_tls_client = self.ui.LocalTLSButton.isChecked()
                use_tls_server = self.ui.RemoteTLSButton.isChecked()
                certfile = self.ui.ServerCertPath.text().strip() or None
                client_certfile = self.ui.ClientCertPath.text().strip() or None

                if not target_host:
                    self.print_redirector.write_general("Error: Remote IP is required")
                    return

                self.load_modules()
                self.proxy_running = True
                self.ui.StartStopButton.setText("Stop")
                self.proxy_thread = threading.Thread(target=self.start_proxy, args=(listen_host, listen_port, target_host, target_port, use_tls_client, use_tls_server, certfile, client_certfile))
                self.proxy_thread.daemon = True  # Make proxy thread daemon
                self.proxy_thread.start()
                self.print_redirector.write_general(f"Started proxy: {listen_host}:{listen_port} -> {target_host}:{target_port}")
            except ValueError as e:
                self.print_redirector.write_general(f"Error: Invalid port number: {e}")
                self.proxy_running = False
                self.ui.StartStopButton.setText("Start")
            except Exception as e:
                self.print_redirector.write_general(f"Error starting proxy: {e}")
                self.proxy_running = False
                self.ui.StartStopButton.setText("Start")

    def cleanup(self):
        """Clean up resources before closing."""
        if self.proxy_running:
            self.stop_proxy()

    def showEvent(self, event):
        """Set focus to LocalIPLine when the tab is shown."""
        super().showEvent(event)
        self.ui.LocalIPLine.setFocus()
