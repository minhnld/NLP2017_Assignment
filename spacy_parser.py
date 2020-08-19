import spacy
from nltk import Tree
from spacy import displacy

def nltk_spacy_tree(node):
    def tok_format(tok):
        return "_".join([tok.orth_, tok.tag_, tok.dep_])

    if node.n_lefts + node.n_rights > 0:
        return Tree(tok_format(node), [nltk_spacy_tree(child) for child in node.children])
    else:
        return tok_format(node)
def nltk_spacy_tree_visualize(sent,nlp):
    """
    Visualize the SpaCy dependency tree with nltk.tree
    """
    doc = nlp(sent)
    def token_format(token):
        return "_".join([token.orth_, token.tag_, token.dep_])

    def to_nltk_tree(node):
        if node.n_lefts + node.n_rights > 0:
            return Tree(token_format(node),
                       [to_nltk_tree(child) 
                        for child in node.children]
                   )
        else:
            return token_format(node)

    # tree = [to_nltk_tree(sent.root) for sent in doc.sents]
    # The first item in the list is the full tree
    # tree[0].draw()
    displacy.serve(doc, style="dep")
    

def spacy_viet(inputText,visualSwitch):
    nlp = spacy.load('vi_spacy_model')
    token_def="Token def."
    token_def+='\n'
    # print('1. token.text, 2. token.lemma_, 3. token.pos_, 4. token.tag_, 5. token.dep_, 6.token.shape_, 7. token.is_alpha, 8. token.is_stop')
    # doc = nlp(inputText)
    # for token in doc:
    #     print("1.{token.text}, 2.{token.lemma_}, 3.{token.pos_}, 4.{token.tag_}, 5.{token.dep_}, 6.{token.shape_}, 7.{token.is_alpha}, 8.{token.is_stop}"
    #     .format(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #             token.shape_, token.is_alpha, token.is_stop) )
    token_def+='a. token.text, b. token.lemma_, c. token.pos_, d. token.tag_, e. token.dep_, f.token.shape_, g. token.is_alpha, h. token.is_stop'
    print(token_def)
    token_def+='\n'
    doc = nlp(inputText)
    for index,token in enumerate(doc):
        temp="{}. a.{}, b.{}, c.{}, d.{}, e.{}, f.{}, g.{}, h.{}".format(index,token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                token.shape_, token.is_alpha, token.is_stop)
        token_def+=temp+'\n'
        print(temp)
    
    print('\nNLTK spaCy Parse Tree')
    result=[nltk_spacy_tree(sent.root) for sent in doc.sents]
    [root.pretty_print() for root in result]
    if visualSwitch=='on':
        nltk_spacy_tree_visualize(inputText,nlp)

    return (result,token_def,doc)

# def to_nltk_tree(node):
#     if node.n_lefts + node.n_rights > 0:
#         return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
#     else:
#         return node.orth_

# [to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]
# nltk_spacy_tree('Xe bus nào đến thành phố Huế lúc 20:00HR ?')
# nltk_spacy_tree('Thời gian xe bus B3 từ Đà Nẵng đến Huế ?')
# nltk_spacy_tree('Xe bus nào đến thành phố Hồ Chí Minh ?')
# nltk_spacy_tree('Những xe bus nào đi đến Huế ?.')
# nltk_spacy_tree('Những xe nào xuất phát từ thành phố Hồ Chí Minh ?.')
# nltk_spacy_tree('Những xe nào đi từ Đà nẵng đến thành phố Hồ Chí Minh ?.')
