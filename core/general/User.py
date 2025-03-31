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

from constants.constants import USER_INFO_PATH
import secrets, os, json 

class UserIDManager:
    def __init__(self, config_path=USER_INFO_PATH):  
        self.config_path = config_path
        self.premium_data = self._load_premium_data() 

    def _load_premium_data(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as file:
                config = json.load(file)
                return {
                    "is_premium": config.get("is_premium", False),
                    "login": config.get("login"),
                    "password": config.get("password")
                }
        return {"is_premium": False, "login": None, "password": None}

    def apply_auth(self, login, password):
        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            data["login"] = login
            data["password"] = password

            with open(self.config_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"Ошибка при обновлении данных: {e}")
            return False