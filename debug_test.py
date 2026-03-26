import asyncio
import traceback

def run_debug():
    try:
        from main import conf, MessageSchema, MessageType, FastMail, SignupRequest
        print("Imports successful.")
        
        print("Testing MessageSchema validation...")
        msg = MessageSchema(
            subject="Test subject",
            recipients=["test@test.com"],
            body="Test body",
            subtype=MessageType.plain
        )
        print("MessageSchema successful.")
        
        print("Testing FastMail instantiation...")
        fm = FastMail(conf)
        print("FastMail instantiated successfully.")
        
    except Exception as e:
        print("ERROR IN DEBUG:")
        traceback.print_exc()

if __name__ == "__main__":
    run_debug()
