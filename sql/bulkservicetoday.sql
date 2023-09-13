WITH base AS (select to_char(timestamp,'yyyy-mm-dd') dt,hour,
SUM(CASE WHEN accessflag IN('66') THEN 1 ELSE 0 END) MO_ATTEMPT,
SUM(CASE WHEN accessflag IN('66') and basiccause IN('938') THEN 1 ELSE 0 END)MO_success,
SUM(CASE WHEN accessflag IN('66')  and basiccause IN('945','336','959','960','940','100','818','601','939','111','601') AND internalcause IN ('4012') THEN 1 ELSE 0 END)MO_INSF,
SUM(CASE WHEN accessflag IN('66')  and basiccause IN('945','336','959','960','940','100','818','601','939','111','601') AND internalcause IN ('5030') THEN 1 ELSE 0 END)MO_UNKS,
SUM(CASE WHEN accessflag IN('66')  and basiccause IN('945','336','959','960','940','100','818','601','939','111','601') AND internalcause IN ('5031') THEN 1 ELSE 0 END)MO_BLCKLIST,
SUM(CASE WHEN accessflag IN('66')  and basiccause IN('945','336','959','960','940','100','818','601','939','111','601') AND internalcause IN ('3004','921','6022','2001','503','500','717') THEN 1 ELSE 0 END)MO_SYSF,
SUM(CASE WHEN accessflag IN('66')  and basiccause IN('945','336','959','960','940','100','818','601','939','111','601') AND (internalcause not IN ('4012','5030','3004','921','6022','2001','503','500','717','5031')or internalcause IS NULL) THEN 1 ELSE 0 END) MO_OTHER_ERROR,
SUM(CASE WHEN accessflag IN('67') THEN 1 ELSE 0 END)MT_ATTEMPT,
SUM(CASE WHEN accessflag IN('67')  and basiccause IN('941') THEN 1 ELSE 0 END)MT_success,
SUM(CASE WHEN accessflag IN('67')  and basiccause IN('363','959','923','340','960','100','749','940','942','943','118','111','41','601','715') AND internalcause IN ('4012') THEN 1 ELSE 0 END)MT_INSF,
SUM(CASE WHEN accessflag IN('67')  and basiccause IN('363','959','923','340','960','100','749','940','942','943','118','111','41','601','715') AND internalcause IN ('5030') THEN 1 ELSE 0 END)MT_UNKS,
SUM(CASE WHEN accessflag IN('67')  and basiccause IN('363','959','923','340','960','100','749','940','942','943','118','111','41','601','715') AND internalcause IN ('5031') THEN 1 ELSE 0 END)MT_BLCKLIST,
SUM(CASE WHEN accessflag IN('67')  and basiccause IN('813') AND internalcause is null THEN 1 ELSE 0 END)MT_CPINA,
SUM(CASE WHEN accessflag IN('67')  and basiccause IN('363','959','923','340','960','100','749','940','942','943','118','111','41','601','715') AND internalcause IN ('3004','921','6022','2001','503','500','717') THEN 1 ELSE 0 END)MT_SYSF,
SUM(CASE WHEN accessflag IN('67')  and basiccause IN('998','363','959','923','340','960','100','749','940','942','943','118','111','41','601','715') AND (internalcause not IN ('4012','5030','3004','921','6022','2001','503','500','717','5031') or internalcause IS NULL) THEN 1 ELSE 0 END) MT_OTHER_ERROR
FROM scmcdr.scm_cc_{mon} where m_day='{day}' and IgnoreFlag='0'
GROUP BY to_char(timestamp,'yyyy-mm-dd') ,hour)
SELECT dt,hour,mo_attempt,mo_success,(MO_INSF+MO_UNKS+MO_BLCKLIST) mo_bf, (MO_SYSF+MO_OTHER_ERROR) mo_fail
,MT_ATTEMPT,MT_success,(MT_INSF+MT_UNKS+MT_BLCKLIST+MT_CPINA) MT_BF,(MT_SYSF+MT_OTHER_ERROR) MT_FAIL
FROM base
ORDER BY hour