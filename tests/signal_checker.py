triggered = {

}


def connect_signal(signal):
    triggered[signal] = False

    def callback():
        triggered[signal] = True

    signal.connect(callback)


def connect_int_signal(signal):
    triggered[signal] = False

    def callback(value: int):
        triggered[signal] = value

    signal.connect(callback)


def disconnect_signal(signal):
    del triggered[signal]


def assert_signal_emitted(signal):
    assert triggered[signal] == True
    triggered[signal] = False


def assert_int_signal(signal, value: int):
    #print(triggered[signal])
    assert triggered[signal] == value
    triggered[signal] = False
