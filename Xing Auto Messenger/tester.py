x = """2.56.119.93:5074:erbaqlvp:b7hddlugm3yf
185.199.229.156:7492:erbaqlvp:b7hddlugm3yf
185.199.228.220:7300:erbaqlvp:b7hddlugm3yf
185.199.231.45:8382:erbaqlvp:b7hddlugm3yf
188.74.210.207:6286:erbaqlvp:b7hddlugm3yf
188.74.183.10:8279:erbaqlvp:b7hddlugm3yf
188.74.210.21:6100:erbaqlvp:b7hddlugm3yf
45.155.68.129:8133:erbaqlvp:b7hddlugm3yf
154.95.36.199:6893:erbaqlvp:b7hddlugm3yf
45.94.47.66:8110:erbaqlvp:b7hddlugm3yf
"""

x = x.strip().split("\n")
for i in x:
    user_name = i.split(":")[2]
    password = i.split(":")[3]
    proxy = i.split(":")[0] + ":" + i.split(":")[1]
    x = f"""{user_name}:{password}@{proxy}"""
    print(x)

    # kqre5mcy84golwbt:jldx7vpbm8r46qh2@
    # kqre5mcy84golwbt:jldx7vpbm8r46qh2@new-york1.thesocialproxy.com:10000

