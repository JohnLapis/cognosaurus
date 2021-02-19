viewset = CognateViewSet.as_view({"get": "list"})
path = (
    "/words?"
    "&por=deus"
    "&*=no"
    "&eng=banana&comparison=equal"
    "&fra=bataillon&por=entidade"
    "&fra=ba*&por=entidade"
    "&zzzzzzz=zzzz&por=entidade"
    "&por=deus"
    "&*=no"
    "&eng=banana&comparison=equal"
    "&fra=bataillon&por=entidade"
    "&fra=ba*&por=entidade"
    "&zzzzzzz=zzzz&por=entidade"
)

for i in range(300):
    viewset(rf.get(path))
