import sys
import os
import subprocess
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class InfoDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Input Field Information")
        self.setStyleSheet("background-color: #282a36; color: white; font-size: 14pt; font-weight: bold;")

        layout = QVBoxLayout()
        layout.setSpacing(25)

        info_text = """
        - Download Folder: Folder where files will be downloaded.
        - Backup Folder: Folder where backup will be saved.
        - Client JSON: Path to your Google client json.
        - Hour: Hour to start the backup.
        - Minute: Minute to start the backup.
        - Retention Days: The number of days to retain the backup.
        - Sendgrid API Key: Your SendGrid API key (optional).
        - From Email: Email to send notifications from (optional - requires SendGrid API key).
        - To Email: Email to send notifications to (optional - requires SendGrid API key).
        """
        info_label = QLabel(info_text)
        layout.addWidget(info_label)

        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("background-color: #44475a; color: white; font-size: 14pt; font-weight: bold; border-radius: 25px;")
        ok_button.clicked.connect(self.close)
        layout.addWidget(ok_button)

        self.setLayout(layout)


class ErrorDialog(QMessageBox):
    def __init__(self, message):
        super().__init__()

        self.setIcon(QMessageBox.Warning)
        self.setText(message)
        self.setWindowTitle("Input Error")
        self.setStyleSheet("background-color: #282a36; color: white; font-size: 14pt; font-weight: bold;")

class BackupThread(QThread):
    def __init__(self, config):
        QThread.__init__(self)
        self.config = config

    def run(self):
        subprocess.run(['python', 'backup.py'] + self.config)


def add_entry_with_label(layout, label_text, echo_mode=None, width=550):
    label = QLabel(label_text)
    label.setStyleSheet("color: white; font-size: 14pt; font-weight: bold;")
    
    line_edit = QLineEdit()
    line_edit.setFixedHeight(35)
    line_edit.setFixedWidth(width)
    line_edit.setStyleSheet("color: white; padding-left: 10px; background-color: #44475a; border-radius: 10px;")
    
    if echo_mode is not None:
        line_edit.setEchoMode(echo_mode)

    layout.addRow(label, line_edit)

    return line_edit


class BackupApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Backup Configuration')
        self.setGeometry(500, 200, 900, 600)
        self.setStyleSheet("background-color: #282a36;")

        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(50, 50, 50, 50)

        self.entries = []
        self.entry_labels = ['Download Folder', 'Backup Folder', 'Client JSON', 'Hour', 'Minute', 'Retention Days', 'Sendgrid API Key (optional)', 'From Email (optional - requires SendGrid API key)', 'To Email (optional - requires SendGrid API key)']

        row1 = QFormLayout()
        self.entries.append(add_entry_with_label(row1, self.entry_labels[0]))
        self.entries.append(add_entry_with_label(row1, self.entry_labels[1])) 
        self.entries.append(add_entry_with_label(row1, self.entry_labels[2]))
        layout.addLayout(row1)

        row2 = QFormLayout()
        self.entries.append(add_entry_with_label(row2, self.entry_labels[3], width=70))
        self.entries.append(add_entry_with_label(row2, self.entry_labels[4], width=70))
        self.entries.append(add_entry_with_label(row2, self.entry_labels[5], width=70))
        layout.addLayout(row2)

        row3 = QFormLayout()
        self.entries.append(add_entry_with_label(row3, self.entry_labels[6], QLineEdit.Password))
        self.entries.append(add_entry_with_label(row3, self.entry_labels[7]))
        self.entries.append(add_entry_with_label(row3, self.entry_labels[8]))
        layout.addLayout(row3)

        button_layout = QHBoxLayout()

        info_button = QPushButton("Info")
        info_button.setFixedHeight(50)
        info_button.setFixedWidth(150)
        info_button.setStyleSheet("background-color: #44475a; color: white; font-size: 14pt; font-weight: bold; border-radius: 25px;")
        info_button.clicked.connect(self.show_info)
        button_layout.addWidget(info_button)

        backup_button = QPushButton("Start Backup")
        backup_button.setFixedHeight(50)
        backup_button.setFixedWidth(150)
        backup_button.setStyleSheet("background-color: #44475a; color: white; font-size: 14pt; font-weight: bold; border-radius: 25px;")
        backup_button.clicked.connect(self.start_backup)
        button_layout.addWidget(backup_button)

        save_button = QPushButton("Save Configuration")
        save_button.setFixedHeight(50)
        save_button.setFixedWidth(200)
        save_button.setStyleSheet("background-color: #44475a; color: white; font-size: 14pt; font-weight: bold; border-radius: 25px;")
        save_button.clicked.connect(self.save_config)
        button_layout.addWidget(save_button)

        load_button = QPushButton("Load Configuration")
        load_button.setFixedHeight(50)
        load_button.setFixedWidth(200)
        load_button.setStyleSheet("background-color: #44475a; color: white; font-size: 14pt; font-weight: bold; border-radius: 25px;")
        load_button.clicked.connect(self.load_config)
        button_layout.addWidget(load_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_config(self):
        dialog = QFileDialog(self)
        dialog.setStyleSheet("color: white;")
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter("JSON Files (*.json)")
        dialog.setDefaultSuffix('json')
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        if dialog.exec_() == QDialog.Accepted:
            file_name = dialog.selectedFiles()[0]
            data = {label: entry.text() for label, entry in zip(self.entry_labels, self.entries)}
            with open(file_name, 'w') as f:
                json.dump(data, f)

    def load_config(self):
        dialog = QFileDialog(self)
        dialog.setStyleSheet("color: white;")
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("JSON Files (*.json)")
        if dialog.exec_() == QDialog.Accepted:
            file_name = dialog.selectedFiles()[0]
            with open(file_name, 'r') as f:
                data = json.load(f)
            for label, entry in zip(self.entry_labels, self.entries):
                if label in data:
                    entry.setText(data[label])

    def show_info(self):
        dialog = InfoDialog()
        dialog.exec_()

    def start_backup(self):
        flags = [
            '--download_folder',
            '--backup_folder',
            '--client_json',
            '--hour',
            '--minute',
            '--retention_days',
            '--sendgrid_api_key',
            '--from_email',
            '--to_email'
        ]
        config = []
        optional_fields = {
            'filled': 0,
            'names': ['Sendgrid API Key', 'From Email', 'To Email'],
            'values': []
        }

        for i, (flag, entry) in enumerate(zip(flags, self.entries)):
            text = entry.text()

            if i in [6, 7, 8]:
                if text:
                    optional_fields['filled'] += 1
                    optional_fields['values'].extend([flag, text])
            else:
                if not text:
                    dialog = ErrorDialog(f"{self.entry_labels[i]} must be filled.")
                    dialog.exec_()
                    return

                if flag in ['--download_folder', '--backup_folder', '--client_json']:
                    text = os.path.normpath(text.strip('"'))
                config.append(flag)
                config.append(text)

        if optional_fields['filled'] not in [0, 3]:
            dialog = ErrorDialog("All or none of 'Sendgrid API Key', 'From Email', and 'To Email' fields must be filled.")
            dialog.exec_()
            return

        if optional_fields['filled'] == 3:
            config.extend(optional_fields['values'])

        try:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Backup process is starting. See the terminal window for any errors or watching the backup progress...")
            msg.setWindowTitle("Backup Status")
            msg.setStyleSheet("background-color: #282a36; color: white; font-size: 14pt; font-weight: bold;")
            msg.exec_()
            self.backupThread = BackupThread(config)
            self.backupThread.start()
        except KeyboardInterrupt:
            sys.exit()


def main():
    app = QApplication(sys.argv)
    window = BackupApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
