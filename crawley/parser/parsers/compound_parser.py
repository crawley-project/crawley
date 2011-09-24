import utils
from parser import Parser, ParserException
from properties import Property
from actions import Action

class CompoundParser(Parser):
    
    def parse(self):

        
        result = self.RETURN + self.COMPREHENSION_LIST_HEAD

        count = 0
        for key, value in self.dsl.properties.iteritems():
            for index, property_element in enumerate(value):
                if count == 0:
                    result += ''.join([utils.not_first_element_plus(index), self.PYQUERY_HEAD, 
                              Property().get(key),
                              utils.trim_single_quotes(property_element),
                              self.CLOSING_PARENTHESIS,
                              Action().get(self.dsl.action)])
                else:
                    if count == 1:
                        result += ''.join([" if x in ",
                                  utils.not_first_element_plus(index), self.PYQUERY_HEAD, 
                                  Property().get(key),
                                  utils.trim_single_quotes(property_element),
                                  self.CLOSING_PARENTHESIS,
                                  Action().get(self.dsl.action)])
                    else:
                        result += ''.join([" and x in ",
                                          utils.not_first_element_plus(index), self.PYQUERY_HEAD, 
                                          Property().get(key),
                                          utils.trim_single_quotes(property_element),
                                          self.CLOSING_PARENTHESIS,
                                          Action().get(self.dsl.action)])

            count += 1
        
        return "%s%s" % (result, self.COMPREHENSION_LIST_TAIL)
    
    def _can_parse(self):
        
        return self.dsl.is_compound()
    
    def _get_exception(self):
        
        return ParserException("Can't Parse, only Compound admitted, Line %d" % self.dsl.number)