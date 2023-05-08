from ytmusicapi import YTMusic
import ytmusicapi

import json
import os


class User:
    __slots__ = ("api",)
    
    def __init__(self):
        try:
            # Write oauth file
            if not os.path.exists('oauth.json'):
                with open('oauth.json', 'w') as f:
                    f.write(json.dumps(ytmusicapi.setup_oauth()))
                    
            self.api = YTMusic("oauth.json")
        except Exception as e:
            # Delete on error
            os.remove('oauth.json')
            raise e
