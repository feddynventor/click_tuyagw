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

## [Tuya Base API](https://pypi.org/project/tinytuya/)
DPs e Metodi base
