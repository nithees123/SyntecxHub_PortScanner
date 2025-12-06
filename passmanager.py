import json
import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from getpass import getpass

FILE = "vault.enc"
SALT_FILE = "salt.bin"


# -------------------------------
# KEY GENERATION FROM MASTER PASSWORD
# -------------------------------
def derive_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key


# -------------------------------
# LOAD OR CREATE SALT
# -------------------------------
def get_salt():
    if os.path.exists(SALT_FILE):
        return open(SALT_FILE, "rb").read()
    else:
        salt = os.urandom(16)
        open(SALT_FILE, "wb").write(salt)
        return salt


# -------------------------------
# LOAD VAULT
# -------------------------------
def load_vault(fernet):
    if not os.path.exists(FILE):
        return {}  # empty vault

    with open(FILE, "rb") as f:
        encrypted_data = f.read()

    try:
        decrypted = fernet.decrypt(encrypted_data)
        return json.loads(decrypted.decode())
    except:
        print("❌ Wrong master password!")
        exit()


# -------------------------------
# SAVE VAULT
# -------------------------------
def save_vault(vault, fernet):
    encrypted = fernet.encrypt(json.dumps(vault).encode())
    with open(FILE, "wb") as f:
        f.write(encrypted)


# -------------------------------
# PROGRAM OPTIONS
# -------------------------------
def add_password(vault):
    site = input("Website/App: ")
    username = input("Username: ")
    password = input("Password: ")

    vault[site] = {"username": username, "password": password}
    print("✔ Password added!")
    return vault


def view_all(vault):
    if not vault:
        print("Vault empty!")
        return
    for site, data in vault.items():
        print(f"{site}: {data['username']} / {data['password']}")


def search(vault):
    key = input("Search website: ")
    if key in vault:
        print(vault[key])
    else:
        print("Not found!")


def delete(vault):
    key = input("Delete entry for website: ")
    if key in vault:
        del vault[key]
        print("✔ Deleted!")
    else:
        print("Not found!")
    return vault


# -------------------------------
# MAIN LOGIC
# -------------------------------
def main():
    print("=== Local Password Manager ===")

    master_password = getpass("Enter master password: ")

    salt = get_salt()
    key = derive_key(master_password, salt)
    fernet = Fernet(key)

    vault = load_vault(fernet)

    while True:
        print("\n1. Add Password")
        print("2. View All")
        print("3. Search")
        print("4. Delete")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            vault = add_password(vault)
            save_vault(vault, fernet)

        elif choice == "2":
            view_all(vault)

        elif choice == "3":
            search(vault)

        elif choice == "4":
            vault = delete(vault)
            save_vault(vault, fernet)

        elif choice == "5":
            save_vault(vault, fernet)
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
