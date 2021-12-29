def contain_source_or_target(stmt):
    return ('insert into' in stmt or 'select' in stmt) \
        and 'stg_cc.monitoring_function' not in stmt \
        and 'stg.proc_log' not in stmt \
        and 'tmp.is_monitoring_function' not in stmt \
        and 'tmp.is_proc_log' not in stmt \
        and 'tmp.is_auto_rerun' not in stmt \
        and 'v_description' not in stmt


def contain_function_name(stmt):
    return 'create or replace function' in stmt


def contain_delete(stmt):
    return 'delete from' in stmt \
        and 'v_prev_int' not in stmt \
        and 'v_description' not in stmt


def contain_truncate(stmt):
    return 'truncate' in stmt \
        and 'v_prev_int' not in stmt \
        and 'v_description' not in stmt


def is_table(text):
    return '.' in text \
        and ':' not in text \
        and '{' not in text \
        and ('||' not in text or text.find("_'||")+1)
