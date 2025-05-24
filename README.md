# Telegram Image Downloader

Ever wanted to download all images from a Telegram group? This tool does exactly that!

## What it does

- Downloads all images from any Telegram group you're in
- Organizes everything neatly in a downloads folder
- Works with any group size (handles rate limits automatically)
- Skips videos and documents - only downloads images

## Quick Start

1. **Get Telegram API access** (takes 2 minutes)
   - Go to https://my.telegram.org/apps
   - Login with your phone number
   - Create a new app (any name works)
   - Copy the `api_id` and `api_hash`

2. **Setup**
   ```bash
   # Easy setup (installs everything)
   python setup.py
   
   # Or manually:
   pip install -r requirements.txt
   cp .env.example .env
   ```

3. **Configure**
   Edit `.env` file with your info:
   ```
   api_id=your_numbers_here
   api_hash=your_hash_here
   group_name=@your_group
   ```

4. **Download images**
   ```bash
   python telegram_downloader.py
   ```

## Configuration

Edit the `.env` file with your settings:

```
api_id=12345678
api_hash=abcdef1234567890abcdef1234567890
group_name=@your_group_name
message_limit=100
```

- `api_id` and `api_hash`: Get these from my.telegram.org
- `group_name`: Can be @username, group link, or numeric ID
- `message_limit`: Number of recent messages to check (leave empty for all)

## Examples

```bash
# Basic download
python telegram_downloader.py

# Using the run script
./run.sh download
```

## First Time Setup

When you run the downloader for the first time, it will ask for:
- Your phone number
- Verification code from Telegram
- 2FA password (if you have it enabled)

After that, it remembers your login.

## Output

- Downloaded images go to `downloads/` folder
- Each image is named with its message ID to avoid duplicates
- Safe to re-run - won't download duplicates

## Pro Tips

- Don't worry about rate limits - it handles them automatically
- Safe to re-run - won't download duplicates
- Works with any group size
- Only downloads images, skips everything else

## Troubleshooting

**"Could not find group"**
- Make sure you're a member of the group
- Try using the full group link instead of username
- For private groups, use the invite link

**"API credentials error"**
- Double-check your api_id and api_hash
- Make sure there are no extra spaces in .env file

**"No images found"**
- The group might not have any images
- Check if message_limit is too small

## Requirements

- Python 3.8+
- Telegram account
- Access to the group you want to download from

## Privacy

- Your credentials stay on your computer
- The tool only downloads images you already have access to
- No data is sent anywhere except to Telegram's official API
