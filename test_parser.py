from parser import parse_signal

text = """
GOLD BUY NOW @ 4180-4176

SL 4173
TP 4185
TP 4190
"""

print(parse_signal(text))