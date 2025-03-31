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

import sys, os
from datetime import datetime
from core.general.Data_loader import load_vpn_list
from core.general.Data_loader import get_prem_auth
from constants.constants import CONFIG_DIR_PATH
 
CONFIG_DIR =  CONFIG_DIR_PATH 
if sys.platform.startswith('win'):
    from core.windows.Ovpn_windows import ovpn_start
elif sys.platform.startswith('linux'):
    from core.linux.Ovpn import ovpn_start


current_process = None

def connect_vpn(ovpn_file):
    global current_process

    config_file = os.path.join(CONFIG_DIR, ovpn_file)
    
    login, ps = "", ""

    vpn_list = load_vpn_list()
    for i in vpn_list:
        if i['ovpn'] == ovpn_file:
            if i['isGold'] == 'True':
                login, ps = get_prem_auth()
            else:    
                login = i['login']
                ps = i['ps']

    current_process = ovpn_start(config_file, login, ps)
    if current_process != None:
        print(f"Подключено к {ovpn_file}")
        return "connected"
    else:
        print(f"Не удалось подключиться к {ovpn_file}")
        return "error connecting"
        
    
def disconnect_vpn():
    global current_process
    if current_process is not None and current_process.poll() is None:
        print("Отключение...")
        try:
            current_process.terminate()
            current_process.wait(timeout=5)  
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] VPN отключен")
        except Exception as e:
            print(f"Ошибка при отключении: {e}")
        finally:
            current_process = None
    else:
        print("VPN уже отключен")
