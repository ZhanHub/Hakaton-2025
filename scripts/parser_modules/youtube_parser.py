from youtube_comment_downloader import YoutubeCommentDownloader

def load_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
    return links

def process(link):
    comments = []
    downloader = YoutubeCommentDownloader()
    for comment in downloader.get_comments_from_url(link, sort_by=0):  # 'top' емес, 0
        comments.append(comment['text'])
    return "\n".join(comments)
