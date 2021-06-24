from urllib import parse
from . import models
from .scrap import gaonnuri_name, lms_name, ksa_name, student_name, department_name

# for temporary use
def delete_copies():
    lms_posts = models.Page.objects.filter(website__istartswith='lms ')
    index_dict = dict()
    for post in lms_posts:
        params = dict(parse.parse_qsl(parse.urlsplit(post.link).query))
        index = params.get('idx')
        if index not in index_dict:
            index_dict[index] = []
        index_dict[index].append(post)
    for posts in index_dict.values():
        if len(posts) > 1:
            for i in range(1, len(posts)):
                posts[i].delete()

def set_default_importance():
    site_names = [gaonnuri_name, lms_name, ksa_name, student_name, department_name]
    official_page = models.Page.objects.filter(website__in=site_names)
    official_page.update(default_importance=3)
    main_page = models.Page.objects.filter(title__in=site_names)
    main_page.update(default_importance=5)
    lms_attendance = models.Page.objects.filter(website__contains='출석')
    lms_attendance.update(default_importance=0.25)
