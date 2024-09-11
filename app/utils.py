"""
Desenvolvido por (Developed by / 開發者) Felipe Ferreira (f3cdde)
"""

import hmac

def safe_str_cmp(a, b):
    return hmac.compare_digest(a, b)
