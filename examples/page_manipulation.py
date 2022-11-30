import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #add parent dir to path

import src.wiki_tools as wt 
from src.wtsite import WtSite, WtPage
from pprint import pprint 

def basic_text_manipulation():
    wikitext_org = """{{OslTemplate:LIMS/Device/Type
    |timestamp=2022-10-10T00:00:00.000Z
    |creator=C1;C2
    |display_name=Test Term
    |label=Device Test Type with Term
    |label_lang_code=en
    |description=Some description 
    with line break
    |category=Category:OSLa444b0eeb79140d58a836a7fc6fc940a
    |relations={{OslTemplate:KB/Relation
    |property=IsRelatedTo
    |value=Term:OSL6b663c61c12d42e8be37d735dd2a869c
    }}SomeText{{OslTemplate:KB/Relation
    |property=IsRelatedTo
    |value=Term:OSL6b663c61c12d42e8be37d735dd2a869c
    }}
    }}
    =Details=
    some text
    
    {{Some/Template
    |p1=v1
    }}
    
    <br />
    {{OslTemplate:LIMS/Device/Type/Footer
    }}"""
    
    content_dict_1 = wt.create_flat_content_structure_from_wikitext(wikitext_org)
    pprint(content_dict_1)
    
    wikitext_2 = wt.get_wikitext_from_flat_content_structure(content_dict_1)
    print(wikitext_2)
    if wikitext_2 == wikitext_org: print("wikitext_2 == wikitext_org")
    else: print("wikitext_2 != wikitext_org")
    
    content_dict_3 = wt.create_flat_content_structure_from_wikitext(wikitext_2)
    pprint(content_dict_3)
    wikitext_3 = wt.get_wikitext_from_flat_content_structure(content_dict_3)
    print(wikitext_3)
    if wikitext_3 == wikitext_2: print("wikitext_3 == wikitext_2")
    else: print("wikitext_3 != wikitext_2")
    
    content_dict_3[0]['OslTemplate:LIMS/Device/Type']['display_name'] = 'NEW VALUE'
    print(wt.get_wikitext_from_flat_content_structure(content_dict_3))
    
def mass_page_edit():
    wtsite = WtSite.from_domain("wiki-dev.open-semantic-lab.org", "examples/wiki-admin.pwd")    
    #wtpage = wtsite.get_WtPage("LabNote:220601-sist-0001-ni")
    #wtpage = wtsite.get_WtPage("testesfesefsef")
    #wtpage.append_template("TestTemplate", {"p1": "v1"})
    #wtpage.append_text("Some text",)
    #wtpage.append_template("TestTemplate", {"p1": "v2"})
    
    #pprint(wtpage._dict)
    
    #res = wtpage.get_value("*.TestTemplate.p1")
    #pprint(res)
    #d = wtpage.set_value("*.TestTemplate.p1", "v3")
    
    
    #local_id = wtpage.title.split(":")[1]
    #wtpage.set_value("*.'OslTemplate:ELN/Entry/Header'", {"local_id" : [local_id]})
    
    #wtpage.update_content()
    #pprint(wtpage._dict)
    #wtpage.edit()
    #print(wtpage.changed)
            
    wtsite.modify_search_results('semantic', '[[Category:labNote]]', 
                                 lambda wtpage:
                                     #print("Lambda")#wtpage.title)
                                     wtpage.set_value("*.'OslTemplate:ELN/Entry/Header'", {"id" : [wtpage.title.split(":")[1]]}).update_content()
                                , limit=1, comment="[bot] set id from title", log=True, dryrun=True)  

def schema_renaming():
    wtsite = WtSite.from_domain("wiki-dev.open-semantic-lab.org", "examples/wiki-admin.pwd")    
    def modify(wtpage: WtPage):
        wtpage.content_replace("_osl_template", "osl_template")
        wtpage.content_replace("_osl_footer", "osl_footer")
    wtsite.modify_search_results('prefix', 'JsonSchema:', modify, limit=20, comment="rename keywords _osl* to osl*", log=True, dryrun=False)      

#mass_page_edit()
schema_renaming()