import requests
import time
import datetime
import threading

class IPChecker:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(IPChecker, cls).__new__(cls)
        return cls._instance

    def __init__(self, interval=600, port=None):
        if not hasattr(self, 'initialized'):  # Prevent reinitialization
            self.interval = interval
            self.port = port
            self.last_ip = None
            self.running = False
            self.thread = None
            self.on_ip_change = None
            self.on_ip_same = None
            self.initialized = True

    def get_public_ip(self):
        return requests.get('https://api.ipify.org').text

    def set_on_ip_change(self, callback):
        self.on_ip_change = callback
        return self

    def set_on_ip_same(self, callback):
        self.on_ip_same = callback
        return self

    def check_ip_change(self):
        while self.running:
            current_ip = self.get_public_ip()
            if current_ip != self.last_ip:
                print(f"[{datetime.datetime.now()}] ==========> IP Changed: {current_ip}")
                if self.on_ip_change:
                    self.on_ip_change(f"http://{current_ip}:{self.port}")
                self.last_ip = current_ip
            else:
                print(f"[{datetime.datetime.now()}] Same IP: {current_ip}")
                if self.on_ip_same:
                    self.on_ip_same(f"http://{current_ip}:{self.port}")
            time.sleep(self.interval)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.check_ip_change)
            self.thread.start()
            print("IP Checker started.")
        else:
            print("IP Checker is already running.")

    def stop(self):
        if self.running:
            self.running = False
            self.thread.join()
            print("IP Checker stopped.")
        else:
            print("IP Checker is not running.")

    def set_interval(self, interval):
        self.interval = interval
        print(f"Interval set to {self.interval} seconds.")

    def set_port(self, port):
        self.port = port
        print(f"Port set to {self.port}.")