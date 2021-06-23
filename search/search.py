from functools import cmp_to_key
from itertools import chain
import datetime
import math
from . import models

TIME, RELEVANCE, DEFAULT = tuple(range(3))

# sorts in increasing order by default
def general_cmp(a, b, reverse, when_equal):
    if reverse:
        if a < b:
            return 1
        elif a > b:
            return -1
        else:
            return when_equal
    else:
        if a > b:
            return 1
        elif a < b:
            return -1
        else:
            return when_equal


def search_pages(s, sort_mode, website=None):
    s = s.lower().strip() # change to lowercase for case-insensitivity
    s = s.split()
    priority = dict()
    for word in s:
        kwargs = [{'title__icontains': word}, {'author__icontains': word}, {'content__icontains': word}]
        if website:
            for kwarg in kwargs:
                kwarg['website'] = website
        if sort_mode == TIME:
            for kwarg in kwargs:
                kwarg['time__isnull'] = False
        title = models.Page.objects.filter(**kwargs[0])
        author = models.Page.objects.filter(**kwargs[1])
        content = models.Page.objects.filter(**kwargs[2])
        for post in chain(title, author, content):
            if post not in priority.keys():
                priority[post] = 0
    for post in priority.keys():
        lower_title = post.title.lower()
        if post.author:
            lower_author = post.author.lower()
        lower_content = post.content.lower()
        for word in s:
            priority[post] += 10*lower_title.count(word)
            if post.author:
              priority[post] += 5*lower_author.count(word)
            priority[post] += 1*lower_content.count(word)
    if sort_mode == DEFAULT:
        sum = 0
        count = 0
        for post in priority.keys():
            if post.time:
                timed = datetime.datetime.now() - post.time
                days = timed.days
                priority[post] /= math.log(days)
                sum += math.log(days)
                count += 1
        if count == 0:
            average = 0
        else:
            average = sum/count
        for post in priority.keys():
            if not post.time:
                priority[post] /= average

    def page_cmp(a, b):
        if sort_mode == TIME:
            return general_cmp(a.time, b.time, True, general_cmp(priority[a], priority[b], True, 0))
        else:
            return general_cmp(priority[a], priority[b], True, 0)

    result = list(priority.keys())
    result.sort(key=cmp_to_key(page_cmp))
    if website:
        return result
    else:
        dict_index = dict()
        final_result = []
        for i in range(len(result)):
            key = result[i].website
            if key not in dict_index.keys():
                dict_index[key] = len(final_result)
                final_result.append([key, []])
            final_result[dict_index[key]][1].append(result[i])
        return final_result
