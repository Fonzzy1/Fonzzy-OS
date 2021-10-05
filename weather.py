import requests as r
import readchar
w = r.get( "http://wttr.in/bentleigh")
print(w.text)
wait = readchar.readkey()
