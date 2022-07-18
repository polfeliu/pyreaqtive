triggered = {

}


def connect_signal(signal):
    triggered[signal] = True

    def callback():
        triggered[signal] = True

    signal.connect(callback)


def disconnect_signal(signal):
    del triggered[signal]


def assert_signal_emitted(signal):
    assert triggered[signal] == True
    triggered[signal] = False
