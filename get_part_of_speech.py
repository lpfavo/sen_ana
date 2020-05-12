


def getpart_of_speech(categories_nodes,categories):
    cate_name={'a':'adjective','b':"Other noun-modifier",
               'c':"Conjunction" ,'d':"Adverb" ,
               'e':"Exclamation",'g':"Morpheme",
               'h':"Prefix",'i':"Idiom",
               'j':"Abbreviation",'k':"Suffix",
               'm':"Number",'n':"General noun",
               'nd':"Direction noun",'nh':"Person name",
               'ni':"Organization name" ,'nl':"Location noun" ,
               'ns':"Geographical name" ,'nt':"Temporal noun" ,
               'nz':"Other proper noun",'o':"Onomatopoeia" ,
               'p':"Preposition",'q':"Quantity" ,
               'r':"Pronoun",'u':"Auxiliary" ,
               'v':"Verb" ,'wp':"Punctuation" ,
               'ws':"Foreign words",'x':"Non-lexeme"}

    categories_num=len(categories)
    categories_collect_entities={}
    collect_categories=[]
    for i in range(categories_num):
        collect_categories.append(cate_name[categories[i]['name']])

    for i in range(categories_num):
        node_info = []
        for entity in categories_nodes:
            if entity['category']==i:
                node_info.append(entity['name'])
        categories_collect_entities[categories[i]['name']]=node_info


    part_of_speech_nodes = []
    part_of_speech_links=[]
    part_of_speech_nodes.append({'name':'root','category':0,'label':"Root"})

    count_node = 1
    for i in range(categories_num):
        part_of_speech_nodes.append({'name':cate_name[categories[i]['name']],'category':i+1})
        part_of_speech_links.append({'source':count_node,'target':0})
        count_node += 1


    for i in range(categories_num):
        app = categories_collect_entities[categories[i]['name']]
        for j in range(len(app)):
            part_of_speech_nodes.append({'name': app[j], 'category': i+1,'label':categories[i]['name']})
            part_of_speech_links.append({'source': count_node, 'target': i + 1})
            count_node += 1

    part_of_speech = {"nodes": part_of_speech_nodes, "links": part_of_speech_links,'categories':collect_categories}
    return part_of_speech


# print(getpart_of_speech("2018年7月26日，华为创始人任正非向5G极化码（Polar码）之父埃尔达尔教授举行颁奖仪式，表彰其对于通信领域做出的贡献。"))
