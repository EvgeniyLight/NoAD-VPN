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

import platform, subprocess, re

DNS_SERVERS = {
    "AdGuard": ["94.140.14.14", "94.140.15.15"]
}
DEFAULT_DNS = ["8.8.8.8", "8.8.4.4"]

def set_dns_windows(dns_servers):
    def run_cmd(command):
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='cp866',
                timeout=15
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
        except Exception as e:
            return False, str(e)

    try:
        success, output = run_cmd(
            'powershell "Get-NetAdapter -Physical | '
            'Where-Object {$_.Status -eq \'Up\'} | '
            'Select-Object -First 1 | '
            'Select-Object -ExpandProperty Name"'
        )
        
        if not success or not output.strip():
            return False
            
        interface_name = output.strip()
        
        commands = [
            f'netsh interface ipv4 set dnsservers name="{interface_name}" source=dhcp',
            f'netsh interface ipv4 set dnsservers name="{interface_name}" source=static addr={dns_servers[0]} primary validate=no',
        ]
        
        for i, dns in enumerate(dns_servers[1:], start=2):
            commands.append(
                f'netsh interface ipv4 add dnsservers name="{interface_name}" addr={dns} index={i} validate=no'
            )
        for cmd in commands:
            success, _ = run_cmd(cmd)
            if not success:
                return False

        run_cmd(f'netsh interface ipv4 show dnsservers "{interface_name}"')
        return True

    except Exception as e:
        return False
    
def reset_dns_windows():
    return set_dns_windows(DEFAULT_DNS)

def _check_dns_windows(dns_servers):
    def run_ps(command):
        try:
            result = subprocess.run(
                ["powershell", "-Command", command],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

    try:
        ps_command = '''
        Get-DnsClientServerAddress -AddressFamily IPv4 | 
        Where-Object { $_.ServerAddresses -ne $null } | 
        Select-Object -ExpandProperty ServerAddresses
        '''
        
        success, output = run_ps(ps_command)
        if not success:
            print(f"Ошибка PowerShell: {output}")
            return False

        found_dns = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', output)
        
        required_dns = set(dns_servers)
        current_dns = set(found_dns)
        
        if required_dns.issubset(current_dns):
            return True
        
        return False

    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
        return False
        
def set_dns_linux(dns_servers):
    try:
        with open("/etc/resolv.conf", "w") as resolv_conf:
            resolv_conf.write("# DNS servers configured by Python script\n")
            for server in dns_servers:
                resolv_conf.write(f"nameserver {server}\n")
        print(f"DNS-серверы {dns_servers} успешно установлены.")
    except Exception as e:
        print(f"Ошибка при установке DNS: {e}")
        return False

def reset_dns_linux():
    try:
        with open("/etc/resolv.conf", "w") as resolv_conf:
            resolv_conf.write("# DNS settings reset to Google Public DNS\n")
            for server in DEFAULT_DNS:
                resolv_conf.write(f"nameserver {server}\n")
        print(f"DNS-серверы сброшены к Google Public DNS: {DEFAULT_DNS}")
    except Exception as e:
        print(f"Ошибка при сбросе DNS на Linux: {e}")
        return False

def set_dns_adguard():
    system = platform.system()
    dns_servers = DNS_SERVERS["AdGuard"]
    if system == "Windows":
        res = set_dns_windows(dns_servers)
        return res
    elif system == "Linux":
        res = set_dns_linux(dns_servers)
        return res
    else:
        print(f"Платформа {system} не поддерживается.")

def reset_dns():
    system = platform.system()
    if system == "Windows":
        res = reset_dns_windows()
        return res
    elif system == "Linux":
        res = reset_dns_linux()
        return res
    else:
        print(f"Платформа {system} не поддерживается.")

def is_custom_dns_set(dns_servers):
    system = platform.system()
    if system == "Windows":
        return _check_dns_windows(dns_servers)
    elif system == "Linux":
        return _check_dns_linux(dns_servers)
    else:
        print(f"Платформа {system} не поддерживается.")
        return False    

def _check_dns_linux(dns_servers):
    try:
        with open("/etc/resolv.conf", "r") as resolv_conf:
            content = resolv_conf.read()

        for server in dns_servers:
            if f"nameserver {server}" in content:
                return True

        return False
    except Exception as e:
        print(f"Ошибка при проверке DNS на Linux: {e}")
        return False

def already_working():
    if is_custom_dns_set(DNS_SERVERS["AdGuard"]):
        return True
    else:
        return False

def activate_deactivation(action):
    if action == "set":
        if is_custom_dns_set(DNS_SERVERS["AdGuard"]):
            print("DNS-серверы AdGuard уже установлены.")
        else:
            res = set_dns_adguard()
            return res
    elif action == "reset":
        res = reset_dns()
        return res
    else:
        print("Неверное действие. Используйте 'set' или 'reset'.")
