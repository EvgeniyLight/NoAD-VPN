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

import os, subprocess, time
from datetime import datetime
from constants.constants import CONFIG_DIR_PATH, OVPN_PATH

# CONFIG_DIR = CONFIG_DIR_PATH # for build deb
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
OVPN_PATH = os.path.join(BASE_DIR, OVPN_PATH) # for develop
CONFIG_DIR =  os.path.join(BASE_DIR, "../." + CONFIG_DIR_PATH) # for develop

def create_auth_file(login, password):
    auth_file_path = os.path.join(CONFIG_DIR, "auth.txt")
    try:
        if os.path.exists(auth_file_path):
            os.remove(auth_file_path)
        with open(auth_file_path, "w") as file:
            file.write(f"{login}\n{password}")
        return auth_file_path
    except Exception as e:
        raise RuntimeError(f"Не удалось создать файл auth.txt: {e}")

def start_vpn(config_file, login, password, timeout=20):
    try:
        if not os.path.exists(OVPN_PATH):
            raise FileNotFoundError("Бинарник openvpn не найден в bin")
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Конфиг {config_file} не найден")
        
        os.chmod(OVPN_PATH, 0o755)
        auth_file_path = create_auth_file(login, password)

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Запускаю OpenVPN...")
        process = subprocess.Popen(
            [
                "sudo",
                OVPN_PATH,
                "--config", config_file,
                "--auth-user-pass", auth_file_path,
                "--verb", "4",
                "--data-ciphers", "AES-256-GCM:AES-128-GCM:CHACHA20-POLY1305:AES-128-CBC"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] PID: {process.pid}")

        start_time = time.time()
        while True:
            line = process.stdout.readline().strip()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if line:
                print(f"[{current_time}] {line}")
                if "Initialization Sequence Completed" in line:
                    print(f"[{current_time}] [УСПЕХ] VPN-соединение установлено!")
                    return process
                if "ERROR: Cannot ioctl TUNSETIFF tun" in line:
                    print(f"[{current_time}] [ОШИБКА] Нет прав для создания TUN интерфейса. Запустите с sudo.")
                    return None
            if process.poll() is not None:
                print(f"[{current_time}] Процесс завершился с кодом {process.returncode}")
                return None
            if time.time() - start_time > timeout:
                process.terminate()
                print(f"[{current_time}] [ОШИБКА] Тайм-аут ({timeout} сек): сервер не отвечает")
                return None

    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ошибка: {e}")
        return None

def ovpn_start(config_file, login, password):
    print(f"Использую конфиг: {os.path.basename(config_file)}")
    print("Запускаю VPN-соединение...")
    return start_vpn(config_file, login, password, timeout=20)  
