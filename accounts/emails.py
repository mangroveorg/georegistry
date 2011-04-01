from django.core.mail import EmailMessage

def send_reply_email(request, post, form):
    subject = "Someone has replied to '%s' on georegistry.org" % (
        post.title)
    
    sender = request.user.email
    
    body = "In reference to %s, %s said:\n\n%s" % (
        request.build_absolute_uri(post.get_absolute_url()),
        sender,
        form.cleaned_data['content'])
    to = (post.contact.email,)
    headers = {'Reply-To': sender}

    email = EmailMessage(subject=subject,
                         body=body,
                         from_email='gr@georegistry.org',
                         to=to,
                         headers=headers)
    email.send()

