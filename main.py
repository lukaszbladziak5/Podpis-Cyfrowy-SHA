import rsa
import sys
import hashlib
import PySimpleGUI as gui
#import qtrng

"""Set color of GUI theme."""
gui.theme('BlueMono')

"""Create layout, display and send message"""
layout = [[gui.Text('Podaj swoją wiadomość:')],
            [gui.InputText()],
            [gui.Submit(), gui.Cancel()]]
window = gui.Window('Szyfrowanie wiadomości', layout)
event, values = window.read()
window.close()
message = values[0]

"""Calculate and display SHA value for sent message"""
messageSHA = hashlib.sha3_224(message.encode("utf-8")).hexdigest().encode("utf-8")
gui.popup('Obliczona wartość SHA z wiadomości: \n' + messageSHA.decode())

"""Generate public and private keys"""
(public_key, private_key) = rsa.newkeys(2048)

"""Display public key"""
gui.popup('Klucz publiczny: \n', public_key)

"""Encrypt SHA value by public key"""
encodedSHA = rsa.encrypt(messageSHA, public_key)
gui.popup('Zaszyfrowana wiadomość: \n', encodedSHA)

"""Create layout for private key change"""
layout = [[gui.Text('Czy chcesz zmodyfikować klucz prywatny? \n Jeżeli nie, zostaw go bez zmian i kliknij przycisk "Submit". ')],
                 [gui.InputText(default_text=str(private_key.n))],
                 [gui.Submit(), gui.Cancel()]]
window = gui.Window('Modyfikacja klucza prywatnego', layout)
event, values = window.read()
window.close()

"""Check private key (if incorrect stop system)"""
if values[0] == str(private_key.n):
  gui.popup('Klucz prywatny jest poprawny! \n Wiadomość zostanie odszyfrowana.')
else:
  gui.popup('Klucz prywatny jest nieprawidłowy. \n Nastąpi zakończenie programu.')
  sys.exit()

"""Decrypt SHA value by private key"""
decodedSHA = rsa.decrypt(encodedSHA, private_key)

"""Create layout for received message change"""
layout = [[gui.Text('Czy chcesz zmodyfikować otrzymaną wiadomość? \n Jeżeli nie, zostaw ją bez zmian i kliknij przycisk "Submit".')],
                 [gui.InputText(default_text = message)],
                 [gui.Submit(), gui.Cancel()]]
window = gui.Window('Modyfikacja otrzymanej wiadomości', layout)
event, values = window.read()
window.close()

"""Check SHA correction and finish work"""
receivedMessageSHA = hashlib.sha3_224(values[0].encode("utf-8")).hexdigest().encode("utf-8")
if(receivedMessageSHA == decodedSHA):
  gui.popup("SHA są zgodne! \n Nastąpi zakończenie programu.")
else:
  gui.popup("SHA są niezgodne! \n Nastąpi zakończenie programu.")
