from src.core.core import Core
from src.core.ripe_stats import fetch_country_ip
from src.ws_server.main import WS_Main
import sys

#TODO: This is temporary, we have to implement config system
def main():
    if len(sys.argv) < 2:
        print("\nNo prefix or country code entered.\n\nExample:\nweBGP 111.222.333.0/24,222.111.333.0/24\nweBGP US\n")
    else:
        if len(sys.argv[1].strip()) == 2:
            prefixes = fetch_country_ip(sys.argv[1].strip().capitalize())
        else:
            prefixes = sys.argv[1].strip().split(",")

        ws_server = WS_Main()
        Core(prefixes, ws_server)
        ws_server.run_server()