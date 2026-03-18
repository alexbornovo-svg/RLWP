import socket
import os

SERVER_DIR = "file_server"
os.makedirs(SERVER_DIR, exist_ok=True)

file_in_progress = {}
VALID_COMMANDS = ["PING", "INFO", "LIST", "GET", "DELETE", "0x010", "0x011", "SHUTDOWN"]

def read_message(conn):
    data = b""
    while b"\n\n" not in data:
        chunk = conn.recv(1024)
        if not chunk:
            break
        data += chunk
    return data.decode().strip()

def handle(conn):
    try:
        msg = read_message(conn)
        addr = conn.getpeername()
        print(f"\033[92m[Server] Messaggio ricevuto da {addr}:\033[0m {msg}")

        response = ""
        # HANDSHAKE
        if msg.startswith("PING"):
            response = "RLWP/1.0 14 24\n\n"
        elif msg.startswith("INFO"):
            response = "RLWP/1.0 25 20\n\nRLWP Server 1.0 - Lista file disponibile"
        elif msg.startswith("LIST"):
            files = os.listdir(SERVER_DIR)
            file_list = "\n".join(files) if files else "Nessun file"
            response = f"RLWP/1.0 12 21\n\n{file_list}\nRLWP/1.0 22 22\n\n"
        elif msg.startswith("GET"):
            parts = msg.split()
            filename = os.path.basename(parts[1]) if len(parts) > 1 else ""
            path = os.path.join(SERVER_DIR, filename)
            if filename and os.path.exists(path):
                with open(path, "r") as f:
                    content = f.read()
                response = f"RLWP/1.0 10 21\n\n{content}\nRLWP/1.0 22 22\n\n"
            else:
                response = "RLWP/1.0 00 44\n\nFile not found"
        elif msg.startswith("DELETE"):
            parts = msg.split()
            filename = os.path.basename(parts[1]) if len(parts) > 1 else ""
            path = os.path.join(SERVER_DIR, filename)
            if filename and os.path.exists(path):
                os.remove(path)
                response = "RLWP/1.0 13 20\n\nFile deleted"
            else:
                response = "RLWP/1.0 00 44\n\nFile not found"
        # CREAZIONE FILE IN DUE FASI
        elif msg.startswith("0x010"):
            parts = msg.split()
            filename = parts[1] if len(parts) > 1 else ""
            if filename:
                file_in_progress[addr] = filename
                response = f"RLWP/1.0 0x010 20\n\nHeader received: {filename}"
            else:
                response = "RLWP/1.0 00 40\n\nMissing file header"
        elif msg.startswith("0x011"):
            if addr not in file_in_progress:
                response = "RLWP/1.0 00 41\n\nNo file header received"
            else:
                body = " ".join(msg.split()[1:])
                filename = file_in_progress.pop(addr)
                path = os.path.join(SERVER_DIR, os.path.basename(filename))
                with open(path, "w") as f:
                    f.write(body)
                response = f"RLWP/1.0 0x011 20\n\nFile saved: {filename}"
        elif msg.startswith("SHUTDOWN"):
            response = "RLWP/1.0 99 20\n\nServer shutting down"
            conn.send(response.encode())
            print("\033[95m[Server] Chiusura server richiesta.\033[0m")
            return "SHUTDOWN"
        else:
            response = "RLWP/1.0 00 45\n\nInvalid command"

        conn.send(response.encode())
        print(f"\033[93m[Server] Risposta inviata:\033[0m {response.strip()}")
        return response
    except Exception as e:
        # Tutti gli errori sono gestiti qui, il client non crasha
        error_response = f"RLWP/1.0 00 41\n\nServer error: {e}"
        conn.send(error_response.encode())
        print(f"\033[91m[Server] Errore interno:\033[0m {e}")
        return error_response

# AVVIO SERVER
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 5000))
server.listen()
print("\033[95m[Server] RLWP attivo sulla porta 5000\033[0m")

try:
    while True:
        conn, _ = server.accept()
        result = handle(conn)
        conn.close()
        if result == "SHUTDOWN":
            break
except KeyboardInterrupt:
    print("\n\033[95m[Server] Chiuso manualmente con Ctrl+C\033[0m")
finally:
    server.close()
    print("\033[95m[Server] Chiusura completata.\033[0m")