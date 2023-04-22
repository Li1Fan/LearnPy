from pynput import keyboard

keyCtrl = keyboard.Controller()


def home():
    print('<home> pressed')
    # 实现Ctrl Home组合按键
    # with keyCtrl.pressed(Key.ctrl):
    keyCtrl.press(keyboard.Key.home)
    keyCtrl.release(keyboard.Key.home)
    return False


def end():
    print('<end> pressed')
    # 实现Ctrl Home组合按键
    # with keyCtrl.pressed(Key.ctrl):
    keyCtrl.press(keyboard.Key.end)
    keyCtrl.release(keyboard.Key.end)
    return False


def esc_shift():
    print('<esc>+<shift> pressed')
    raise Exception


with keyboard.GlobalHotKeys({
    '<esc>+<shift>': esc_shift,
    '<ctrl>+[': home,
    '<ctrl>+]': end}
) as h:
    h.join()

# h = keyboard.GlobalHotKeys({
#     '<esc>+<shift>': esc_shift,
#     '<ctrl>+[': home,
#     '<ctrl>+]': end}
# )
#
# h.setDaemon(False)
# h.start()
