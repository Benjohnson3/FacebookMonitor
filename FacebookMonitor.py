
import re
from facepy import GraphAPI
from better_profanity import profanity

#userToken = 'EAANGamOm9fYBAEz8ypxpi4Mj05aqKtJqSA7zPjKssKXoNjZBlde0wMwbOJllPMfx6nACsg0vyNmVCoR3wLxZAsAJYzYf12PXbYoqzluRQB7ZAB7FruiqdebDonoNtZADS7YutUxbXt9HF1e9Su30KiZBExnA5qYtA8YDMT9no941chG24Raba'
#appToken = '921847682495990|Sa4noY4DA_FiDIRrjqlag2jjewQ'

#newToken = 'EAANGamOm9fYBAHcMzbfReXRklYUFcUdMuhhA9xzmNNrQFO0qOzHScNvGL474DaWgmEZBOC3rUbv0B3sY0S9g9JlQJnrvneSjsUl0zbl99rdqa7PWzGZBnN6ZALb3abvbedWvZACuhjnjFNSkUC7QdZBHPvdXtZAYvV2ZAPHjIiJkBG9AmhRPDZAAh0uXe3kljYsfXJr1zFkW5OGvGqaHLf45xrTXS4x8sll1QqV45sOxTc0MDZBHAo8Rn'
#page_access_token = 'EAAyNZBZA3BoOIBAJkCK9QM3mz1iuhlWLtbmXkZBzQwcbWiTPiYqwN6TaI51jVVM4ZAAqC0rvkvejD7KED5cBXWIGmuuKw38daeTyeqgJxBsKjVoHZBLmb0BBxgnFBrsZCABHo4CuDVZAOc4wZAZC8edYGdOx6U8Aa4HDaNSZAkmz6zk2iYBANmvKZBh'

class FacebookMonitor:
    def __init__(self, access_token, group_id):
        self.graph = GraphAPI(access_token)
        self.group_id = group_id
        self.post_url = f'https://www.facebook.com/groups/{group_id}/permalink/'
    def get_group_posts(self):
        return self.graph.get(f'{self.group_id}/feed')['data']
    def contains_profanity(self, text):
        return profanity.contains_profanity(text)
    def scan_group_posts(self):
        results = []
        group_posts = self.graph.get(f"{self.group_id}/feed")
        for post in group_posts['data']:
            post_id = post['id']
            post_message = post.get('message', '')
            if self.contains_profanity(post_message):
                post_url = f"{self.post_url}{post_id.split('_')[-1]}"
                poster_name = post.get('from', {}).get('name', 'Unknown')
                results.append({
                    "type": "post",
                    "poster_name": poster_name,
                    "content": post_message,  # Return the whole post content
                    "url": post_url
                })
            comments = self.graph.get(f"{post_id}/comments")
            for comment in comments['data']:
                comment_message = comment.get('message', '')
                if self.contains_profanity(comment_message):
                    comment_id = comment['id']
                    comment_url = f"{self.post_url}{post_id.split('_')[-1]}?comment_id={comment_id}"
                    commenter_name = comment.get('from', {}).get('name', 'Unknown')
                    results.append({
                        "type": "comment",
                        "poster_name": commenter_name,
                        "content": comment_message,  # Return the whole comment content
                        "url": comment_url
                    })
        return results

    def get_profanity(self, text):
        profanities = profanity.censor(text, '***')
        return profanities
    
    def get_profanity_list(self, text):
        return profanity.censor_words(text)


