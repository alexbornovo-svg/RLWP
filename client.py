import socket
import time

HOST = "127.0.0.1"  # IP del server
PORT = 5000          # Porta RLWP
RETRY_DELAY = 3      # secondi tra i tentativi
MAX_RETRIES = 5      # massimo tentativi

def send(msg):
    """Invia un messaggio al server RLWP e ritorna la risposta con retry se il server non risponde"""
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.send((msg + "\n\n").encode())
                response = s.recv(4096).decode()
            return response
        except ConnectionRefusedError:
            attempt += 1
            print(f"[Errore] Server non raggiungibile, tentativo {attempt}/{MAX_RETRIES}. Riprovo tra {RETRY_DELAY} sec...")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            return f"[Errore] {e}"
    return "[Errore] Impossibile connettersi al server dopo più tentativi."

def main():
    print("\033[96m=== Client RLWP Interattivo ===\033[0m")
    print("Digita 'exit' per uscire.\n")

    # Handshake automatico
    print("\033[94m[Client] Handshake: PING RLWP/1.0\033[0m")
    response = send("PING RLWP/1.0")
    print(f"\033[92m[Server]\033[0m {response.strip()}\n")

    while True:
        cmd = input("\033[94mInserisci comando RLWP> \033[0m")
        if cmd.lower() == "exit":
            print("Chiusura client.")
            break
        if not cmd.strip():
            continue

        response = send(cmd)
        print(f"\033[92m[Server]\033[0m {response.strip()}\n")

if __name__ == "__main__":
    main()