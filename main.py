import network
import time
import machine
import neopixel
import urandom
from machine import Timer

ssid = "hackeriet.no"
psk = "hackeriet.no"

print("Connecting to wifi: " + ssid)  

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid,psk)

np = neopixel.NeoPixel(machine.Pin(0), 50)


while not station.isconnected():
    machine.idle()

print("Connected: " + str(station.ifconfig()))

ap_if = network.WLAN(network.AP_IF)
if ap_if.active(): ap_if.active(False)






import usocket, uselect
ports   = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,554,587,593,625,631,636,646,787,808,873,902,990, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443, 8888, 9000, 9001, 9090, 9100, 9102, 2121, 2161, 2301, 2383,2401,2601,2717,2869,2967,3000,9999 ]
sockets = []
poller = uselect.poll()
for p in ports:
    addr = usocket.getaddrinfo('0.0.0.0', p)[0][-1]
    s = usocket.socket()
    s.settimeout(0.1)
    s.bind(addr)
    s.listen(4)
    sockets.append(s)
    poller.register(s, uselect.POLLIN)
    print("binding to port " + str(p))

clearaddr = usocket.getaddrinfo('0.0.0.0', 7331)[0][-1]
clear_s = usocket.socket()
clear_s.bind(clearaddr)
clear_s.listen(4)
sockets.append(clear_s)
poller.register(clear_s, uselect.POLLIN)

import colorsys

def hex2rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))


def slideto(to):
    n=np.n
    for i in range(to):
        for j in range(to):
            np[j] = (0, 0, 0)
        if (i // n) % 2 == 0:
            np[i % n] = colorsys.hsv_to_rgb(0.5, 1/n, 1)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(1)



def randint(min, max):
    span = max - min + 1
    div = 0x3fffffff // span
    offset = urandom.getrandbits(30) // div
    val = min + offset
    return val

def hit(i, r, g, b):
    n = np.n
    np[i] = (r,g,b)
    np.write()

def dim(i):
    n = np.n
    for j in range(n):
        val = i
        d = np[j]
        np[j] = (int(d[0] * (val/255)), int(d[1] * (val/255)),  int(d[2] * (val/255)))

def tick(t=False):
    dim(250)

def clear():
    n=np.n
    for j in range(n):
        val = i
        d = np[j]
        np[j] = (0,0,0)
    for j in range(n):
        val = i
        d = np[j]
        np[j] = (0,255,0)
    for j in range(n):
        val = i
        d = np[j]
        np[j] = (0,0,0)
    np.write()


timer = Timer(-1)
print("Number of ports: " + str(len(ports)))

# import machine;machine.reset()

while True:
    for event in poller.ipoll (-1):
        cl, addr = event[0].accept()
        data = None
        try:
            data = cl.recv(6)
        except:
            print("Timed out")
        finally:
            cl.close()

        if data and len(data) == 6:
            print("data:" + str(data))
        else:
            data = None

        
        i=0
        port=None
        for s in sockets:
            if event[0] == s:
                try:
                    port = ports[i]
                except IndexError:
                    pass
                break
            i+=1
        if port:
            try:
                rgb = hex2rgb(data)
            except:
                rgb = (randint(1,255), randint(1,255), randint(1,255))
            hit(i,rgb[0],rgb[1],rgb[2])
        if event[0] == clear_s:
            clear()

        print("Port: " + str(port))



