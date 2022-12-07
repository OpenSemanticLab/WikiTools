# extents mwclient.site

import sys
import src.wiki_tools as wt 
import mwclient
from jsonpath_ng.ext import parse

class WtSite:
    
    def __init__(self, site: mwclient.Site = None):
        if site: self._site = site
        else: raise ValueError("Parameter 'site' is None")
        
    @classmethod
    def from_domain(cls, domain: str = None, password_file: str = None):
        site = wt.create_site_object(domain, password_file)
        return cls(site)
    
    def get_WtPage(self, title: str = None):
        wtpage = WtPage(self, title)
        return wtpage
    
    def prefix_search(self, text):
        return wt.prefix_search(self._site, text)
    
    def semantic_search(self, query):
        return wt.semantic_search(self._site, query)

    def modify_search_results(self, mode:str, query: str, modify_page, limit=None, comment=None, log=False, dryrun=False):
        titles = []
        if mode == 'prefix': titles = wt.prefix_search(self._site, query)
        elif mode == 'semantic': titles = wt.semantic_search(self._site, query)
        if limit: titles = titles[0:limit]
        if log: print(f"Found: {titles}")
        for title in titles:
            wtpage = self.get_WtPage(title)
            modify_page(wtpage)
            if log: 
                print(f"======= {title} =======")
                print(wtpage._content + "\n")
            if not dryrun: wtpage.edit(comment)              
                
            
    
class WtPage:
    
    def __init__(self, wtSite: WtSite = None, title: str = None):
        self.wtSite = wtSite
        self.title = title
        
        self._page = wtSite._site.pages[self.title]
        self.exists = self._page.exists
        self._original_content = ""
        self._content = ""
        self._dict = []
        if self.exists: 
            self._original_content = self._page.text()
            self._content = self._original_content
            self._dict = wt.create_flat_content_structure_from_wikitext(self._content, array_mode = 'only_multiple' )

    def get_content(self):
        return self._content

    def set_content(self, content):
        self._content = content
        self.changed = True
            
    def append_template(self, template_name: str = None, template_params: dict = None):
        self._dict.append({template_name: template_params})
        return self

    def append_text(self, text):
        self._dict.append(text)
        return self
        
    def get_value(self, jsonpath):
        jsonpath_expr = parse(jsonpath)
        res = []
        d = dict(zip(range(len(self._dict)), self._dict)) #convert list to dict with index
        for match in jsonpath_expr.find(d):
            res.append(match.value)
        return res
    
    def update_dict(combined: dict, update: dict) -> None:
        for k, v in update.items():
            if isinstance(v, dict):
                WtPage.combine_into(v, combined.setdefault(k, {}))
            else:
                combined[k] = v
    
    def set_value(self, jsonpath_match, value, replace = False):
        jsonpath_expr = parse(jsonpath_match)
        d = dict(zip(range(len(self._dict)), self._dict)) #convert list to dict with index
        #if create: jsonpath_expr.update_or_create(d, value)
        #else: jsonpath_expr.update(d, value)
        matches = jsonpath_expr.find(d)
        for match in matches:
            print(match.full_path)
            #pprint(value)
            if not replace: 
                WtPage.update_dict(match.value, value)
                value = match.value
            #pprint(value)
            match.full_path.update_or_create(d, value)
        self._dict = list(d.values()) #convert dict with index to list
        return self

    def update_content(self):
        self._content = wt.get_wikitext_from_flat_content_structure(self._dict)
        self.changed = self._original_content != self._content
        return self
    
    def edit(self, comment: str = None):
        if not comment: comment = "[bot] update of page content"
        if self.changed: self._page.edit(self._content, comment);

 
        
    
        
    
