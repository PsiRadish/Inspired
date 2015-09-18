# coding=utf-8

# modified from http://chase-seibert.github.io/blog/2011/01/28/sanitize-html-with-beautiful-soup.html

from bs4 import BeautifulSoup, Comment
import re
from html.parser import HTMLParseError

def sanitize(html):
    
    if not html:
        return None
    
    # remove these tags, complete with contents.
    blacklist_tags = ['script', 'style']
    
    whitelist_tags = [
        'a', 'abbr', 'acronym', 'address', 'b', 'big', 'blockquote', 'br', 'caption',
        'center', 'cite', 'code', 'col', 'colgroup', 'dd', 'del', 'dfn', 'div', 'dl',
        'dt', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'ins', 'kbd',
        'li', 'ol', 'p', 'pre', 'q', 's', 'samp', 'small', 'span', 'strike', 'strong',
        'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr', 'tt', 'u',
        'ul', 'var']
    whitelist_attr = ['align', 'alt', 'axis', 'class', 'height', 'href', 'name', 'src',
        'title', 'width']
    
    try:
        soup = BeautifulSoup(html, "lxml")
    except:
        # special handling?
        print(e)
        raise e
    
    # now strip HTML we don't like.
    for tag in soup.findAll():
        if tag.name.lower() in blacklist_tags:
            # blacklisted tags are removed in their entirety
            tag.extract()
        # check against whitelist
        elif tag.name.lower() in whitelist_tags:
            # tag is allowed, now filter attributes
            tag.attrs = {name: value for name, value in tag.attrs.items() if name.lower() in whitelist_attr}
            
            # no hrefs starting with "javascript:"
            if ('href' in tag.attrs and re.match('^javascript:', tag.attrs['href'])):
                tag.attrs.pop('href')
        else:
            tag.unwrap()
            # tag.name = "span"
            # tag.attrs = []
    
    # scripts can be executed from comments in some cases
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    
    # print(soup)
    
    return str(soup)

