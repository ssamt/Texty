from bs4 import BeautifulSoup
from . import models
from ksalib.ksalib.Auth import Auth
from ksalib.ksalib.gaonnuri import Post, Board, get_gaonnuri_response, get_board_names, board_url, get_special_links

gaonnuri_name = '가온누리'
gaonnuri_board_name = gaonnuri_name + ' {board}'

def save_gaonnuri_page(auth, link):
    find = models.Page.objects.filter(link=link)
    if len(find) == 0:
        response = get_gaonnuri_response(auth, link)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text
        page_model = models.Page(website=gaonnuri_name, link=link, title=title, content='')
        page_model.save()

def save_all_gaonnuri_page(auth):
    gaonnuri_links = [
        'https://gaonnuri.ksain.net/xe/',
        'https://gaonnuri.ksain.net/mentoring/',
    ]
    board_names = get_board_names(auth)
    for board in board_names:
        gaonnuri_links.append(board_url.format(board))
    special_links = get_special_links(auth)
    gaonnuri_links.extend(special_links)
    for link in gaonnuri_links:
        save_gaonnuri_page(auth, link)
        print(link)

def save_gaonnuri_post(auth, link, board):
    find = models.Page.objects.filter(link=link)
    if len(find) == 0:
        post = Post(auth, link)
        website = gaonnuri_board_name.format(board)
        comments = '\n'.join([f'{comment.author} {comment.content}' for comment in post.comments])
        content = f'{post.text()} {comments}'
        post_model = models.Page(website=website, link=link, title=post.title, content=content, author=post.author,
                                 time=post.time)
        post_model.save()

def save_gaonnuri_board(auth, board_name, board_names):
    print(board_name)
    board = Board(auth, board_name)
    links = board.all_links()
    for i in range(len(links)):
        print(f'{links[i]} {i}/{len(links)}')
        try:
            save_gaonnuri_post(auth, links[i], board_names[board_name])
        except:
            print('error')

def save_all_gaonnuri_post(auth):
    board_names = get_board_names(auth)
    for board_name in board_names.keys():
        save_gaonnuri_board(auth, board_name, board_names)
