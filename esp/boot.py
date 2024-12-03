from machine import Pin

# 释放所有GPIO, 断电重上电不再失控
def release_all_GPIO():
    for i in range(0, 22):
        try:
            GND = Pin(i, Pin.OUT, value=0)
            print(f"releasing gpio {i}")
        except:
            print(f"skip gpio {i}")
            continue
release_all_GPIO()
