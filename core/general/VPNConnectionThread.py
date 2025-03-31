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

from PyQt6.QtCore import QObject, pyqtSignal
import threading
from core.general.Vpn_manager import connect_vpn

class VPNConnectionWorker(QObject):
    connection_started = pyqtSignal()
    connection_finished = pyqtSignal(str)
    connection_failed = pyqtSignal(str)

    def __init__(self, vpn_name):
        super().__init__()
        self.vpn_name = vpn_name

    def run(self):
        try:
            self.connection_started.emit()
            result = connect_vpn(self.vpn_name)
            if result == "error connecting":
                self.connection_failed.emit("error connecting")
            elif result:
                self.connection_finished.emit(self.vpn_name)
        except Exception as e:
            self.connection_failed.emit(str(e))

class VPNConnectionThread:
    def __init__(self, vpn_name):
        self.worker = VPNConnectionWorker(vpn_name)
        self.thread = threading.Thread(target=self.worker.run)

    def start(self):
        self.thread.start()

    @property
    def connection_started(self):
        return self.worker.connection_started

    @property
    def connection_finished(self):
        return self.worker.connection_finished

    @property
    def connection_failed(self):
        return self.worker.connection_failed