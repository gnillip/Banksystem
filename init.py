import json, hashlib, getpass

print("Initializing...")

ADMIN = input("ADMIN-username: ")
PASW = getpass.getpass("ADMIN-pasword: ", echo_char="*")
SAM = {
    ADMIN:{
        "password": hashlib.sha512(PASW.encode()).hexdigest(),
        "groups": [
            "admins",
            "users"
        ],
        "lock":False
    }
}
with open("SAM.json", "w") as sam:
    json.dump(SAM, sam, indent=4)

with open("BANK.json", "w") as bank:
    json.dump({ADMIN:1000000}, bank, indent=4)

IP = input("\nIP: ")
PORT = input("PORT: ")

DATA = {
    "IP": IP,
    "PORT": int(PORT)
}

with open("env.json", "w") as f:
    json.dump(DATA, f, indent=4)