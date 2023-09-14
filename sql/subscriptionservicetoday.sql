SELECT DT,hour,MO_ATTEMPT,MO_success,MO_INSF+MO_UNKS+MO_BLCKLIST SMOBF,MO_SYSF+MO_PLUG SMOFAIL,
MT_ATTEMPT,MT_success,MT_INSF+MT_UNKS+MT_BLCKLIST SMTBF,MT_SYSF+MT_PLUG SMTFAIL
FROM (
	SELECT to_char(timestamp,'yyyy-mm-dd') DT,hour,
	SUM(CASE WHEN accessflag IN('72') AND internalcause IS NOT NULL THEN NVL(1,0) ELSE 0 END)MO_ATTEMPT,
	SUM(CASE WHEN accessflag IN('73') AND internalcause IS NOT NULL THEN NVL(1,0) ELSE 0 END)MT_ATTEMPT,
	SUM(CASE WHEN accessflag IN('72')  AND basiccause IN('987') THEN NVL(1,0) ELSE 0 END)MO_success,
	SUM(CASE WHEN accessflag IN('73')  AND basiccause IN('941') THEN NVL(1,0) ELSE 0 END)MT_success,
	SUM(CASE WHEN accessflag IN('72')  AND basiccause IN('945','336','959','960','940','100','818','601','939','111','601') AND internalcause IN ('4012') THEN NVL(1,0) ELSE 0 END)MO_INSF,
	SUM(CASE WHEN accessflag IN('73')  AND basiccause IN('363','959','923','340','960','100','749','940','942','943','118','111','41','601','715') AND internalcause IN ('4012') THEN NVL(1,0) ELSE 0 END)MT_INSF,
	SUM(CASE WHEN accessflag IN('72')  AND basiccause IN('945','336','959','960','940','100','818','601','939','111','601') AND internalcause IN ('5030') THEN NVL(1,0) ELSE 0 END)MO_UNKS,
	SUM(CASE WHEN accessflag IN('73')  AND basiccause IN('363','959','923','340','960','100','749','940','942','943','118','111','41','601','715') AND internalcause IN ('5030') THEN NVL(1,0) ELSE 0 END)MT_UNKS,
	SUM(CASE WHEN accessflag IN('72')  AND basiccause IN('945','336','959','960','940','100','818','601','939','111','601') AND internalcause IN ('3004','921','6022','2001','503','500','717','5031') THEN NVL(1,0) ELSE 0 END)MO_SYSF,
	SUM(CASE WHEN accessflag IN('73')  AND basiccause IN('363','959','923','340','960','100','749','940','942','943','118','111','41','601','715') AND internalcause IN ('3004','921','6022','2001','503','500','717','5031') THEN NVL(1,0) ELSE 0 END)MT_SYSF,
	SUM(CASE WHEN accessflag IN('72')  AND basiccause IN('945','336','959','960','940','100','818','601','939','111','601') AND internalcause IN ('4010') THEN NVL(1,0) ELSE 0 END)MO_PLUG,
	SUM(CASE WHEN accessflag IN('73')  AND basiccause IN('363','959','923','340','960','100','749','940','942','943','118','111','41','601','715') AND internalcause IN ('4010') THEN NVL(1,0) ELSE 0 END)MT_PLUG,
	SUM(CASE WHEN accessflag IN('72')  AND basiccause IN('945','336','959','960','940','100','818','601','939','111','601') AND internalcause IN('5031') THEN NVL(1,0) ELSE 0 END)MO_BLCKLIST,
	SUM(CASE WHEN accessflag IN('73')  AND basiccause IN('363','959','923','340','960','100','749','940','942','943','118','111','41','601','715') AND internalcause IN('5031') THEN NVL(1,0) ELSE 0 END)MT_BLCKLIST,
	SUM(CASE WHEN ((accessflag IN('72') AND basiccause IN('987')) or ( (accessflag IN('46') AND basiccause IN('808','809','850','112','361','817','762') AND NETWORKMODE='SUBSCRIPTIONBULK_M0'))) THEN to_number(callcharge,'9999.99') ELSE 0 END)+
	SUM(CASE WHEN ((accessflag IN('73') AND basiccause IN('941')) or ( (accessflag IN('46') AND basiccause IN('808','809','850','112','361','817','762') AND NETWORKMODE='SUBSCRIPTIONBULK_MT'))) AND FIRSTTIMETONE='ISCHARGABLE' THEN to_number(callcharge,'99999.99') ELSE 0 END) REVENUE
	FROM scmcdr.scm_cc_{mon} 
	WHERE m_day='{day}'
	AND accessflag IN('72','73','46') 
	GROUP BY to_char(timestamp,'yyyy-mm-dd'),hour order by HOUR asc
)