paths = [
    "/words?por=deus",
    "/",
    "/words",
    "/words?*=no",
    "/words?eng=banana&comparison=equal",
    "/words?fra=bataillon&por=entidade",
    "/words?fra=ba*&por=entidade",
    "/words?zzzzzzz=zzzz&por=entidade",
]

# for i in range(100):
for i in range(1):
    for path in paths:
        client.get(path)
