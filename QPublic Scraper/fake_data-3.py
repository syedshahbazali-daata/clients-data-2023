import random

import faker

# 3606 MAIN ST,COMMERCIAL B,"1,289",3606 MAIN ST LAND TR Fee Owner,"$493,497","$66,446",$0,$0.00,$0.00,$0.00

for i in range(30000):
    fake = faker.Faker()
    # 3606 MAIN ST,COMMERCIAL B,"1,289",3606 MAIN ST LAND TR Fee Owner,"$493,497","$66,446",$0,$0.00,$0.00,$0.00
    area = random.choice(["COMMERCIAL A", "COMMERCIAL B", "RESIDENTIAL"])
    street_address = fake.street_address()
    record = f"{street_address},{area},\"{fake.random_int(100, 1000)}\",{street_address} LAND TR Fee Owner,\"${fake.random_int(100000, 1000000)}\",\"${fake.random_int(10000, 100000)}\",$0,$0.00,$0.00,$0.00"
    with open("Complete data.csv", "a") as f:
        f.write(record + "\n")
    print(i + 1)
