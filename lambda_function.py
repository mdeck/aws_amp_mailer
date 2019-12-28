import base64, boto3, email.parser, email.policy, io, json
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


def parse_form(event):
    ct_header = event['headers']['content-type']
    body = base64.b64decode(event['body']).decode()

    src = f'Content-Type: {ct_header}\n\n{body}'
    msg = email.parser.Parser(policy=email.policy.HTTP).parsestr(src)

    name_of = lambda p: p['content-disposition'].params['name']
    return {name_of(p): p.get_content() for p in msg.iter_parts()}


def build_body_text(data):
    return f'''
        The following message was submitted via the k2photo.gallery inquiry form:
        
        Sender: {data['name']} ({data['email']})
        
        Subject: {data['subject']}
        
        Message:
        {data['message']}
    '''
