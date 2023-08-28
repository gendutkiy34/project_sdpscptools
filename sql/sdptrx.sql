WITH BASE AS (SELECT to_char(timestamp,'dd-mm-yyyy HH24:MI:SS') as cdrtime,clienttransactionid,aparty,internalcause,basiccause,transactionid,offercode,accessflag,callcharge,contentproviderid
,categoryid,cp_name,networkmode,shortcode,keyword,taskid,username,thirdpartyerrorcode
FROM scmcdr.SCM_CC_{mon}
WHERE m_day='{day}' AND hour='{hour}' AND aparty='{msisdn}'
ORDER BY to_char(timestamp,'dd-mm-yyyy HH24:MI:SS')
)
SELECT *
FROM BASE