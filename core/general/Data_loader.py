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

import json, os

from constants.constants import VPN_INFO_PATH, USER_INFO_PATH

def load_vpn_list():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    file_path = os.path.join(project_root, VPN_INFO_PATH.lstrip("./")) # _LINUX_VPN_INFO_PATH
    with open(VPN_INFO_PATH, "r") as file:
        return json.load(file)
    
def get_dont_show_update(default=False):
    if not os.path.exists(USER_INFO_PATH): # _LINUX_USER_INFO_PATH
        return default

    try:
        with open(USER_INFO_PATH, "r") as f:  # _LINUX_USER_INFO_PATH
            data = json.load(f)
            return data.get("dont_show_update", default)
    except (json.JSONDecodeError, FileNotFoundError):
        return default
    

def get_prem_auth():
    try:
        with open(USER_INFO_PATH, 'r', encoding='utf-8') as file:  # _LINUX_USER_INFO_PATH
            data = json.load(file) 

        login = data.get("login")
        password = data.get("password")
        if login and password:
            return login, password
        else:
            print("Логин или пароль не найдены в файле.")
    except json.JSONDecodeError:
        print("Ошибка: Файл содержит некорректный JSON.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")