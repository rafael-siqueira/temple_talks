import brotli
import bs4
import dropbox
from dropbox.files import WriteMode
import requests as rq
import re

# Connect to Dropbox
dbx = dropbox.Dropbox('$YOUR_DBX_TOKEN')
dbx_path = '$YOUR_DBX_PATH'

# Get links
resp = rq.get("https://tou.org/talks/")
try:
  content = brotli.decompress(resp.content)
except:
  content = resp.content
parsed_html = bs4.BeautifulSoup(content)
talks_elements = parsed_html.find_all('a', attrs={'class': re.compile(r'fusion-button button-flat button-small button-blue')})

# Download and save files to Dropbox folder
for i in range(0,3):
  talk_url = talks_elements[i].get('href')
  talk_file = rq.get(talk_url)
  begin_file_name = re.search("talks/", talk_url).span()[1]
  dbx_path_talk = dbx_path+talk_url[begin_file_name:]
  dbx.files_upload(talk_file.content, dbx_path_talk, mode=WriteMode('overwrite'))
