data1 = "Hello"
data2 = "Hello"
data3 = "World"

hash1 = hash(data1)
hash2 = hash(data2)
hash3 = hash(data3)

print(f"Хэш '{data1}': {hash1}")
print(f"Хэш '{data2}': {hash2}")
print(f"Хэш '{data3}': {hash3}")
print("1 коммит")
print("2 коммит")
# hash1 и hash2 будут одинаковыми при одном запуске программы,
# но могут отличаться между разными запусками (в целях безопасности).
# hash3, скорее всего, будет отличаться от hash1 и hash2.