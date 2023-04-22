from pynput.keyboard import Key, Listener, Controller

keyCtrl = Controller()


def on_press(key):
    print(key.__dict__)
    # 当按下esc，结束监听
    if key == Key.esc:
        # 实现Ctrl Home组合按键
        with keyCtrl.pressed(Key.ctrl):
            keyCtrl.press(Key.home)
            keyCtrl.release(Key.home)
        return False
    try:
        if key.char == '[':
            print(111)
            return
    except AttributeError:
        pass
    print(f"你按下了{key}键")


def on_release(key):
    print(f"你松开了{key}键")


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
