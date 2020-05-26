import time
import os
import sys
import threading
import json
import subprocess
import requests
import urllib.parse
import signal


class Manager:
    def __init__(self):
        self.data = {}
        self.exit = threading.Event()
        with open("config.json") as json_file:
            self.data = json.load(json_file)
        self.url = urllib.parse.urljoin(
            self.data.get("frontendURL"), "api/get_data?show_devices=true"
        )
        self.hold = self.data["deviceHold"]
        self.allowed_devices = self.data["devices"]
        self.restart_enabled = self.data["restart"]["enabled"]
        self.restart_threshold = self.data["restart"]["threshold"]
        self.install_enabled = self.data["install"]["enabled"]
        self.install_threshold = self.data["install"]["threshold"]
        self.ipa_path = self.data["ipa"]
        self.save_screenshots = self.data["saveScreenshots"]
        self.device_action = {}

    def run(self):
        print("Start MacLessManager...")
        for sig in ("TERM", "HUP", "INT"):
            signal.signal(getattr(signal, "SIG" + sig), self.quit)

        while not self.exit.is_set():
            self.controller()
            self.exit.wait(30)

    def quit(self, signo, _frame):
        print("Interrupted by %d, shutting down" % signo)
        self.exit.set()

    def controller(self):
        devices = self.all_devices()
        if not devices:
            print("Failed to load devices (or none connected)")
            time.sleep(1)

        print("{} device connected".format(len(devices.keys())))

        status = self.device_status()
        if not status:
            print("Failed to load status")
            time.sleep(1)
        print("{} status found".format(len(status.keys())))

        for device in devices:
            name = devices[device].decode("utf-8")
            if name not in status.keys() or (
                self.allowed_devices and name not in self.allowed_devices
            ):
                continue
            # Respect the last action so devices have enough time to start working
            last_action = self.device_action.get(name, 0)
            if (self.current_time() - last_action) <= self.hold:
                print("DEBUG: need to wait longer before acting on {}".format(name))
                continue
            # Save device screenshot
            # TODO: We should respect timeouts and not screenshot every 30sec
            if self.save_screenshots:
                self.screenshot(device, name)
            # TODO: Install and restart happen in the same run. Need to delay restart action.
            if self.install_enabled and (
                status[name] + self.install_threshold <= self.current_time()
                and os.path.isfile(self.ipa_path)
            ):
                print("Installing ipa on device {}...".format(name))
                self.install(device)
                self.device_action[name] = self.current_time()
            if self.restart_enabled and (
                status[name] + self.restart_threshold <= self.current_time()
            ):
                print("Restarting device {}...".format(name))
                self.restart(device)
                self.device_action[name] = self.current_time()

    def current_time(self):
        return int(time.time())

    def device_status(self):
        status = {}
        user = self.data.get("user")
        password = self.data.get("password")
        r = requests.get(self.url, auth=(user, password))
        if r.status_code == 200:
            json_data = r.json()["data"]
            devices = json_data["devices"]
            for d in devices:
                uuid = d["uuid"]
                seen = d["last_seen"]
                status[uuid] = seen
        return status

    def device_ids(self) -> list:
        cmd = ["idevice_id", "--list"]
        run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = run.communicate()
        output = output.decode("ascii").split("\n")
        if not output:
            data = []
        else:
            data = list(filter(None, output))
        return data

    def all_devices(self) -> dict:
        devices = {}
        uuids = self.device_ids()
        for uuid in uuids:
            cmd = ["idevicename", "--udid", str(uuid)]
            run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = run.communicate()
            devices[uuid] = output.strip()
        return devices

    def screenshot(self, uuid: str, name: str):
        cmd = ["idevicescreenshot", "--udid", uuid, "{}.png".format(name)]
        run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = run.communicate()
        if "Screenshot saved to" not in str(output):
            print("Error taking screenshot on {} - {}".format(name, output.strip()))

    def restart(self, uuid: str):
        cmd = ["idevicediagnostics", "restart", "--udid", uuid]
        run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = run.communicate()
        if err:
            print(err)

    def install(self, uuid: str):
        ipa = self.ipa_path
        cmd = ["ios-deploy", "--bundle", ipa, "--id", uuid]
        run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = run.communicate()
        if err:
            print(err)


if __name__ == "__main__":
    task = Manager()
    task.run()
