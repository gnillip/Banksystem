import json, socket, mod, getpass, hashlib

print("[*] Welcome!")
ENV:dict = mod.load_ENV()
print("[*] loaded ENV")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ENV["IP"], ENV["PORT"]))
print("[*] Created Connection.\n")

USERNAME = input("Username: ")
PASSWORD = getpass.getpass("Password: ", echo_char="*")
PASSWORD_hash = hashlib.sha512(PASSWORD.encode()).hexdigest()

mod.send(USERNAME.encode(), 8, client)
mod.send(PASSWORD_hash.encode(), 8, client)

COMMANDS:dict = json.loads( mod.recieve(8, client) )

while True:
    print(f"\n\nCOMMANDS: {COMMANDS}")
    cmd = input("-----\nYour command: ")
    mod.send(cmd.encode(), 8, client)

    if cmd == "adduser":
        data = {
            "username":input("Username of the new User: "),
            "password":hashlib.sha512(input("Password of the new User: ").encode()).hexdigest(),
            "groups":input("Groups (seperated with comma): ").split(","),
            "lock":False if input("Lock [y]: ") else True
        }
        mod.send(json.dumps(data).encode(), 8, client)
    
    if cmd == "deluser":
        data = input("Username to delete: ")
        mod.send(data.encode(), 8, client)
    
    if cmd == "alluser":
        pass

    if cmd == "getuser":
        data = input("Username of the user you want some Info about: ")
        mod.send(data.encode(), 8, client)
    
    if cmd == "chuser":
        data = {
            "username":input("Username of the changing User: "),
            "password":input("New Password (empty for old one): "),
            "groups":input("new groups: "),
            "lock":True if input("lock [y]: ") else False,
            "money":int(input("Amount money: "))
        }
        mod.send(json.dumps(data).encode(), 8, client)
    
    if cmd == "check":
        pass

    if cmd == "change":
        data = hashlib.sha512(input("New Password: ").encode()).hexdigest()
        mod.send(data.encode(), 8, client)
    
    if cmd == "pay":
        data = {
            "to":input("To: "),
            "amount":int(input("Amount: "))
        }
        mod.send(json.dumps(data).encode(), 8, client)
    
    if cmd == "exit":
        client.close()
        break
    
    ans = mod.recieve(8, client)
    print(f"ans: {ans}")