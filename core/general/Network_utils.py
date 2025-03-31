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

import requests, webbrowser
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from constants.constants import TG_LINK, CHECK_PREM_URL

def generate_user_agent():
    ua = UserAgent()
    return ua.random
    
def check_internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=1)
        return response.status_code == 200
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
    
def get_sitekey(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        turnstile_div = soup.find("div", class_="cf-turnstile")

        if turnstile_div:
            sitekey = turnstile_div.get("data-sitekey")
            return sitekey
        else:
            print("Элемент с классом 'cf-turnstile' не найден.")
            return None
            
    except requests.exceptions.RequestException as req_err:
        print(f"Ошибка при выполнении запроса: {req_err}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None
    
def check_promo(promo):
    try:
        payload = {"promo": promo}
        response = requests.post(CHECK_PREM_URL, json=payload)
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {
                "success": False,
                "error": f"Server returned status code {response.status_code}",
                "details": response.text,
            }

    except requests.exceptions.RequestException as e:
        return {"success": False, "error": "Network error", "details": str(e)}

def open_telegram_link():
    webbrowser.open(TG_LINK)