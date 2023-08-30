<<<<<<< HEAD
SELECT to_char(TIMESTAMP,'yyyy-mm-dd HH24:MM:SS') AS CDRTIME,TASKID ,CLIENTTRANSACTIONID,TRANSACTIONID,APARTY,BASICCAUSE,INTERNALCAUSE,CALLCHARGE
,OFFERCODE,CP_NAME,CONTENTPROVIDERID,NETWORKMODE,SHORTCODE ,KEYWORD ,CATEGORYID,THIRDPARTYERRORCODE 
FROM SCMCDR.SCM_CC_{mon}
WHERE M_DAY='{day}'AND HOUR='{hour}' and APARTY like ('%{msisdn}')
ORDER BY to_char(TIMESTAMP,'yyyy-mm-dd HH24:MM:SS')
=======
WITH BASE AS (SELECT to_char(timestamp,'dd-mm-yyyy HH24:MI:SS') as cdrtime,clienttransactionid,aparty,internalcause,basiccause,transactionid,offercode,accessflag,callcharge,contentproviderid
,categoryid,cp_name,networkmode,shortcode,keyword,taskid,username,thirdpartyerrorcode
FROM scmcdr.SCM_CC_{mon}
WHERE m_day='{day}' AND hour='{hour}' AND aparty like ('%{msisdn}')
ORDER BY to_char(timestamp,'dd-mm-yyyy HH24:MI:SS')
)
SELECT *
FROM BASE
>>>>>>> 145ba57fefd693fccb4b7961d603bb647b95c7cb
