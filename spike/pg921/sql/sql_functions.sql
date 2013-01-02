--sql_functions.sql
select name, func from sys.functions where sql = true
order by name;
