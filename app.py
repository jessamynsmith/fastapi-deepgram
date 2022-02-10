import os
import socketio
import uvicorn
from deepgram import Deepgram


DEEPGRAM_API_KEY = os.environ.get('DEEPGRAM_API_KEY')


async def transcript_handler(data):
    print('transcript handler')
    if 'channel' in data:
        transcript = data['channel']['alternatives'][0]['transcript']
        print('received transcript:', transcript)
        await sio.emit('message', f"received: {transcript}")
        print("sent")


async def connect_to_deepgram():
    # Initialize the Deepgram SDK
    dg_client = Deepgram(DEEPGRAM_API_KEY)

    # Create a websocket connection to Deepgram
    try:
        dg_socket = await dg_client.transcription.live({'punctuate': True})

        # Listen for the connection to close
        dg_socket.registerHandler(dg_socket.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))

        # Print incoming transcription objects
        dg_socket.registerHandler(dg_socket.event.TRANSCRIPT_RECEIVED, transcript_handler)
    except Exception as e:
        print(f'Could not open socket: {e}')

    return dg_socket


async def process_audio(connection, data):
    print('processing audio', len(data))
    await sio.emit('message', f"received audio")

    connection.send(data)

    # Indicate that we've finished sending data
    print('finishing')
    await connection.finish()
    print('finished')


static_files = {
    '/static': './public',
}


# create a Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi')


@sio.on('message')
async def print_message(sid, message):
    print("Socket ID: ", sid)
    await sio.emit('message', f"received: {message}")


@sio.on('audio')
async def print_message(sid, data):
    print("Socket ID: ", sid)
    dg_socket = await connect_to_deepgram()
    await process_audio(dg_socket, data)


# wrap with ASGI application
app = socketio.ASGIApp(sio, static_files=static_files)

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
