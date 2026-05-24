import re

import pickle

from Library import librarian

import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("0.0.0.0", 8080))

server.listen(1)

client_socket, client_address = server.accept()

print("Listening for users.....")


if client_address[0] != "127.0.0.1":
    print("This user is not of this device.")

elif client_address[0] == "127.0.0.1":

    def cont():
        while True:
            cont = input("Further?: ")
            if cont.lower() == "yes":
                return True
            elif cont.lower() == "no":
                return False
            else:
                continue

    while True:

        # if not cont():
        #    break

        length = pickle.loads(client_socket.recv(50))
        if not length:
            continue

        data = pickle.loads(client_socket.recv(length))

        pattern = r"\(([^)]+)\)"

        search = list(re.finditer(pattern, data, re.I))

        if search:
            request = search[0].group(1)
        else:
            client_socket.send(
                f"Please check your request.".encode("utf-8"))

        if request.lower() == "show":
            print(data[9:])
            if librarian.approval():
                if librarian.users:
                    for user in librarian.users:
                        if user["name"] == (search[1].group(1)):
                            librarian.show_user_books()
                            break
                        else:
                            continue
                    else:
                        message = pickle.dumps(
                            "Please sign up first to see library books.")
                        length = len(message)
                        client_socket.send(pickle.dumps("deny"))
                        # time.sleep(1)
                        client_socket.send(pickle.dumps(length))
                        # time.sleep(1)
                        client_socket.send(message)
                else:
                    message = pickle.dumps(
                        "Please sign up first to see library books.")
                    length = len(message)
                    client_socket.send(pickle.dumps("deny"))
                    # time.sleep(1)
                    client_socket.send(pickle.dumps(length))
                    # time.sleep(1)
                    client_socket.send(message)

            else:
                message = pickle.dumps(
                    "Sorry your request was disapproved.")
                length = len(message)
                client_socket.send(pickle.dumps("deny"))
                # time.sleep(1)
                client_socket.send(pickle.dumps(length))
                # time.sleep(1)
                client_socket.send(message)

        elif request.lower() == "borrow":
            title = search[2].group(1)
            user_name = search[1].group(1)
            print(data[9:])
            if librarian.approval():
                # pattern = r"\((\d+)\)"
                user_id = pickle.loads(client_socket.recv(10))
                # match = re.search(pattern, rev, re.I)
                # user_id = int(match.group(1))
                if user_id:
                    librarian.borrow_book(title, user_name, user_id)
                else:
                    message = pickle.dumps(
                        "Please signup to access library books.")
                    length = len(message)
                    client_socket.send(pickle.dumps(length))
                    # time.sleep(1)
                    client_socket.send(message)
            else:
                message = pickle.dumps(
                    "Sorry, your request was denied.")
                length = len(message)
                client_socket.send(pickle.dumps(length))
                # time.sleep(1)
                client_socket.send(message)

        elif request.lower() == "signup":
            print("A user wants to sign up")
            if librarian.approval():
                text = data[9:]
                pattern = r"(\d*[A-Za-z][A-Za-z_%&$?+]*\d*[@gmail.com]*)|\d+"
                search = list(re.finditer(pattern, text, re.I))
                if search:
                    librarian.add_user(search[0].group(1), search[1].group(
                        1), search[2].group(1), search[3].group(1))
                else:
                    client_socket.send(pickle.dumps("nr"))
                    message = pickle.dumps(
                        "Your sign up info was not received. Please try again.")
                    length = len(message)
                    client_socket.send(pickle.dumps(length))
                    # time.sleep(1)
                    client_socket.send(message)

            else:
                client_socket.send(pickle.dumps("de"))
                message = pickle.dumps(
                    "Sorry, your request was denied.")
                length = len(message)
                client_socket.send(pickle.dumps(length))
                # time.sleep(1)
                client_socket.send(message)

        elif request.lower() == "return":
            title = search[2].group(1)
            user_name = search[1].group(1)
            print(data[9:])
            if librarian.approval():
                # pattern = r"\((\d+)\)"
                # rev = client_socket.recv(10).decode("utf-8")
                # match = re.search(pattern, rev, re.I)
                user_id = pickle.loads(client_socket.recv(10))
                if user_id:
                    librarian.return_book(title, user_name, user_id)
                else:
                    message = pickle.dumps(
                        "Please signup to access library books.")
                    length = len(message)
                    client_socket.send(pickle.dumps(length))
                    # time.sleep(1)
                    client_socket.send(message)

            else:
                message = pickle.dumps(
                    "Sorry, your request was denied.")
                length = len(message)
                client_socket.send(pickle.dumps(length))
                # time.sleep(1)
                client_socket.send(message)

        else:
            continue
