from __future__ import unicode_literals

import youtube_dl

with open("hrefs.txt", "r") as fp:
    urls = fp.readlines()

    for url in urls:
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
