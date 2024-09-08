# Patient Interface of Mobile Medical Drone
Here is right directory of each file.

run the following commands first:
```bash
cd ~
mkdir drone
```


/home/pi/drone/ : move all files to this directory except 이동진료소.desktop

/home/pi/Desktop/ : 이동진료소.desktop

## Required library
### pigpio
This library allow servos to minimize jittering.
Run the following commands to install:

```bash
$wget https://github.com/joan2937/pigpio/archive/master.zip
$unzip master.zip
$cd pigpio-master
$make
$sudo make install
```

