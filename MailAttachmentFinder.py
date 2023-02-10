import imaplib
import email
import os

def get_attachments(email_id, mail):
    result, data = mail.fetch(email_id, "(RFC822)")
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)

    attachments = []

    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        attachments.append(part.get_filename())
    
    return attachments

def display_attachments(mail, target_email_address):
    mail.select("inbox")
    result, data = mail.search(None, f'FROM "{target_email_address}"')
    email_ids = data[0].split()

    attachments = []

    for email_id in email_ids:
        attachments.extend(get_attachments(email_id, mail))
    
    if attachments:
        print("Attachments:")
        for attachment in attachments:
            print(attachment)
    else:
        print("No attachments found.")

if __name__ == '__main__':
    email_address = input("Enter your Gmail address: ")
    password = input("Enter your Gmail password: ")
    target_email_address = input("Enter the target Gmail address: ")

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_address, password)

    display_attachments(mail, target_email_address)

    mail.logout()
