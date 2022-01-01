class Colors:
    GREEN = "\u001b[32m"
    RED = "\u001b[31m"
    BRED = "\u001b[31;1m"
    CYAN = "\u001b[36m"
    YELLOW = "\u001b[33m"
    BOLD = "\u001b[1m"
    BMAGENTA = "\u001b[35;1m"
    BBLACK = "\u001b[30;1m"
    RESET = "\u001b[0m"


ERROR = f"{Colors.RED}[ERROR]{Colors.RESET}"
WARNING = f"{Colors.YELLOW}[WARNING]{Colors.RESET}"
INFO = f"{Colors.BBLACK}[INFO]{Colors.RESET}"