RLWP – RLWP_1.0 Protocol Implementation

This project is an experimental implementation of the RLWP_1.0 protocol, a lightweight client-server communication system without HTTP.
It allows sending commands, reading files, deleting files, creating files in two steps (header + body), and basic multi-client support.

⚡ Supported Commands

Client → Server

Code	Description
PING RLWP/1.0	Handshake
INFO RLWP/1.0	Server info
LIST RLWP/1.0	List files
GET <file> RLWP/1.0	Download file
DELETE <file> RLWP/1.0	Delete file
0x010 <filename> RLWP/1.0	Start file creation (header = filename)
0x011 <content> RLWP/1.0	Send file content (body)
SHUTDOWN RLWP/1.0	Shutdown server safely
🖥️ How to Use

Start the server:

python server.py

Server listens on port 5000 by default

Colored messages: green = received, yellow = sent, purple = status, red = errors

Start the client:

python client.py

Interactive client

Automatic retry if server is not reachable

Type RLWP commands directly

Type exit to quit

Create a file (header + body):

0x010 ciao.txt RLWP/1.0
0x011 This is the file content RLWP/1.0
📂 Project Structure
RLWP/
│ server.py      # RLWP server
│ client.py      # Interactive client
│ file_server/   # Folder where files are saved
⚠️ Notes

Server handles one client at a time (threaded/multi-client version planned)

SHUTDOWN RLWP/1.0 shuts down the server from any client

All errors are handled only on the server, client never crashes

File names and content are sanitized (os.path.basename)

🔧 Future Improvements

True multi-client support with threading or asyncio

Binary file support (base64)

Timeout handling for file creation

Duplicate file name management

Client improvements: colored messages, simplified file sending
