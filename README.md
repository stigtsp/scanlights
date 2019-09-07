Scanlight is a NodeMCU/ESP8266 with micropython that maps tcp ports to individual neopixel lights. Made at cccamp19 by sgo and oklien, converting automated port scans into tent decorations.

## TODO
- [ ] Create fancy animations, animation loop maybe, use select?
- [ ] It's a bit unstable with many incoming connections. Fix up socket code a bit.
- [ ] Try ESP32, maybe more stable.

## Setup
1. Flash micropython to an ESP8266
2. Wire up your neopixel compatible rgb led strip(s).
3. Upload main.py to the ESP8266 by running `make`
4. Reboot the device
5. Watch the blinkenlights

## Wiring of neopixels:
- data = D3(NodeMCU) which is Pin 0 in micropython
- red = Vin or 3v3
- gnd = gnd

## Notes
- Connections to port 7331 blanks the lights.
- Agressive nmap scans will likely crash the microcontroller.

## Testing the lights

nmap:

```
nmap -Pn -v -T2 -p 21,22,23,25,53,80,110,111,135,139,143,443,445,554,587,593,625,631,636,646,787,808,873,902,990,993,995,1723,3306,3389,5900,8080,8443,8888,9000,9001,9090,9100,9102,2121,2161,2301,2383,2401,2601,2717,2869,2967,3000,9999 $IPADDRESS
```

or

pushing hex color values to the ports:

```
while true; do color=$(perl -e 'printf "%08X\\n", rand(0xffffffff);'); for i in $(perl -le '$,=" ";print join " ", 21,22,23,25,53,80,110,111,135,139,143,443,445,554,587,593,625,631,636,646,787,808,873,902,990,993,995,1723,3306,3389,5900,8080,8443,8888,9000,9001,9090,9100,9102,2121,2161,2301,2383,2401,2601,2717,2869,2967,3000;'); do echo -e $color | nc -n -w1 -v $IPADDRESS $i ;sleep 20; done; done
```
