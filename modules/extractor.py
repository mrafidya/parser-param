from pipetools import pipe
from .cleaner import cleaner, clean_prt
from .remove_duplicate import remove_duplicate
from .split import split


def extract(lists):
    container = []
    function_name = ''
    for item in lists:
        item = item.lower()
        c=0
        if (('V_CURR_DATE' in item)
                and ':=' in item
                and 'now()' in item):
            
            stmt = item.split(' ')
            for idx, target in enumerate(stmt):
              
              if target == 'interval' and idx < len(stmt):
                  if 'days' in stmt[idx+2] or 'day' in stmt[idx+2] \
                            and '.fnc' not in stmt[idx+1]:
                        container.append (function_name+';-'+(stmt[idx+1]))
                        c=1
            if c!=1:
                container.append (function_name+';0')
    return container


extractor = pipe | cleaner | split | extract | remove_duplicate
