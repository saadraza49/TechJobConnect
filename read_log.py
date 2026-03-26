import io
try:
    with io.open('uvicorn_error.log', 'r', encoding='utf-16-le') as f:
        content = f.read()
        print("LOG CONTENT:")
        print(content[-2000:])
except Exception as e:
    print(e)
