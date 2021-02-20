viewset = CognateViewSet.as_view({"get": "list"})
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

for i in range(300):
    for path in paths:
        viewset(rf.get(path))
