import feedparser
import urllib.request
import shutil
import os.path
import config

class Channel9SessionsDownloader:
    def __init__(self, feed_url, output_dir, filter_keywords):
        self.feed_url = feed_url
        self.output_dir = output_dir
        self.filter_keywords = [x.lower() for x in filter_keywords]

    def parse(self):
        print(f"Parsing rss:{self.feed_url}")
        d = feedparser.parse(self.feed_url)
        print(f"Title: {d['feed']['title']}")
        videos = [ {'title':i['title'], 
            'media': [{'url':u['url'],'size':int(u['filesize'])} 
                for u in i['media_content']]} for i in d['entries']]
        for v in videos:
            biggest = {'url':'', 'size':-1}
            for m in v['media']:
                if (biggest['size'] < m['size']):
                    biggest = {'url':m['url'], 'size':m['size']}
            v['url'] = biggest['url']
            v['size'] = biggest['size']
            del(v['media'])

        self.videos = videos
        

    def humanbytes(self,B):
        'Return the given bytes as a human friendly KB, MB, GB, or TB string'
        B = float(B)
        KB = float(1024)
        MB = float(KB ** 2) # 1,048,576
        GB = float(KB ** 3) # 1,073,741,824
        TB = float(KB ** 4) # 1,099,511,627,776

        if B < KB:
            return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
        elif KB <= B < MB:
            return '{0:.2f} KB'.format(B/KB)
        elif MB <= B < GB:
            return '{0:.2f} MB'.format(B/MB)
        elif GB <= B < TB:
            return '{0:.2f} GB'.format(B/GB)
        elif TB <= B:
            return '{0:.2f} TB'.format(B/TB)
    
    def includes_keywords(self, title):
        title_words = title.lower().split()
        filtered = [val for val in title_words if val in self.filter_keywords]
        return len(filtered) > 0

    def download(self):
        print(f"searching for new files which includes following keywords in title to download {', '.join(self.filter_keywords)}")
        for v in self.videos:
            if (self.includes_keywords(v['title']) == False):
                print (f"skipping {v['title']}")
                continue;

            print(f"downloading '{v['title']}', file size: {self.humanbytes(v['size'])}....")
            url = v['url']
            file_name = os.path.join(self.output_dir, v['title'].replace('/','').replace('\\','')) + "_" + url[url.rfind("/")+1:]
 
            if os.path.exists(file_name):
                if (os.path.getsize(file_name) > 0):
                    print(f"file '{v['title']}' already exists")
                    continue;
                    
            out_file = open(file_name, mode='wb')
            response = urllib.request.urlopen(url)
            data = response.read()
            out_file.write(data)
            out_file.close()


b = Channel9SessionsDownloader(config.feed_url, config.output_dir, config.filter_keywords)
b.parse()
b.download()