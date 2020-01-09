import ujson

class settings():
    def __init__(self):
        f = open("settings.json", "r")
        settings_str = f.read()
        self.settings_obj = ujson.loads(settings_str)
        f.close()
        return None

    def get_settings(self):
        return self.settings_obj

