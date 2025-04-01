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
from ui.main import main
import sys, os

def is_linux():
    return sys.platform.startswith('linux')

def is_windows():
    return sys.platform.startswith('win32') or sys.platform.startswith('cygwin')

def is_root():
    if is_linux():
        return os.geteuid() == 0
    elif is_windows():
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    return True  


if __name__ == "__main__":
    if not is_root():
        if is_linux():
            print("Ошибка: Для корректной работы программа должна быть запущена с правами администратора.")
            print("Пожалуйста, запустите программу с помощью sudo")
        elif is_windows():
            print("Ошибка: Программа должна быть запущена от имени администратора.")
            print("Пожалуйста, запустите программу с правами администратора")
        else:
            print("Ошибка: Программа требует прав администратора")
        sys.exit(1)

    main()