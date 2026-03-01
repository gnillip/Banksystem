import json, socket, mod

print("[*] Starting Server")

data_check = ["username", "password", "groups", "lock"]
COMMANDS = {
    "admin": [
        "adduser",
        "deluser",
        "alluser",
        "getuser",
        "chuser"
    ],
    "general": [
        "check",
        "change",
        "pay",
        "exit"
    ]
}


ENV:dict = mod.load_ENV()
print("[*] Loaded ENV")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", ENV["PORT"]))
server.listen()

print("[*] Waiting for incomming connection...")
while True:
    SAM:dict = mod.load("SAM.json", True)
    conn, addr = server.accept()
    print(f"Connection from: {addr}")

    username:str = mod.recieve(8, conn).decode()
    password:str = mod.recieve(8, conn).decode()

    if username not in SAM:
        conn.close()
        print(f"[*] not existing User (IP:{addr[0]})")
        continue

    if SAM[username]["password"] != password:
        conn.close()
        print(f"[*] wrong password for User {username} (IP:{addr[0]})")
        continue

    if SAM[username]["lock"]:
        conn.close()
        print(f"[*] user {username} is locked (IP:{addr[0]})")
        continue

    if "admins" in SAM[username]["groups"]:
        mod.send(json.dumps(COMMANDS).encode(), 8, conn)
    else:
        mod.send(json.dumps(COMMANDS["general"]).encode(), 8, conn)
    while True:
        cmd = mod.recieve(8, conn).decode()

        found = 0
        for key, value in COMMANDS.items():
            if key == "admin" and "admins" not in SAM[username]["groups"]:
                continue
            if cmd in value:
                found += 1
        
        if found <= 0:
            mod.send(b"Command not found.", 8, conn)
            continue

        if "admins" in SAM[username]["groups"]:

            if cmd == "adduser":
                data:dict = json.loads( mod.recieve(8, conn).decode() )

                # data = {"username":<username>, "password":<password-hash>, "groups":[<list-of-groups>], locked:<bool>}
                
                alert = False
                for element in data_check:
                    if element not in data:
                        mod.send(b"Not enough data.", 8, conn)
                        alert = True
                        break
                if alert:
                    continue

                if data["username"] in SAM:
                    mod.send(b"This User already exists!", 8, conn)
                    continue

                SAM[data["username"]] = {
                    "password":data["password"],
                    "groups":data["groups"],
                    "lock":data["lock"]
                }
                mod.write("SAM.json", SAM)

                BANK:dict = mod.load("BANK.json", True)
                BANK[data["username"]] = 100
                mod.write("BANK.json", BANK)
            
            if cmd == "deluser":
                data = mod.recieve(8, conn).decode()

                if data in SAM:
                    SAM.pop(data)
                    mod.write("SAM.json", SAM)
                    BANK = mod.load("BANK.json", True)
                    BANK.pop(data)
                    mod.write("BANK.json", BANK)
                else:
                    mod.send(b"This User already doesn't exist.", 8, conn)
                    continue
            
            if cmd == "alluser":
                mod.send( json.dumps(SAM).encode(), 8, conn )
                continue

            if cmd == "getuser":
                data = mod.recieve(8, conn).decode()

                if data not in SAM:
                    mod.send(b"This user doesn't exist!", 8, conn)
                    continue

                tmp = json.dumps(SAM[data])
                mod.send(tmp.encode(), 8, conn)
                continue

            if cmd == "chuser":
                data = json.loads( mod.recieve(8, conn) )

                alert = False
                for element in data_check:
                    if element not in data:
                        mod.send(b"Not enough data.", 8, conn)
                        alert = True
                        break
                if alert:
                    continue
                
                SAM[data["username"]] = {
                    "password": data["password"] or SAM[data["username"]]["password"],
                    "groups": data["groups"],
                    "lock": data["lock"]
                }
                mod.write("SAM.json", SAM)
                BANK = mod.load("BANK.json", True)
                BANK[data["username"]] = int(data["money"])
                mod.write("BANK.json", True)

        if cmd == "check":
            BANK:dict = mod.load("BANK.json", True)
            mod.send(str(BANK[username]).encode(), 8, conn)
        
        if cmd == "change":
            data = mod.recieve(8, conn).decode()
            SAM[username]["password"] = data
            mod.write("SAM.json", SAM)
        
        if cmd == "pay":
            BANK:dict = mod.load("BANK.json", True)
            data = json.loads( mod.recieve(8, conn) )
            # should be {"to":<user>, "amount":<int>}
            if "to" not in data or "amount" not in data:
                mod.send(b"Not enough data.", 8, conn)
                continue

            data["amount"] = int(data["amount"])

            if data["to"] not in SAM:
                mod.send(b"This user doesn't exist!", 8, conn)
                continue

            if data["amount"] > BANK[username]:
                mod.send(b"You have not enough Money.", 8, conn)
                continue

            if data["amount"] < 0:
                mod.send(b"You can't pay negative amounts!", 8, conn)
                continue

            BANK[username] -= int(data["amount"])
            BANK[data["to"]] += int(data["amount"])
            mod.write("BANK.json", BANK)
        
        if cmd == "exit":
            conn.close()
            break
        
        mod.send(b"Command executed.", 8, conn)
        print(f"Command {cmd} executed. (IP:{addr[0]}, user:{username})")