from functools import cmp_to_key
from itertools import chain
from . import models

TIME, RELEVANCE = tuple(range(2))

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
    s = s.strip()
    s = s.split()
    priority = dict()
    for word in s:
        if website:
            title = models.Page.objects.filter(title__icontains=word, website=website)
            author = models.Page.objects.filter(author__icontains=word, website=website)
            content = models.Page.objects.filter(content__icontains=word, website=website)
        else:
            title = models.Page.objects.filter(title__icontains=word)
            author = models.Page.objects.filter(author__icontains=word)
            content = models.Page.objects.filter(content__icontains=word)
        for post in chain(title, author, content):
            if post not in priority.keys():
                priority[post] = 0
        for post in title:
            priority[post] += 20*post.title.count(word)
        for post in author:
            priority[post] += 10*post.author.count(word)
        for post in content:
            priority[post] += 1*post.content.count(word)

    def page_cmp(a, b):
        if sort_mode == TIME:
            return general_cmp(a.time, b.time, True, general_cmp(priority[a], priority[b], True, 0))
        else:
            return general_cmp(priority[a], priority[b], True, general_cmp(a.time, b.time, True, 0))

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
        print(final_result)
        return final_result
