# tetrapol-kit (Fork)

**A fork of [airphel/tetrapol-kit-2023](https://github.com/airphel/tetrapol-kit-2023)**

The intention is to create scientific and research tool for analysis of
TETRAPOL radio networks. The project is under heavy (but slow) development,
there is no stable release yet.

With this tools You should be able:
  - find and identify base stations
  - receive and demodulate TETRAPOL transmissions
  - analyse traffic data
  - send crafted traffic

## Dependecie
  Install libraries and development files for:
```bash
sudo apt install libglib2.0-dev libjson-c-dev libcmocka-dev cmake libusb-1.0-0-dev
```
  rtl-sdr
https://osmocom.org/projects/rtl-sdr/wiki/Rtl-sdr
  OsmoSDR
https://osmocom.org/projects/gr-osmosdr/wiki/GrOsmoSDR 

### Know issues

osmocom source in gnu radio :
Install or compile rtl-sdr before OsmoSDR

modprob :
vim /etc/modprobe.d/librtlsdr.conf 
```bash
blacklist dvb_usb_rtl28xxu
blacklist rtl2832
blacklist rtl2830
```

## Installation

Build:

```bash
mkdir build
cd build
cmake ..
make
```
## Usage
  Open ../demod/tetrapol_demod.grc in gnuradio
  Modify frequency or via QT when running it

  Open new terminal
  ```bash
  ./build/apps/tetrapol_dump -t TCH -r 42000 1> /tmp/tch.json
  ```

## Todo

- Rework log dump
- headless multichannel demod

## Reference

https://github.com/airphel/tetrapol-kit-2023/wiki
https://brmlab.cz/gitweb/?p=tetrapol-kit.git
https://github.com/aeburriel/tetrapol-kit
https://github.com/jenda122/tetrapol-kit
https://github.com/jswo/tetrapol-kit
