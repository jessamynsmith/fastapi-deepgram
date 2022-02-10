import socketio
import uvicorn


static_files = {
    '/static': './public',
}


# create a Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi')


@sio.on('message')
async def print_message(sid, message):
    ## When we receive a new event of type
    ## 'message' through a socket.io connection
    ## we print the socket ID and the message
    print("Socket ID: ", sid)
    print(message)


# wrap with ASGI application
app = socketio.ASGIApp(sio, static_files=static_files)

uvicorn.run(app, host='127.0.0.1', port=8000)
