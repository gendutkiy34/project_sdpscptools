WITH base_d0 AS (SELECT to_char(timestamp,'yyyy-mm-dd') AS cdr_date
,SUM(CASE WHEN accessflag IN('66') THEN 1 ELSE 0 END) MO_ATT
,SUM(CASE WHEN accessflag IN('66') AND basiccause IN('938') THEN 1 ELSE 0 END)AS MO_SUC
,SUM(CASE WHEN accessflag IN('66')  
AND basiccause IN('945','336','959','960','940','100','818','601','939','111','601')
AND internalcause IN ('4012','5030','5031') THEN 1 ELSE 0 END ) AS MO_BFL
,SUM(CASE WHEN accessflag IN('67') THEN 1 ELSE 0 END)MT_ATT
,SUM(CASE WHEN accessflag IN('67')  AND basiccause IN('941') THEN 1 ELSE 0 END) AS MT_SUC
,SUM(CASE WHEN accessflag IN('67')  AND basiccause IN('363','959','923','340','960','100','749','940','942','943','118','111','41','601','715') 
AND internalcause IN ('4012','5030','5031') 
OR (basiccause IN('813') AND internalcause is null) THEN 1 ELSE 0 END ) AS MT_BFL
FROM scmcdr.scm_cc_{mon0}
WHERE m_day= '{day0}' AND IgnoreFlag='0' 
GROUP BY to_char(timestamp,'yyyy-mm-dd')
),
base_d1 AS (SELECT to_char(timestamp,'yyyy-mm-dd') AS cdr_date
,SUM(CASE WHEN accessflag IN('66') THEN 1 ELSE 0 END) MO_ATT
,SUM(CASE WHEN accessflag IN('66') AND basiccause IN('938') THEN 1 ELSE 0 END)AS MO_SUC
,SUM(CASE WHEN accessflag IN('66')  
AND basiccause IN('945','336','959','960','940','100','818','601','939','111','601')
AND internalcause IN ('4012','5030','5031') THEN 1 ELSE 0 END ) AS MO_BFL
,SUM(CASE WHEN accessflag IN('67') THEN 1 ELSE 0 END)MT_ATT
,SUM(CASE WHEN accessflag IN('67')  AND basiccause IN('941') THEN 1 ELSE 0 END) AS MT_SUC
,SUM(CASE WHEN accessflag IN('67')  AND basiccause IN('363','959','923','340','960','100','749','940','942','943','118','111','41','601','715') 
AND internalcause IN ('4012','5030','5031') 
OR (basiccause IN('813') AND internalcause is null) THEN 1 ELSE 0 END ) AS MT_BFL
FROM scmcdr.scm_cc_{mon1}
WHERE m_day= '{day1}' AND IgnoreFlag='0'  AND HOUR <= TO_CHAR(SYSDATE,'HH24')
GROUP BY to_char(timestamp,'yyyy-mm-dd')
)
SELECT *
FROM base_d0
UNION
SELECT *
FROM base_d1