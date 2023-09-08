WITH base_attempt AS (SELECT to_char(TIMESTAMP,'dd-mm-yyyy') AS cdrdate,HOUR
,SUM(CASE WHEN accessflag IN('66') AND  IgnoreFlag='0' THEN 1 ELSE 0 END) AS MO
,SUM(CASE WHEN accessflag IN('67') AND  IgnoreFlag='0' THEN 1 ELSE 0 END) AS MT 
,SUM(CASE WHEN accessflag IN('68') then  1 else 0 end) AS DIG
,SUM(CASE WHEN  accessflag IN('72')  
AND basiccause IN ('941','808','809','850','112','361','817','762','363','909','923','340',
'960','100','749','940','942','943','118','111','41','601','715','846') THEN 1 ELSE 0 END) AS SMO
,SUM(CASE WHEN  accessflag IN('73')  
AND basiccause IN ('941','808','809','850','112','361','817','762','363','909','923','340',
'960','100','749','940','942','943','118','111','41','601','715','846') THEN 1 ELSE 0 END) AS SMT
FROM SCMCDR.SCM_CC_{mon}
WHERE M_DAY='{day}'
GROUP BY to_char(TIMESTAMP,'dd-mm-yyyy'),HOUR
),
base_success AS (SELECT to_char(TIMESTAMP,'dd-mm-yyyy') AS cdrdate,HOUR
,SUM(CASE WHEN accessflag IN('66') AND  basiccause IN('938')  AND  IgnoreFlag='0' THEN 1 ELSE 0 END) AS MO
,SUM(CASE WHEN accessflag IN('67') AND basiccause IN('941') AND  IgnoreFlag='0' THEN 1 ELSE 0 END) AS MT 
,SUM(CASE WHEN accessflag IN('68') AND basiccause in('852','963','123','949') then  1 else 0 end) AS DIG
,SUM(CASE WHEN  accessflag IN('72')  
AND basiccause IN('808','809','850','112','361','817','762') 
AND FIRSTTIMETONE='ISCHARGABLE' THEN 1 ELSE 0 END) AS SMO
,SUM(CASE WHEN  accessflag IN('73')  
AND basiccause IN('808','809','850','112','361','817','762')
AND FIRSTTIMETONE='ISCHARGABLE'THEN 1 ELSE 0 END) AS SMT
FROM SCMCDR.SCM_CC_{mon}
WHERE M_DAY='{day}'
GROUP BY to_char(TIMESTAMP,'dd-mm-yyyy'),HOUR
),
base_busfail AS (SELECT to_char(TIMESTAMP,'dd-mm-yyyy') AS cdrdate,HOUR
,SUM(CASE WHEN accessflag IN('66') AND  basiccause IN('945','336','959','960','940','100','818','601','939','111','601')  
AND  internalcause IN ('4012','5030','5031') THEN 1 ELSE 0 END) AS MO
,SUM(CASE WHEN accessflag IN('67') AND basiccause IN('363','959','923','340','960','100','749','940','942','943','118','111','41','601','715') 
AND  internalcause IN ('4012','5030','5031') THEN 1 ELSE 0 END) AS MT 
,SUM(CASE WHEN accessflag IN('68') AND basiccause IN('100','961','962','810','297','804','288','948','293','950','111') 
AND  internalcause in('4012','5030','5031','4010')then  1 else 0 end) AS DIG
,SUM(CASE WHEN  accessflag IN('72')  
AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') 
AND  internalcause in('4012','5030','5031','4010')  THEN 1 ELSE 0 END) AS SMO
,SUM(CASE WHEN  accessflag IN('73')  
AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') 
AND  internalcause in('4012','5030','5031','4010') THEN 1 ELSE 0 END) AS SMT
FROM SCMCDR.SCM_CC_{mon}
WHERE M_DAY='{day}'
GROUP BY to_char(TIMESTAMP,'dd-mm-yyyy'),HOUR
)
SELECT a.cdrdate,a.hour,a.MO AS BMO_ATTEMPT,b.MO AS BMO_SUCCESS,c.MO AS BMO_BSF,(a.MO-(b.MO+c.MO)) AS BMO_FAIL
,a.MT AS BMT_ATTEMPT,b.MT AS BMT_SUCCESS,c.MT AS BMT_BSF,(a.MT-(b.MT+c.MT)) AS BMT_FAIL
,a.DIG AS DIG_ATTEMPT,b.DIG AS DIG_SUCCESS,c.DIG AS DIG_BSF,(a.DIG-(b.DIG+c.DIG)) AS DIG_FAIL
,a.SMO AS SMO_ATTEMPT,b.SMO AS SMO_SUCCESS,c.SMO AS SMO_BSF,(a.SMO-(b.SMO+c.SMO)) AS SMO_FAIL
,a.SMT AS SMT_ATTEMPT,b.SMT AS SMT_SUCCESS,c.SMT AS SMT_BSF,(a.SMT-(b.SMT+c.SMT)) AS SMT_FAIL
FROM base_attempt a
LEFT JOIN base_success b ON a.cdrdate=b.cdrdate AND a.HOUR=b.HOUR
LEFT JOIN base_busfail c ON a.cdrdate=c.cdrdate AND a.HOUR=c.HOUR
ORDER BY a.HOUR


