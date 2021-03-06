# person_detection_viewer
Image viewer for the [person detection example](https://github.com/kitsook/tflite-micro-sparkfun-edge-examples/tree/main/examples/person_detection) of
[SparkFun Edge Development Board](https://www.sparkfun.com/products/15170).

The person detection example can be modified to print out hexadeciaml dump of the images. This viewer can read them from serial port and display them.

![image](https://user-images.githubusercontent.com/13360325/150475786-c8391c70-a9cc-4c76-8131-99c9b9aba0ae.png)
&nbsp;&nbsp;
![image](https://user-images.githubusercontent.com/13360325/150476541-83b165a8-e9bf-4e48-a65b-d726a87daec0.png)


## Modify the example
- Uncomment the line to [enable the hex dump](https://github.com/kitsook/tflite-micro-sparkfun-edge-examples/blob/2ffe1fab709a7fd742404a05c9b144f346731d3c/examples/person_detection/image_provider.cc#L27)
```
#define DEMO_HM01B0_FRAMEBUFFER_DUMP_ENABLE
```
- Modify the debug output to [skip the printing of address](https://github.com/kitsook/tflite-micro-sparkfun-edge-examples/blob/2ffe1fab709a7fd742404a05c9b144f346731d3c/examples/person_detection/himax_driver/HM01B0_debug.c#L31)
```
am_util_stdio_printf("\r\n");
```

## Quickstart
```
git clone https://github.com/kitsook/person_detection_viewer.git
cd person_detection_viewer
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python3 main.py
```
Edit `main.py` to change the `SERIAL_PORT` as appropriate.
