# NoAD VPN - the program uses ovpn to connect to vpn and also automatically updates authorization data for public configs
# Copyright (C) 2025 Evgeniy Light
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from constants.constants import CHECK_UPDATE_URL, USER_INFO_PATH

import requests, json, os
from typing import Optional, Dict

class AppUpdater:
    def __init__(self, current_version: str, server_url: str = CHECK_UPDATE_URL):
        self.current_version = current_version
        self.server_url = server_url

    def check_for_updates(self) -> Optional[Dict[str, str]]:
        try:
            payload = {"current_version": self.current_version}
            response = requests.post(self.server_url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "no_update":
                    print("У вас актуальная версия приложения.")
                    return None
                else:
                    return data 
            else:
                print(f"Ошибка сервера: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при проверке обновлений: {e}")
            return None

    def save_dont_show_flag(self, dont_show_checkbox):
        if os.path.exists(USER_INFO_PATH): # _LINUX_USER_INFO_PATH
            try:
                with open(USER_INFO_PATH, "r") as f: # _LINUX_USER_INFO_PATH
                    data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                data = {}
        else:
            data = {}
        data["dont_show_update"] = dont_show_checkbox

        with open(USER_INFO_PATH, "w") as f: # _LINUX_USER_INFO_PATH
            json.dump(data, f, indent=4)

    @staticmethod
    def should_show_update():
        try:
            with open(USER_INFO_PATH, "r") as f: # _LINUX_USER_INFO_PATH
                data = json.load(f)
                return not data.get("dont_show_update", False)
        except (FileNotFoundError, json.JSONDecodeError):
            return True