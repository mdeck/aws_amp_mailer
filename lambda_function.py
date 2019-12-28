import base64, boto3, email.parser, io, json
from botocore.exceptions import ClientError


SENDER = 'Form Inquiries @ k2photo.gallery <k2formsender@gmail.com>'
RECIPIENT = 'K2 photographers <k2photographyde@gmail.com>'


def lambda_handler(event, context):
    status_code, body = 500, ''
    origin = event['headers'].get('origin', '*')

    data = parse_form(event)
    try:
        send_email(data)
        status_code = 200
        body = json.dumps({'sentTo': RECIPIENT})
    except ClientError as e:
        body = json.dumps({'detail': str(e)})

    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        },
        'body': body
    }


def send_email(data):

    def utf8(s):
        return {'Data': s, 'Charset': 'UTF-8'}

    ses = boto3.client('ses')

    response = ses.send_email(
        Source=SENDER,
        Destination={
            'ToAddresses' : [RECIPIENT,],
            # 'CcAddresses' : [],
            # 'BccAddresses': []
        },
        Message={
            'Subject': utf8(data['subject']),
            'Body': {
                'Text': utf8(build_body_text(data)),
                #'Html': utf8('HTML_FORMAT_BODY')
            }
        },
        ReplyToAddresses=[f"{data['name']} <{data['email']}>",],
    )
