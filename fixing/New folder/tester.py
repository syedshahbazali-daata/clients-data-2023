import imaplib
import email
import traceback
import re

# Login credentials

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "forghm25" + ORG_EMAIL
FROM_PWD = "wgbmvkduugowwmsl"

SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993


def read_email_from_gmail_and_get_code():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')

        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id, first_email_id, -1):
            typ, data = mail.fetch(str(i).encode(), '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode('utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')

                    email_body = msg.get_payload()
                    if isinstance(email_body, list):
                        email_body = ''.join(str(part) for part in email_body)
                    # print('Description : ' + email_body + '\n')
                    # print("------------------------------")

                    # print(email_body)


                    if "verification code".lower() in str(email_body).lower():
                        print('Found')
                        try:
                            code = re.findall(r'(\d{6})\n', email_body)[0]
                            print(code)
                            return code
                        except:
                            pass

    except Exception:
        traceback.print_exc()




read_email_from_gmail_and_get_code()