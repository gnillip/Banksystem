import json, socket

def load_ENV() -> dict:
    with open("env.json", "r") as f:
        if f == "":
            raise SystemError("ERROR: Couldn't load ENV!")
        return json.load(f)

def load(filename:str, isJson:bool) -> dict|str:
    with open(filename, "r") as data:
        if isJson:
            return json.load(data)
        else:
            return data.read()

def write(filename:str, data:dict|str) -> None:
    with open(filename, "w") as f:
        if type(data) == dict:
            json.dump(data, f, indent=4)
        else:
            f.write(data)

def recv_exact(conn:socket.socket, n:int):
    data = b""
    while len(data) < n:
        chunk = conn.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Socket Closed.")
        data += chunk
    return data

def send(txt:bytes, byte_length:int, conn:socket.socket):
    conn.sendall(len(txt).to_bytes(byte_length, "big") + txt)

def recieve(len_length:int, conn:socket.socket) -> bytes:
    txt_len:int = int.from_bytes(recv_exact(conn, len_length), "big")
    txt = recv_exact(conn, txt_len)
    return txt