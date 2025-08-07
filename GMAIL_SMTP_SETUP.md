# Gmail SMTP Configuration for Production

## Overview
This guide explains how to configure Gmail SMTP for the booking system's email notifications in production.

## Gmail SMTP Settings
To enable Gmail SMTP, update your `config_production.json` with these settings:

```json
"email": {
    "enabled": true,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "use_tls": true,
    "sender_email": "your-company-email@gmail.com",
    "sender_password": "your-app-password",
    "recipient_email": "notifications@dacpol.eu",
    "sender_name": "DACPOL Booking System"
}
```

## Gmail App Password Setup
1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and generate password
   - Use this 16-character password in `sender_password`

## Railway Environment Variables (Recommended)
For security, set email credentials as Railway environment variables:

```bash
# In Railway dashboard, add these environment variables:
GMAIL_EMAIL=your-company-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password
NOTIFICATION_EMAIL=notifications@dacpol.eu
```

## Code Modification for Environment Variables
Update `config.py` to read from environment variables in production:

```python
import os

def load_config():
    # ... existing code ...
    
    # Override email settings with environment variables if available
    if config.get('email', {}).get('enabled') and os.getenv('RAILWAY_ENVIRONMENT'):
        config['email']['sender_email'] = os.getenv('GMAIL_EMAIL', config['email']['sender_email'])
        config['email']['sender_password'] = os.getenv('GMAIL_APP_PASSWORD', config['email']['sender_password'])
        config['email']['recipient_email'] = os.getenv('NOTIFICATION_EMAIL', config['email']['recipient_email'])
    
    return config
```

## Benefits of Gmail SMTP
✅ **Reliable delivery** - Gmail has excellent deliverability
✅ **Free for moderate usage** - Up to 500 emails per day
✅ **Easy setup** - Well-documented process
✅ **Secure** - Uses App Passwords instead of main password

## Testing
After configuration, test email functionality:
1. Create a test reservation
2. Check that notification emails are sent
3. Verify emails arrive in recipient inbox

## Production Deployment
1. Update `config_production.json` with Gmail settings
2. Set Railway environment variables (recommended)
3. Deploy changes via git push
4. Test email functionality on live system

## Notes
- Keep App Password secure and never commit it to git
- Consider using Railway environment variables for sensitive data
- Monitor email usage to stay within Gmail's daily limits
- For high volume, consider upgrading to Google Workspace
