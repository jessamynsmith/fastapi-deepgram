import socketio
import uvicorn


static_files = {
    '/static': './public',
}


# create a Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi')


@sio.on('message')
async def print_message(sid, message):
    print("Socket ID: ", sid)
    print(message)


@sio.on('audio')
async def print_message(sid, message):
    print("Socket ID: ", sid)


# wrap with ASGI application
app = socketio.ASGIApp(sio, static_files=static_files)

uvicorn.run(app, host='127.0.0.1', port=8000)
