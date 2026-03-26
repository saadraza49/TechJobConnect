import asyncio
import traceback

async def run_debug():
    try:
        from main import conf, MessageSchema, MessageType, FastMail
        print("Testing FastMail send_message...")
        
        msg = MessageSchema(
            subject="Test subject",
            recipients=["msaadraza49@gmail.com"],
            body="Test body",
            subtype=MessageType.plain
        )
        
        fm = FastMail(conf)
        await fm.send_message(msg)
        print("Email sent successfully!")
        
    except Exception as e:
        print("ERROR SENDING EMAIL:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_debug())
