from bs4 import BeautifulSoup
from urllib import parse
from . import models
import ksalib.ksalib.gaonnuri as gaonnuri
import ksalib.ksalib.lms as lms
import ksalib.ksalib.ksa as ksa

gaonnuri_name = '가온누리'
gaonnuri_board_name = gaonnuri_name + ' {}'
lms_name = 'LMS'
lms_board_name = lms_name + ' {}'
ksa_name = '학교 사이트'

# read id and pw from text file
def read_id_pw(path):
    f = open(path)
    text = f.readlines()
    return text[0], text[1]

# all links are saved in Page model
def all_links_saved(links):
    for i in range(len(links)):
        find = models.Page.objects.filter(link=links[i])
        if len(find) == 0:
            return False
    return True

def save_gaonnuri_page(auth, link):
    find = models.Page.objects.filter(link=link)
    if len(find) == 0:
        response = gaonnuri.get_gaonnuri_response(auth, link)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text
        page_model = models.Page(website=gaonnuri_name, link=link, title=title, content='')
        page_model.save()

def save_all_gaonnuri_page(auth):
    gaonnuri_links = [
        'https://gaonnuri.ksain.net/xe/',
        'https://gaonnuri.ksain.net/mentoring/',
    ]
    board_names = gaonnuri.get_board_names(auth)
    for board in board_names:
        gaonnuri_links.append(gaonnuri.board_url.format(board))
    special_links = gaonnuri.get_special_links(auth)
    gaonnuri_links.extend(special_links)
    for link in gaonnuri_links:
        save_gaonnuri_page(auth, link)
        print(link)

def save_gaonnuri_post(auth, link, board):
    find = models.Page.objects.filter(link=link)
    if len(find) == 0:
        post = gaonnuri.Post(auth, link)
        website = gaonnuri_board_name.format(board)
        comments = '\n'.join([f'{comment.author} {comment.content}' for comment in post.comments])
        content = f'{post.text()} {comments}'
        post_model = models.Page(website=website, link=link, title=post.title, content=content, author=post.author,
                                 time=post.time)
        post_model.save()

def save_gaonnuri_board(auth, board_name, board_names):
    print(board_names[board_name])
    board = gaonnuri.Board(auth, board_name)
    page_num = board.page_num()
    for page in range(1, page_num+1):
        print(f'Page: {page}/{page_num}')
        links = board.links_in_page(page)
        if all_links_saved(links):
            break
        for i in range(len(links)):
            print(f'{links[i]} {i+1}/{len(links)}')
            save_gaonnuri_post(auth, links[i], board_names[board_name])

def save_all_gaonnuri_post(auth):
    board_names = gaonnuri.get_board_names(auth)
    for board_name in board_names.keys():
        save_gaonnuri_board(auth, board_name, board_names)

def save_lms_post(auth, link, board):
    params = dict(parse.parse_qsl(parse.urlsplit(link).query))
    index = params.get('idx')
    find = models.Page.objects.filter(link__contains=f'idx={index}&', website__icontains='lms')
    if len(find) == 0:
        post = lms.Post(auth, link)
        website = lms_board_name.format(board)
        content = ''
        for file in post.files:
            content += f'{file}\n'
        content += f'{post.article}\n'
        for comment in post.comments:
            content += f'{comment.author} {comment.content}\n'
        post_model = models.Page(website=website, link=link, title=post.title, author=post.author, content=content, time=post.time)
        post_model.save()
    elif len(find) == 1:
        print("already exists")
        post_model = find[0]
        post_model.link = link
        post_model.save()
    else:
        print(f"deleteing {len(find)-1} instances")
        post_model = find[0]
        post_model.link = link
        post_model.save()
        for i in range(1, len(find)):
            find[i].delete()

def save_lms_board_post(auth, key):
    board = lms.Board(auth, key)
    print(str(board))
    for page in range(1, board.page_num+1):
        print(f'Page: {page}/{board.page_num}')
        links = board.get_links_page(page)
        if all_links_saved(links):
            break
        for i in range(len(links)):
            print(f'{links[i]} {i+1}/{len(links)}')
            try:
                save_lms_post(auth, links[i], str(board))
            except:
                print('error')

def save_all_lms_post(auth):
    boards = lms.get_all_boards(auth)
    for board in boards.keys():
        save_lms_board_post(auth, board)

def save_lms_board(auth, key):
    link = lms.board_url.format(key)
    find = models.Page.objects.filter(link=link)
    if len(find) == 0:
        board = lms.Board(auth, key)
        print(board)
        page_model = models.Page(website=lms_name, link=board.link, title=str(board), author=board.teacher, content='')
        page_model.save()

def save_all_lms_board(auth):
    boards = lms.get_all_boards(auth)
    for key in boards.keys():
        save_lms_board(auth, key)

def save_ksa_page(link):
    find = models.Page.objects.filter(link=link)
    if len(find) == 0:
        page = ksa.Page(link)
        print(page.title)
        page_model = models.Page(website=ksa_name, link=link, title=page.title, content=page.content)
        page_model.save()

def save_all_ksa_page():
    pages = ksa.get_all_pages()
    for link in pages:
        save_ksa_page(link)

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
