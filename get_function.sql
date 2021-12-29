SELECT
    n.nspname as schema_name,
    a.proname,
    'CREATE OR REPLACE FUNCTION '||n.nspname||'.'||a.proname||'('||pg_catalog.pg_get_function_arguments(a.oid)||')
                    RETURNS integer AS
                    $BODY$'||chr(10)||
    a.prosrc
        ||chr(10)||
    '$BODY$
LANGUAGE plpgsql VOLATILE;' as routine_definition
FROM pg_proc a
         LEFT JOIN pg_catalog.pg_namespace n ON n.oid = a.pronamespace
ORDER BY 1,2