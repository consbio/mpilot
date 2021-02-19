
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'COLON COMMA EQUAL FALSE FLOAT ID INT LBRACK LPAREN MINUS PLAIN_STRING PLUS RBRACK RPAREN STRING TRUE\n        program : commands\n        \n        commands : command commands\n        \n        commands : command\n        \n        command : ID EQUAL ID arguments\n        \n        arguments : LPAREN argument_list RPAREN\n        \n        arguments : LPAREN RPAREN\n        \n        argument_list : argument COMMA argument_list\n        \n        argument_list : argument COMMA\n                      | argument\n        \n        argument : ID EQUAL expression\n        \n        expression : ID\n                   | plain_string\n                   | STRING\n                   | number\n                   | list\n                   | boolean\n        \n        expression : ID expression\n        \n        plain_string : PLAIN_STRING\n                     | ID\n        \n        plain_string : plain_string COLON plain_string\n        \n        number : INT\n               | FLOAT\n        \n        number : PLUS number\n               | MINUS number\n        \n        list : LBRACK elements RBRACK\n        \n        list : LBRACK RBRACK\n        \n        elements : element COMMA elements\n        \n        elements : element COMMA\n                 | element\n        \n        element : expression\n        \n        elements : tuple_pairs\n        \n        tuple_pairs : tuple_pair COMMA tuple_pairs\n        \n        tuple_pairs : tuple_pair COMMA\n                    | tuple_pair\n        \n        tuple_pair : STRING COLON expression\n                   | PLAIN_STRING COLON expression\n                   | ID COLON expression\n        \n        boolean : TRUE\n                | FALSE\n        '
    
_lr_action_items = {'ID':([0,3,6,8,9,11,14,15,16,18,30,34,43,49,50,51,52,53,],[4,4,7,-4,13,-6,-5,13,18,18,43,47,18,43,58,18,18,18,]),'$end':([1,2,3,5,8,11,14,],[0,-1,-3,-2,-4,-6,-5,]),'EQUAL':([4,13,],[6,16,]),'LPAREN':([7,],[9,]),'RPAREN':([9,10,12,15,17,18,19,20,21,22,23,24,25,26,27,31,32,33,35,36,38,46,47,48,],[11,14,-9,-8,-7,-11,-10,-12,-13,-14,-15,-16,-18,-21,-22,-38,-39,-17,-23,-24,-26,-20,-19,-25,]),'COMMA':([12,18,19,20,21,22,23,24,25,26,27,31,32,33,35,36,38,39,41,42,43,44,45,46,47,48,59,60,61,],[15,-11,-10,-12,-13,-14,-15,-16,-18,-21,-22,-38,-39,-17,-23,-24,-26,49,-30,50,-11,-13,-18,-20,-19,-25,-37,-35,-36,]),'STRING':([16,18,30,43,49,50,51,52,53,],[21,21,44,21,44,56,21,21,21,]),'PLAIN_STRING':([16,18,30,34,43,49,50,51,52,53,],[25,25,45,25,25,45,57,25,25,25,]),'INT':([16,18,28,29,30,43,49,51,52,53,],[26,26,26,26,26,26,26,26,26,26,]),'FLOAT':([16,18,28,29,30,43,49,51,52,53,],[27,27,27,27,27,27,27,27,27,27,]),'PLUS':([16,18,28,29,30,43,49,51,52,53,],[28,28,28,28,28,28,28,28,28,28,]),'MINUS':([16,18,28,29,30,43,49,51,52,53,],[29,29,29,29,29,29,29,29,29,29,]),'LBRACK':([16,18,30,43,49,51,52,53,],[30,30,30,30,30,30,30,30,]),'TRUE':([16,18,30,43,49,51,52,53,],[31,31,31,31,31,31,31,31,]),'FALSE':([16,18,30,43,49,51,52,53,],[32,32,32,32,32,32,32,32,]),'RBRACK':([18,20,21,22,23,24,25,26,27,30,31,32,33,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,54,55,59,60,61,],[-11,-12,-13,-14,-15,-16,-18,-21,-22,38,-38,-39,-17,-23,-24,48,-26,-29,-31,-30,-34,-11,-13,-18,-20,-19,-25,-28,-33,-27,-32,-37,-35,-36,]),'COLON':([18,20,25,43,44,45,46,47,56,57,58,],[-19,34,-18,51,52,53,34,-19,52,53,51,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'commands':([0,3,],[2,5,]),'command':([0,3,],[3,3,]),'arguments':([7,],[8,]),'argument_list':([9,15,],[10,17,]),'argument':([9,15,],[12,12,]),'expression':([16,18,30,43,49,51,52,53,],[19,33,41,33,41,59,60,61,]),'plain_string':([16,18,30,34,43,49,51,52,53,],[20,20,20,46,20,20,20,20,20,]),'number':([16,18,28,29,30,43,49,51,52,53,],[22,22,35,36,22,22,22,22,22,22,]),'list':([16,18,30,43,49,51,52,53,],[23,23,23,23,23,23,23,23,]),'boolean':([16,18,30,43,49,51,52,53,],[24,24,24,24,24,24,24,24,]),'elements':([30,49,],[37,54,]),'element':([30,49,],[39,39,]),'tuple_pairs':([30,49,50,],[40,40,55,]),'tuple_pair':([30,49,50,],[42,42,42,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> commands','program',1,'p_program','parser.py',85),
  ('commands -> command commands','commands',2,'p_commands','parser.py',92),
  ('commands -> command','commands',1,'p_commands_command','parser.py',99),
  ('command -> ID EQUAL ID arguments','command',4,'p_command','parser.py',106),
  ('arguments -> LPAREN argument_list RPAREN','arguments',3,'p_arguments','parser.py',113),
  ('arguments -> LPAREN RPAREN','arguments',2,'p_argument_empty','parser.py',120),
  ('argument_list -> argument COMMA argument_list','argument_list',3,'p_argument_list','parser.py',127),
  ('argument_list -> argument COMMA','argument_list',2,'p_argument_list_argument','parser.py',134),
  ('argument_list -> argument','argument_list',1,'p_argument_list_argument','parser.py',135),
  ('argument -> ID EQUAL expression','argument',3,'p_argument','parser.py',141),
  ('expression -> ID','expression',1,'p_expression','parser.py',148),
  ('expression -> plain_string','expression',1,'p_expression','parser.py',149),
  ('expression -> STRING','expression',1,'p_expression','parser.py',150),
  ('expression -> number','expression',1,'p_expression','parser.py',151),
  ('expression -> list','expression',1,'p_expression','parser.py',152),
  ('expression -> boolean','expression',1,'p_expression','parser.py',153),
  ('expression -> ID expression','expression',2,'p_expression_identifier_expression','parser.py',160),
  ('plain_string -> PLAIN_STRING','plain_string',1,'p_plain_string','parser.py',167),
  ('plain_string -> ID','plain_string',1,'p_plain_string','parser.py',168),
  ('plain_string -> plain_string COLON plain_string','plain_string',3,'p_plain_string_with_colon','parser.py',175),
  ('number -> INT','number',1,'p_number','parser.py',182),
  ('number -> FLOAT','number',1,'p_number','parser.py',183),
  ('number -> PLUS number','number',2,'p_number_unary','parser.py',190),
  ('number -> MINUS number','number',2,'p_number_unary','parser.py',191),
  ('list -> LBRACK elements RBRACK','list',3,'p_list','parser.py',201),
  ('list -> LBRACK RBRACK','list',2,'p_list_empty','parser.py',208),
  ('elements -> element COMMA elements','elements',3,'p_elements','parser.py',215),
  ('elements -> element COMMA','elements',2,'p_elements_element','parser.py',222),
  ('elements -> element','elements',1,'p_elements_element','parser.py',223),
  ('element -> expression','element',1,'p_element_expression','parser.py',230),
  ('elements -> tuple_pairs','elements',1,'p_element_tuple_pairs','parser.py',237),
  ('tuple_pairs -> tuple_pair COMMA tuple_pairs','tuple_pairs',3,'p_tuple_pairs','parser.py',244),
  ('tuple_pairs -> tuple_pair COMMA','tuple_pairs',2,'p_tuple_pairs_pair','parser.py',251),
  ('tuple_pairs -> tuple_pair','tuple_pairs',1,'p_tuple_pairs_pair','parser.py',252),
  ('tuple_pair -> STRING COLON expression','tuple_pair',3,'p_tuple_pair','parser.py',259),
  ('tuple_pair -> PLAIN_STRING COLON expression','tuple_pair',3,'p_tuple_pair','parser.py',260),
  ('tuple_pair -> ID COLON expression','tuple_pair',3,'p_tuple_pair','parser.py',261),
  ('boolean -> TRUE','boolean',1,'p_boolean','parser.py',268),
  ('boolean -> FALSE','boolean',1,'p_boolean','parser.py',269),
]
