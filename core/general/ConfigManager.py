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

from constants.constants import VPN_INFO_PATH

import json
from datetime import datetime, timedelta
import string, random

class ConfigManager():
    def __init__(self, vpn_info_path=VPN_INFO_PATH): 
        self.vpn_info_path = vpn_info_path

    def checking_VPN_upToDate(self, selected_vpn):
        vpn_info = self.read_vpn_info(selected_vpn)
        
        vpn_uptime = vpn_info['uptime'] 
        vpn_uptime_dt = datetime.fromisoformat(vpn_uptime)
        today = datetime.today()

        if vpn_uptime_dt > today:
            return True
        elif vpn_uptime_dt <= today:
            print("Требyется обновление конфигурации.")
            return None
        
    def read_vpn_info(self, selected_vpn):
        try:
            with open(self.vpn_info_path, "r") as f:
                vpn_data = json.load(f)
                for i in vpn_data:
                    if i.get("ovpn") == selected_vpn:
                        return i
                return None

        except Exception as e:
            print(f"Ошибка при чтении файла {self.vpn_info_path}: {e}")
            return None
        
    def generate_random_string(self, length):
        characters = string.ascii_letters  
        return ''.join(random.choice(characters) for _ in range(length))

    def update_vpn_info(self, selected_vpn, login, password):
        try:
            with open(self.vpn_info_path, "r") as f:
                vpn_data = json.load(f)

            for i in vpn_data:
                if i.get("ovpn") == selected_vpn:
                    ttl = i['ttl']
                    today = datetime.now()
                    future_date = today + timedelta(days=ttl)
                    new_uptime = future_date.strftime("%Y-%m-%d")
        
                    i["login"] = login + "-vpnjantit.com"
                    i["ps"] = password
                    i["uptime"] = new_uptime
                    break  
            else:
                print(f"Запись с ovpn={selected_vpn} не найдена.")
                return

            with open(self.vpn_info_path, "w") as f:
                json.dump(vpn_data, f, indent=4)
            print(f"Данные успешно сохранены в файл {self.vpn_info_path}.")

        except Exception as e:
            print(f"Ошибка при обновлении файла {self.vpn_info_path}: {e}")
