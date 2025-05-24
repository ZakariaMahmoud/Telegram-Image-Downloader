import os
import asyncio
from pathlib import Path
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv

class TelegramDownloader:
    def __init__(self):
        load_dotenv()
        self.api_id = int(os.getenv('api_id'))
        self.api_hash = os.getenv('api_hash')
        self.group_name = os.getenv('group_name')
        self.message_limit = os.getenv('message_limit')
        self.client = None
        self.downloads_folder = Path('downloads')
        
    async def connect(self):
        print("Connecting to Telegram...")
        self.client = TelegramClient('session', self.api_id, self.api_hash)
        await self.client.start()
        
        if not await self.client.is_user_authorized():
            phone = input("Enter your phone number: ")
            await self.client.send_code_request(phone)
            code = input("Enter the verification code: ")
            
            try:
                await self.client.sign_in(phone, code)
            except SessionPasswordNeededError:
                password = input("Enter your 2FA password: ")
                await self.client.sign_in(password=password)
        
        print("Connected successfully!")
        
    async def get_group(self):
        try:
            if self.group_name.startswith('https://t.me/'):
                username = self.group_name.split('/')[-1]
                if username.startswith('+'):
                    entity = await self.client.get_entity(self.group_name)
                else:
                    entity = await self.client.get_entity(username)
            elif self.group_name.startswith('@'):
                entity = await self.client.get_entity(self.group_name)
            elif self.group_name.isdigit() or (self.group_name.startswith('-') and self.group_name[1:].isdigit()):
                entity = await self.client.get_entity(int(self.group_name))
            else:
                entity = await self.client.get_entity(self.group_name)
            return entity
        except Exception as e:
            print(f"Error finding group: {e}")
            return None
    
    async def download_images(self):
        entity = await self.get_group()
        if not entity:
            print("Could not find the group")
            return
            
        print(f"Found group: {entity.title}")
        self.downloads_folder.mkdir(exist_ok=True)
        
        limit = None
        if self.message_limit and self.message_limit.strip():
            try:
                limit = int(self.message_limit.strip())
                print(f"Downloading from last {limit} messages")
            except ValueError:
                print("Invalid message limit, downloading all messages")
        
        print("Counting messages...")
        total_messages = 0
        async for message in self.client.iter_messages(entity, limit=limit):
            total_messages += 1
        
        print(f"Found {total_messages} messages to check")
        
        downloaded_count = 0
        processed_count = 0
        
        async for message in self.client.iter_messages(entity, limit=limit):
            processed_count += 1
            
            if processed_count % 100 == 0:
                progress = (processed_count / total_messages) * 100
                print(f"Progress: {processed_count}/{total_messages} ({progress:.1f}%) - Downloaded: {downloaded_count}")
            
            if message.media and isinstance(message.media, MessageMediaPhoto):
                try:
                    filename = f"image_{message.id}.jpg"
                    file_path = self.downloads_folder / filename
                    
                    if file_path.exists():
                        continue
                    
                    print(f"Downloading {filename}...")
                    await self.client.download_media(message.media, file=str(file_path))
                    downloaded_count += 1
                    
                    await asyncio.sleep(0.1)
                    
                except FloodWaitError as e:
                    print(f"Rate limited. Waiting {e.seconds} seconds...")
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    print(f"Error downloading image from message {message.id}: {e}")
                    continue
        
        print(f"Download complete! Downloaded {downloaded_count} images")
        print(f"Images saved to: {self.downloads_folder.absolute()}")
    
    async def disconnect(self):
        if self.client:
            await self.client.disconnect()

async def main():
    downloader = TelegramDownloader()
    
    try:
        await downloader.connect()
        await downloader.download_images()
    except KeyboardInterrupt:
        print("\nDownload stopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await downloader.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
