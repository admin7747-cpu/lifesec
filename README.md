# LIFESEC 🛡️

An offline intelligent terminal featuring AI integration and a DDoS
module designed for Termux.

## 📥 Installation

To clone and launch the tool in your Termux terminal, run the following commands:

```bash
pkg update && pkg install git python -y
git clone [https://github.com/admin7747-cpu/lifesec.git](https://github.com/admin7747-cpu/lifesec.git)
cd lifesec
python lifesec.py

#🚀DDoS MODULE USAGE
You can execute test attacks or manage servers by specifying the server IP (-s) and turbo threads (-t):
python lifesec.py --ddos -s
<SERVER_IP> -t <THREADS>
