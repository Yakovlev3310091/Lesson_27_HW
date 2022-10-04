import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView

from Lesson_27_HW import settings
from users.models import User, Location


class UserListView(ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(self, *args, **kwargs)
        self.object_list = self.object_list.order_by('user_name')
        paginator = Paginator(object_list=self.object_list, per_page=settings.TOTAL_ON_PAGE)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        result = []
        for user in page_obj:
            result.append(
                {'id': user.id,
                 'user_name': user.user_name,
                 'first_name': user.first_name,
                 'last_name': user.last_name,
                 'role': user.role,
                 'ads_count': user.ads.count()
                 })
        return JsonResponse({'ads': result, 'page': page_obj.number, 'total': page_obj.paginator.count},
                            safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['user_name', 'password', 'first_name', 'last_name', 'role', 'locations']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        user = User.objects.create(
            user_name=data['user_name'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data['role'],
            password=data['password']
        )
        for loc in data['locations']:
            location, _ = Location.objects.get_or_create(name=loc)
            user.location.add(location)

        return JsonResponse(
            {'id': user.id,
             'user_name': user.user_name,
             'first_name': user.first_name,
             'last_name': user.last_name,
             'role': user.role,
             'locations': [str(u) for u in user.location.all()]
             })




