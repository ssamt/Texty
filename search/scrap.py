from . import models
from ksalib.ksalib.Auth import Auth
from ksalib.ksalib.gaonnuri import Post, Board, get_board_names

def save_gaonnuri_post(auth, link, board):
    find = models.Page.objects.filter(link=link)
    if len(find) == 0:
        post = Post(auth, link)
        website = f'가온누리 {board}'
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

def save_all_gaonnuri_post(auth, board_names):
    for board_name in board_names.keys():
        save_gaonnuri_board(auth, board_name, board_names)
