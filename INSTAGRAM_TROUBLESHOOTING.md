# Instagram Rate Limit Troubleshooting Guide

When working with the Instagram API via scraping tools like Instaloader, you may encounter rate limiting issues. Here's how to handle them:

## Common Error Messages

1. **"Please wait a few minutes before you try again"** (401 Unauthorized)
2. **"Forbidden"** (403 Forbidden)
3. **"Too many requests"** (429 Too Many Requests)

## Solutions

### 1. Authenticate with a valid Instagram account

The most effective way to reduce rate limiting is to use valid Instagram credentials:

```
IG_LOGIN_USERNAME=your_instagram_username
IG_LOGIN_PASSWORD=your_instagram_password
```

Add these to your `.env` file.

### 2. Use a proxy server

If you're consistently getting rate limited, try using a proxy:

```
USE_PROXY=true
PROXY_URL=http://your-proxy-host:port
```

### 3. Adjust delay and retry settings

Increase delay times to appear more like a human user:

```
BASE_DELAY=30  # Longer delay before retries
MAX_RETRIES=5  # More retry attempts
```

### 4. Rotate between multiple accounts

Create multiple Instagram accounts and rotate between them to avoid hitting rate limits on a single account.

### 5. Wait before trying again

Instagram rate limits usually reset after some time. If all else fails:
- Wait at least 24 hours before trying again
- Try from a different network/IP address
- Use a VPN service (as a last resort)

## Note on Instagram's Terms of Service

Remember that excessive scraping may violate Instagram's Terms of Service. Always use the script responsibly and ethically, and consider whether official API access might be more appropriate for your needs.
