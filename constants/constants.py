# constants.py

CURRENT_VERSION = "1.0.0"

BASE_SERVER_URL = "https://noad-vpn.ddns.net"
CHECK_UPDATE_URL = f"{BASE_SERVER_URL}/check-update"
CHECK_PREM_URL = f"{BASE_SERVER_URL}/check-promo"
PLUS_ONE = f"{BASE_SERVER_URL}/plus-one"

BUILD_DIR_LINUX = "/opt/noad-vpn"
_LINUX_VPN_INFO_PATH = BUILD_DIR_LINUX +  "/data/vpn_info.json"
_LINUX_USER_INFO_PATH = BUILD_DIR_LINUX +  "/data/user_config.json"
_LINUX_CONFIG_DIR_PATH = BUILD_DIR_LINUX +  "/configs"
_LINUX_LAST_RUN_FILE = BUILD_DIR_LINUX +  "/data/last_run_date.txt"
_LINUX_OVPN_PATH = BUILD_DIR_LINUX +  "/bin/linux/openvpn"

BUILD_DIR_WINDOWS = r"C:\Program Files\noad-vpn"
WINDOWS_VPN_INFO_PATH = BUILD_DIR_WINDOWS +  r"\data\vpn_info.json"
_WINDOWS_USER_INFO_PATH = BUILD_DIR_WINDOWS +  r"\data\user_config.json"
_WINDOWS_CONFIG_DIR_PATH = BUILD_DIR_WINDOWS +  r"\configs"
_WINDOWS_LAST_RUN_FILE = BUILD_DIR_WINDOWS +  r"\data\last_run_date.txt"
_WINDOWS_OVPN_PATH = BUILD_DIR_WINDOWS +  r"\bin\windows\openvpn.exe"


VPN_INFO_PATH ="./data/vpn_info.json"
USER_INFO_PATH = "./data/user_config.json"
CONFIG_DIR_PATH =  "./configs"
LAST_RUN_FILE ="./data/last_run_date.txt"
OVPN_PATH = "../../bin/linux/openvpn"

# start for build deb
# VPN_INFO_PATH =_LINUX_VPN_INFO_PATH
# USER_INFO_PATH = _LINUX_USER_INFO_PATH
# CONFIG_DIR_PATH =  _LINUX_CONFIG_DIR_PATH
# LAST_RUN_FILE = _LINUX_LAST_RUN_FILE
# OVPN_PATH = _LINUX_OVPN_PATH
# end bulid deb

# start for build exe
# VPN_INFO_PATH =WINDOWS_VPN_INFO_PATH
# USER_INFO_PATH = _WINDOWS_USER_INFO_PATH
# CONFIG_DIR_PATH =  _WINDOWS_CONFIG_DIR_PATH
# LAST_RUN_FILE = _WINDOWS_LAST_RUN_FILE
# OVPN_PATH = _WINDOWS_OVPN_PATH
# end bulid exe


TG_LINK = "https://t.me/NoAD_VPN"

CURRENCY = {"BTC": "BTC", "USDT_TRC20":"USDT_TRC20" }

BTC_ADDR = "bc1qkwasfkg6vnldw2u0txxkrj5cy6qz2e8f3mt9h4"
TETHER_TRC20_ADDR = "TQ5Fomw1ooCAFiwVUnCegYEexmN7JLhN2w"