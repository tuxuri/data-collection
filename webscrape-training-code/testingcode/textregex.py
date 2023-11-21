import re


address = "9366-9368, Jalan Besar, Pekan Meru, 41050 Klang, Selangor Darul Ehsan."
pattern = r'(?:.*?,){3}\s*([^,]+)$'
match = re.search(pattern, address)

if match:
    result = match.group()
    parts = [part.strip() for part in result.split(',')]
    x = len(parts) - 2

    print(parts[x-1])
    print(parts)
    if ' ' in parts[len(parts)-1] :        
        print(parts[len(parts)-1])




