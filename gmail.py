import random
from email.message import EmailMessage
import smtplib
import ssl
import time
import audit_template

def send_email(email_receiver, seo_info, company):
    # worked = False

    subject1 = 'Get More Customers'
    subject2 = 'Want More Customers?'

    body1 = '''Hi - This is David with Kayusi Digital. 

We noticed your website on Yellow Pages and wanted to offer our SEO services.

We help small businesses generate qualified leads by strengthening their SEO score. 

This encourages Google to rank your website on search results much higher than your competitors.

Attached below is a quick SEO audit we did on your website's homepage. 

If you like it, we can work on the remainder of your website as well as create weekly articles using industry-niche keywords. (Google likes this a lot) 

I look forward to your response.

Thanks,
David'''

    body2 = '''Hi - I saw your services on Yellow Pages and wanted to offer our SEO services.
    
We help small businesses generate qualified leads by strengthening their SEO score. 

This encourages Google to rank your website on search results much higher than your competitors.

Attached below is a quick SEO audit we did on your website's homepage. 

If you like it, we can work on the remainder of your website as well as create weekly articles using industry-niche keywords. (Google likes this a lot) 

I look forward to your response.

Thanks,
David'''

    body3 = '''Hi - I saw your services on Yellow Pages and wanted to offer our SEO services.

We help small businesses generate qualified leads by strengthening their SEO score. 

Attached below is a quick SEO audit we did on your website's homepage. 

Ultimately we'd like to clean up all of your sites errors and begin making weekly articles so that Google ranks you in their search results higher.

Our services for 4 monthly articles (1 per week) is $350 / month. 

Let us know if you're interested in taking your business to the next level. 

Thanks,
David'''

    subjects = [subject1, subject2]
    bodies = [body1, body2, body3]

    subject = random.choice(subjects)
    body = random.choice(bodies)


    email_sender = "{{ENABLE GMAIL 2FA THEN INSERT YOUR EMAIL HERE}}"
    email_password = "{{ENABLE GMAIL 2FA THEN INSERT YOUR 2FA CODES  HERE}}"

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)



    audit_template.create_audit(company, seo_info)

    with open(f"{company}.pdf", 'rb') as f:
        file_data = f.read()
        file_name = f.name

    em.add_attachment(file_data, maintype="application", subtype='octet-stream', filename=file_name)

    context = ssl.create_default_context()

    # while not worked:
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            print("Email sent.")

            # worked = True
    except Exception as e:
        print(e)
        time.sleep(43200)
        print("Email limit reached. Sleeping for 12 hours")



