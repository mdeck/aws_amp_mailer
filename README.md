# aws_amp_mailer

This is an AWS Lambda function which receives a contact form and sends it via email.  I'm using it in practice to implement a "Contact Us" [amp-form](https://amp.dev/documentation/components/amp-form/) on an AMPHTML site.  [See it live](https://www.k2photo.gallery/contact/).

It uses AWS Simple Email Service (SES) to transmit the email.  In this implementation, both the sender and recipient email addresses are verified through AWS.  Thus, there is no need to exit the default SES sandbox.  If you use this to directly email other people, you will need to [request production access from Amazon](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html).

It uses Python's built-in email.parser lib to parse the input MIME-encoded form data (Content-Type: multipart/form-data).

The lambda should be assigned in API Gateway to a POST resource LAMBDA_PROXY integration request.
The method response headers should include Access-Control-Allow-Origin.
