## Gateway software
### OpenWrt
Usa `opkg` da Shell per l'installazione
https://downloads.openwrt.org/releases/19.07.8/packages/*/packages
- python3-base
- python3-setuptools
### Manual install
- Flask: https://github.com/pallets/flask/archive/refs/tags/2.0.1.tar.gz
- Flask-CORS: https://github.com/corydolphin/flask-cors/archive/refs/tags/3.0.10.tar.gz
- MultiPing: https://github.com/romana/multi-ping/archive/refs/tags/1.1.2.tar.gz
- pyaes: https://github.com/ricmoo/pyaes/archive/refs/tags/v1.6.1.tar.gz
- TinyDB: https://github.com/msiemens/tinydb/archive/refs/tags/v4.5.1.tar.gz
- TinyTuya: https://github.com/jasonacox/tinytuya/archive/refs/tags/v1.2.8.tar.gz

## Configuration
### Smart Life APK: https://www.apkmirror.com/wp-content/uploads/2019/10/5d9b418fbafa8/com.tuya.smartlife_3.12.6-109_minAPI16(arm64-v8a,armeabi-v7a)(nodpi)_apkmirror.com.apk?verify=1630340904-fa8cFIuDWT11Ns8qNCPfpz-8jyVns39bWIrWPagWQsY
### Tuya Private Keys
`cp list-app.js tuya-cli/node_modules/@tuyapi/cli/lib/list-app.js`
`node tuya-cli/node_modules/@tuyapi/cli/cli.js`
Risposta:
```
Devices(s):
[ { name: 'giftwhole（rgb）',
    id: 'bf957f7112e75c1cedxeuw',
    key: '1016d5554017e8a4' } ]
```

# Tuya DPs - v. 3.1
**Version 3.1 - Plug or Switch Type**
DP ID	Function Point	Type	Range	Units
1	Switch	bool	True/False	
2	Countdown?	integer	0-86400	s
4	Current	integer	0-30000	mA
5	Power	integer	0-50000	W
6	Voltage	integer	0-5000	V
**Version 3.1 - Light Type (RGB)**
DP ID	Function Point	Type	Range	Units
1	Switch	bool	True/False	
2	Mode	enum	white,colour,scene,music	
3	Bright	integer	10-1000*	
4	Color Temp	integer	0-1000*	
5	Color	hexstring	r:0-255,g:0-255,b:0-255,h:0-360,s:0-255,v:0-255	rgb+hsv

# Tuya DPs - v. 3.3
**Version 3.3 - Plug, Switch, Power Strip Type**
DP ID	Function Point	Type	Range	Units
1	Switch 1	bool	True/False	
2	Switch 2	bool	True/False	
3	Switch 3	bool	True/False	
4	Switch 4	bool	True/False	
5	Switch 5	bool	True/False	
6	Switch 6	bool	True/False	
7	Switch 7/usb	bool	True/False	
9	Countdown 1	integer	0-86400	s
10	Countdown 2	integer	0-86400	s
11	Countdown 3	integer	0-86400	s
12	Countdown 4	integer	0-86400	s
13	Countdown 5	integer	0-86400	s
14	Countdown 6	integer	0-86400	s
15	Countdown 7	integer	0-86400	s
17	Add Electricity	integer	0-50000	kwh
18	Current	integer	0-30000	mA
19	Power	integer	0-50000	W
20	Voltage	integer	0-5000	V
21	Test Bit	integer	0-5	n/a
22	Voltage coe	integer	0-1000000	
23	Current coe	integer	0-1000000	
24	Power coe	integer	0-1000000	
25	Electricity coe	integer	0-1000000	
26	Fault	fault	ov_cr	
**Version 3.3 - Dimmer Switch**
DP ID	Function Point	Type	Range	Units
1	Switch	bool	True/False	
2	Brightness	integer	10-1000*	
3	Minimum of Brightness	integer	10-1000*	
4	Type of light source1	enum	LED,incandescent,halogen	
5	Mode	enum	white	
**Version 3.3 - Light Type (RGB)**
DP ID	Function Point	Type	Range	Units
20	Switch	bool	True/False	
21	Mode	enum	white,colour,scene,music	
22	Bright	integer	10-1000*	
23	Color Temp	integer	0-1000	
24	Color	hexstring	h:0-360,s:0-1000,v:0-1000	hsv
25	Scene	string	n/a	
26	Left time	integer	0-86400	s
27	Music	string	n/a	
28	Debugger	string	n/a	
29	Debug	string	n/a	
**Version 3.3 - Automated Curtain Type**
DP ID	Function Point	Type	Range	Units
1	Curtain Switch 1	enum	open, stop, close, continue	
2	Percent control 1	integer	0-100	%
3	Accurate Calibration 1	enum	start, end	
4	Curtain Switch 2	enum	open, stop, close, continue	
5	Percent control 2	integer	0-100	
6	Accurate Calibration 2	enum	start, end	
8	Motor Steer 1	enum	forward, back	
9	Motor steer 2	enum	forward, back	
10	Quick Calibration 1	integer	1-180	s
11	Quick Calibration 2	integer	1-180	s
12	Motor Mode 1	enum	strong_power, dry_contact	
13	Motor Mode 2	enum	strong_power, dry_contact	
14	Light mode	enum	relay, pos, none	
**Version 3.3 - Fan Switch Type**
DP ID	Function Point	Type	Range	Units
1	Fan switch	bool	True/False	n/a
2	Fan countdown	integer	0-86400	s
3	Fan speed	enum	level_1, level_2, level_3, level_4, level_5	
4	Fan speed	integer	1-100	%
5	Fan light switch	bool	True/False	
6	Brightness integer	integer	10-1000	
7	Fan light countdown	integer	0-86400	
8	Minimum brightness	integer	10-1000	
9	Maximum brightness	integer	10-1000	
10	Mode	enum	white	
11	Power-on state setting	enum	off, on, memory	
12	Indicator status setting	enum	none, relay, pos	
13	Backlight switch	bool	True/False	
**Version 3.3 - Sensor Type**
`Important Note: Battery-powered Tuya sensors are usually designed to stay in sleep mode until a state change (eg.open or close alert). This means you will not be able to poll these devices except in the brief moment they awake, connect to the WiFi and send their state update payload the the Tuya Cloud. Keep in mind that if you manage to poll the device enough to keep it awake, you will likely quickly drain the battery.`

DP ID	Function Point	Type	Range	Units
1	Door Sensor	bool	True/False	
2	Battery level state	enum	low, middle, high	
3	Battery level	integer	0-100	%
4	Temper alarm	bool	True/False	
5	Flooding Detection State	enum	alarm, normal	
6	Luminance detection state	enum	low, middle, high, strong	
7	Current Luminance	integer	0-100	%
8	Current Temperature	integer	400-2000	
9	Current Humidity	integer	0-100	%
10	Shake State	enum	normal, vibration, drop, tilt	
11	Pressure State	enum	alarm, normal	
12	PIR state	enum	pir, none	
13	Smoke Detection State	enum	alarm, normal	
14	Smoke value	integer	0-1000	
15	Alarm Volume	enum	low, middle, high, mute	
16	Alarm Ringtone	enum	1, 2, 3, 4, 5	
17	Alarm Time	integer	0-60	s
18	Auto-Detect	bool	True/False	
19	Auto-Detect Result	enum	checking, check_success, check_failure, others	
20	Preheat	bool	True/False	
21	Fault Alarm	fault	fault, serious_fault, sensor_fault, probe_fault, power_fault	Barrier
22	Lifecycle	bool	True/False	
23	Alarm Switch	bool	True/False	
24	Silence	bool	True/False	
25	Gas Detection State	enum	alarm, normal	
26	Detected Gas	integer	0-1000	
27	CH4 Detection State	enum	alarm, normal	
28	CH4 value	integer	0-1000	
29	Alarm state	enum	alarm_sound, alarm_light, alarm_sound_light, normal	
30	VOC Detection State	enum	alarm, normal	
31	VOC value	integer	0-999	
32	PM2.5 state	enum	alarm, normal	
33	PM2.5 value	integer	0-999	
34	CO state	enum	alarm, normal	
35	CO value	integer	0-1000	
36	CO2 Detection State	enum	alarm, normal	
37	CO2 value	integer	0-1000	
38	Formaldehyde Detection State	enum	alarm, normal	
39	CH2O value	integer	0-1000	
40	Master mode	enum	disarmed, arm, home, sos	
41	Air quality index	enum	level_1, level_2, level_3, level_4, level_5, level_6	