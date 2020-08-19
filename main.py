"""
© 2020 Nguyen Linh Dang Minh aka Minh Ng
If there are any problems, contact me at minh.nldang@gmail.com or minh.nguyenlinhdang@hcmut.edu.vn 
This project is under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Inherit from NLTK)
"""

import nltk
from nltk import grammar, parse
import argparse
from nlp_parser import parse_to_procedure
from nlp_data import retrieve_result
from nlp_file import write_file
import spacy
from spacy_parser import spacy_viet

def main(args):
    """
    Main entry point for the program
    """
    if args.language=="english":
      #English Version
      #Load grammar from .fcfg file
      print("-------------Loading grammar---------------------")
      nlp_grammar = parse.load_parser(args.rule_file_name, trace = 0)
      print("Grammar loaded at {}".format(args.rule_file_name))
      write_file(1, str(nlp_grammar.grammar()))
                
      question = args.question
      
      #Get parse tree English
      print("-------------Parsed structure-------------")
      tree = nlp_grammar.parse_one(question.replace('?','').split())
      print(question)
      print(tree)
      write_file(2, str(tree))
  
      #
      #Parse to logical form
      print("-------------Parsed logical form-------------")
      logical_form = str(tree.label()['SEM']).replace(',',' ')
      print(logical_form)
      write_file(3, str(logical_form))
                
      #Get procedure semantics
      print("-------------Procedure semantics-------------")
      procedure_semantics = parse_to_procedure(tree)
      print(procedure_semantics['str'])
      write_file(4, procedure_semantics['str'])
      
      #Retrive result:
      print("-------------Retrieved result-------------")
      results = retrieve_result(procedure_semantics)
      if len(results) == 0:
          print("No result found!")
      else:
          for result in results:
              print(result, end=' ', flush=True)
          print('')
          write_file(5, " ".join(results))
    else:
      #Vietnamse Version
      #Load grammar from .fcfg file
      # print("-------------Loading grammar---------------------")
      # nlp_grammar = parse.load_parser(args.rule_file_name, trace = 0)
      # print("Grammar loaded at {}".format(args.rule_file_name))
      # write_file(1, str(nlp_grammar.grammar()))
                
      question = args.question
      visualize = args.visualize
      #Get parse tree English
      print("-------------Parsed structure-------------")
      print(question)
      # tree = nlp_grammar.parse_one(question.replace('?','').split())
      tree,token_def,doc=spacy_viet(question.replace('?','').replace(':','').replace('.',''),visualize)
      write_file(2, str(tree) + "\n" +token_def)

      print("-------------Parsed logical form-------------")
      from code_featstructures import mainLogic
      featStructCfg=mainLogic(doc)

      #Parse to logical form
      logical_form=featStructCfg['sem']
      # print(logical_form)
      write_file(3, str(logical_form))

      from nlp_featstruct_parser import code_featstructures_to_procedure
      #Get procedure semantics
      print("-------------Procedure semantics-------------")
      procedure_semantics = code_featstructures_to_procedure(featStructCfg) 
      print(procedure_semantics['str'])
      write_file(4, procedure_semantics['str'])

      #Retrive result:
      print("-------------Retrieved result-------------")
      results = retrieve_result(procedure_semantics)
      if len(results) == 0:
          print("No result found!")
      else:
          for result in results:
              print(result, end=' ', flush=True)
          print('')
          write_file(5, " ".join(results))
  
      # #
      # #Parse to logical form
      # print("-------------Parsed logical form-------------")
      # logical_form = str(tree.label()['SEM']).replace(',',' ')
      # print(logical_form)
      # write_file(3, str(logical_form))
                
      # #Get procedure semantics
      # print("-------------Procedure semantics-------------")
      # procedure_semantics = parse_to_procedure(tree)
      # print(procedure_semantics['str'])
      # write_file(4, procedure_semantics['str'])
      
      # #Retrive result:
      # print("-------------Retrieved result-------------")
      # results = retrieve_result(procedure_semantics)
      # if len(results) == 0:
      #     print("No result found!")
      # else:
      #     for result in results:
      #         print(result, end=' ', flush=True)
      #     print('')
      #     write_file(5, " ".join(results))


    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="NLP Assignment Command Line")
    
    parser.add_argument(
      '--question',
      default= "Which bus to Hồ Chí Minh city arrives at 05:00HR ?",
      help= "All the question to be parsed."
      # 
      #Thời gian xe bus B1 từ Hồ Chí Minh đến Huế ?
      # DẠNG 1 Xe bus nào đến thành phố Huế lúc 20:00HR ?
      # 'Which bus to Huế city arrives at 20:00HR ?'
      # 'Which bus to Huế city arrives at 22:30HR ?'
      # 'Which bus to Hồ Chí Minh city arrives at 5:00HR ?'
      # 'Which bus to Hồ Chí Minh city arrives at 5:30HR ?'
      # 'Which bus to Hồ Chí Minh city arrives at 20:30HR ?'
      # 'Which bus to Đà Nẵng city arrives at 13:30HR ?'
      # 'Which bus to Đà Nẵng city arrives at 9:30HR ?'

      # DẠNG 2 Thời gian xe bus B3 từ Đà Nẵng đến HCM ?
      # Thời gian xe bus B1 từ Hồ Chí Minh đến Huế ?
      # How long does the bus B1 depart from Hồ Chí Minh city arrive in Huế city ? 
      # Thời gian xe bus B2 từ Hồ Chí Minh đến Huế ?
      # How long does the bus B2 depart from Hồ Chí Minh city arrive in Huế city ? 
      # Thời gian xe bus B3 từ Đà Nẵng đến Hồ Chí Minh ?
      # How long does the bus B3 depart from Đà Nẵng city arrive in Hồ Chí Minh city ?
      # Thời gian xe bus B4 từ Đà Nẵng đến Hồ Chí Minh?
      # How long does the bus B4 depart from Hồ Chí Minh city arrive in Đà Nẵng city ?
      # Thời gian xe bus B5 từ Huế đến Đà Nẵng?
      # Thời gian xe bus B6 từ Huế đến Đà Nẵng?
      # Thời gian xe bus B7 từ Huế đến Hồ Chí Minh?


      # DẠNG 3 Xe bus nào đến thành phố Hồ Chí Minh ? Những xe bus nào đi đến Huế ?
      # Which bus arrive in Hồ Chí Minh city?
      # Which bus arrive in Đà Nẵng city?
      # Which buses arrive in Huế city?

      # DẠNG 4 Những xe nào xuất phát từ thành phố Hồ Chí Minh ?
      # Which buses depart from Hồ Chí Minh city?
      # Which buses depart from Huế city?
      # Which buses depart from Đà Nẵng city?
      #BONUS Which bus from Hồ Chí Minh city depart at 12:30HR?

      # DẠNG 5 Những xe nào đi từ Đà nẵng đến thành phố Hồ Chí Minh ?.
      # Which bus B1 depart from Hồ Chí Minh city arrive in Huế city ?

      )
    
    parser.add_argument(
      '--rule_file_name',
      default= "grammar.fcfg",
      help= "Context Free Grammar file to be parsed. Default = 'grammar.fcfg'"
      )

    parser.add_argument(
      '--language',
      default= "english",
      help= "You can choose between english and vietnamese"
      )
    
    parser.add_argument(
      '--visualize',
      default= "off",
      help= ""
      )
    
    args = parser.parse_args()
    main(args)