import speech_recognition as sr
from pynput.mouse import Button, Controller
import time
import re
import subprocess
from pynput.keyboard import Controller as Controller_k, Key
import pygetwindow as gw
from win32 import win32gui
from emailer import *
keyboard = Controller_k()
import os
def create_email(path, email):
    '''
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    import base64
    import os
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders

    # Step 1: Authenticate & Get Token
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)

    # Step 2: Create Gmail API Service
    service = build("gmail", "v1", credentials=creds)

    # Step 3: Create & Send an Email with Attachment
    def send_email(sender, to, subject, message_text, file_path):
        # Create email container
        message = MIMEMultipart()
        message["to"] = email
        message["from"] = sender
        message["subject"] = "Email from" + sender

        # Attach text content
        message.attach(MIMEText(message_text, "plain"))

        # Attach file if provided
        if file_path:
            file_name = os.path.basename(file_path)
            with open(file_path, "rb") as file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file.read())

            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={file_name}")
            message.attach(part)

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
        
        print(f"Message sent: {send_message['id']}")

    # Example Usage
    send_email(
        "your-email@gmail.com",
        "recipient@gmail.com",
        "Test Email with Attachment",
        "Hello, this email has an attachment!",
        path  # Change to the actual file path
    )
    '''
    return 'success'
def get_file():
    os.startfile("dropper.exe")


    # Wait for the window to appear
    time.sleep(1)  # Adjust as needed

    # Find and move the window
    for window in gw.getWindowsWithTitle("dropper"):  # Adjust title if necessary
        win32gui.MoveWindow(window._hWnd, 0, 0, window.width, window.height, True)
        break
    mouse = Controller()
    
    # Get the current mouse position
    start_x, start_y = mouse.position
    mouse.press(Button.left)
    # Press and hold the left button
    time.sleep(0.5)
    
    # Move to the target position
    mouse.position = (100, 100)
    time.sleep(0.1)  # Simulate a drag duration
    
    # Release the left button
    mouse.release(Button.left)
    time.sleep(0.1)
    # Press and release the Enter key
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(0.1) 
    keyboard.press(Key.enter)
    
    keyboard.release(Key.enter)
    time.sleep(0.4)
   
    with open('data/path.txt', 'r') as f:
        path = f.read()
    return path
def send_email(recp):
    path = get_file()
    email = get_email_by_name(recp)
    
    create_email(path, email)
    from plyer import notification
 
    notification.notify(
        title="Success!",
        message="Email sent with file to "+recp,
        app_name="Dropper",
        timeout=5  # Notification disappears after 5 seconds
    )
def tell_time():
   
    from plyer import notification
    from datetime import datetime

    now = datetime.now()
    
    notification.notify(
        title="Time is " + now.strftime("%H:%M:%S"),
        message="Greetings from dropper",
        app_name="Dropper",
        timeout=5  # Notification disappears after 5 seconds
    )
def uploader(path):
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": os.path.basename(file_path)}
    media = MediaFileUpload(path, mimetype=mime_type)

    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
def upload_to_drive():
    path = get_file()
    
    uploader(path)
    from plyer import notification
   
    notification.notify(
        title="Success!",
        message="Upload Success" + path,
        app_name="Dropper",
        timeout=5  # Notification disappears after 5 seconds
    )
def parse_command(command):
    command = command.lower()
    
    # Ensure "dropper" is in the command
    if "dropper" not in command:
        return None, "No invocation of 'dropper' found."
    
    # Check if it contains an intent to email
    if "upload" in command:
        upload_to_drive()
    if "time" in command:
        tell_time()
    if "email"  in command:
    
        # Extract recipient's name
        match = re.search(r'email (?:this file to|the file to|to) ([A-Za-z]+)', command)
        if match:
            recipient = match.group(1)
            send_email(recipient)
        else:
            pass        
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        try:
            audio = recognizer.listen(source)  # Listen to user's speech
            text = recognizer.recognize_google(audio)  # Convert speech to text
            parse_command(text)
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            pass
if __name__ == "__main__":
    while True:
        recognize_speech()
