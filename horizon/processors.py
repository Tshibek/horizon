
from accounts.models import Admin, Profile


# @cache_page(60 * 10)
# def server(request):
#     from mcstatus import MinecraftServer
#     server = MinecraftServer.lookup("hub.bmc.gg")
#     stat = server.status()
#     calc = ((stat.players.online / 250) * 100)
#     context = locals()
#     return context


def adminrequest(request):
    if request.user.is_authenticated:
        admin = Admin.objects.filter(user=request.user)
    else:
        admin = None
    return {'admin': admin, 'request': request}


def rolerequest(request):
    if request.user.is_authenticated:
        news_role = None
        if request.user.profile.rank == 'Właściciel' or request.user.profile.rank == 'HeadAdmin':
            news_role = Profile.objects.filter(user=request.user)
    else:
        news_role = None
    return {'news_role': news_role, 'request': request}
