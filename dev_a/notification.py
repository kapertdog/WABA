import win10toast

n = win10toast.ToastNotifier()


def notify(title="", msg="", icon_path=None, duration=3):
    n.show_toast(title, msg, icon_path, duration, True)
