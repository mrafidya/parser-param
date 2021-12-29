from pipetools import pipe
import re


def clean_block_comments(text):
    return re.sub(r'/\*[\w\W]*?(?=\*/)\*/', '', text)


def clean_single_comment(text):
    return re.sub(r'--[^\r\n]*', '', text)


def clean_block_variable(text):
    return re.sub(r'DECLARE[\w\W]*?(?=BEGIN)BEGIN', '', text, re.IGNORECASE)


def clean_line(text):
    return re.sub(r'[\t\r\n]', ' ', text)


def clean_prt(text):
    return re.sub(r'_1_prt_[^\r\n]*', '', text)


def clean_tail(text):
    return re.sub(r"_?'?\|\|[^\r\n]*", '', text).replace(')', '')


clean_table = pipe | clean_prt | clean_tail

cleaner = pipe | clean_block_comments | clean_single_comment | clean_block_variable | clean_line
