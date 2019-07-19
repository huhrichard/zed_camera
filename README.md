# zed_camera

Testing code for running zed camera

Prerequisite:
installed pyzed:
https://github.com/stereolabs/zed-python-api

and also opencv

Example of usage:
```
python test_multi.py 0
```
The last argument stands for the camera id, if you have N camera(s) are connected, you can use integer with range from 0 to N-1 to call corresponding camera. 

IF the fps is normal as setting:
  The fps will print once per frame.
ELSE
  The fps will print once per hour
