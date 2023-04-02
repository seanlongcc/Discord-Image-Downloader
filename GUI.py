import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
import discord_downloader

app = QApplication(sys.argv)

window = QWidget()
layout = QVBoxLayout()

# input fields
labels = ['Token', 'Guild ID', 'Channel ID', 'Start Date', 'End Date']
inputs = {}

for label in labels:
    lbl = QLabel(label)
    layout.addWidget(lbl)
    le = QLineEdit()
    layout.addWidget(le)
    inputs[label] = le

# button
btn = QPushButton('Download Attachments')
layout.addWidget(btn)

# set up window
window.setLayout(layout)
window.setWindowTitle('Discord Attachments Downloader')


def on_download_attachments():
    TOKEN = inputs['Token'].text()
    GUILD_ID = int(inputs['Guild ID'].text())
    CHANNEL_ID = int(inputs['Channel ID'].text())
    START_DATE = inputs['Start Date'].text()
    END_DATE = inputs['End Date'].text()

    discord_downloader.start_downloader(TOKEN_IN=TOKEN, GUILD_ID_IN=GUILD_ID,
                                        CHANNEL_ID_IN=CHANNEL_ID, START_DATE_IN=START_DATE, END_DATE_IN=END_DATE)


btn.clicked.connect(on_download_attachments)

window.show()
sys.exit(app.exec())
