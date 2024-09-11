"""
Desenvolvido por (Developed by / 開發者) Felipe Ferreira (f3cdde)
"""

import hmac

def safe_str_cmp(a, b):
    """
    Compara duas strings de forma segura, evitando ataques de timing.

    Args:
        a (str): Primeira string a ser comparada.
        b (str): Segunda string a ser comparada.

    Returns:
        bool: True se as strings forem iguais, False caso contrário.
    """
    return hmac.compare_digest(a, b)
