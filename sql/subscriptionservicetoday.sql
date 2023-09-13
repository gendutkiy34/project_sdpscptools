SELECT DT,hour,
SMOATTEMPT,SMOSUCCESS,SMOINSF+SMOUNKS+SMOBLCK SMOBF,SMOSYSF+SMOOTHER SMOFAIL,
SMOSR,SMTATTEMPT,SMTSUCCESS,SMTINSF+SMTUNKS+SMTBLCK SMTBF,SMTSYSF+SMTOTHER SMTFAIL
FROM (
	SELECT A.DT,hour,SUM(A.SMOchargecontent)+SUM(A.SMONochargeContent)+SUM(A.SMOINSF)+SUM(A.SMOUNKS)+SUM(A.SMOBLCK)+SUM(A.SMOSUSP)+SUM(A.SMOSYSF)+SUM(A.SMOCOMMIT_ERROR)+SUM(A.SMOOTHER) SMOATTEMPT,
	SUM(A.SMONochargeContent)+SUM(A.SMONochargeContent) SMOSUCCESS,SUM(A.SMOchargecontent)SMOchargecontent,
	SUM(A.SMONochargeContent)SMONochargeContent,SUM(A.SMOINSF)SMOINSF,SUM(A.SMOUNKS)SMOUNKS,SUM(A.SMOBLCK)SMOBLCK,
	SUM(A.SMOSUSP)SMOSUSP,SUM(A.SMOSYSF)SMOSYSF,SUM(A.SMOCOMMIT_ERROR)SMOCOMMIT_ERROR,SUM(A.SMOOTHER)SMOOTHER,	SUM(A.SMTchargecontent)+SUM(A.SMTNochargeContent)+SUM(A.SMTINSF)+SUM(A.SMTUNKS)+SUM(A.SMTBLCK)+SUM(A.SMTSUSP)+SUM(A.SMTSYSF)+SUM(A.SMTCOMMIT_ERROR)+SUM(A.SMTOTHER) SMTATTEMPT,
	SUM(A.SMTNochargeContent)+SUM(A.SMTNochargeContent) SMTSUCCESS,SUM(A.SMTchargecontent)SMTchargecontent,
	SUM(A.SMTNochargeContent)SMTNochargeContent,SUM(A.SMTINSF)SMTINSF,SUM(A.SMTUNKS)SMTUNKS,SUM(A.SMTBLCK)SMTBLCK,
	SUM(A.SMTSUSP)SMTSUSP,SUM(A.SMTSYSF)SMTSYSF,SUM(A.SMTCOMMIT_ERROR)SMTCOMMIT_ERROR,SUM(A.SMTOTHER)SMTOTHER
	FROM (
		SELECT TO_CHAR(timestamp,'yyyymmdd') DT,hour,offercode,
		SUM(CASE WHEN ((accessflag IN('72') AND basiccause IN('941')) or (accessflag IN('46') AND basiccause IN('808','809','850','112','361','817','762'))) AND FIRSTTIMETONE='ISCHARGABLE' AND callcharge!='0.0' THEN 1 ELSE 0 END)SMOchargecontent,
		SUM(CASE WHEN ((accessflag IN('72') AND basiccause IN('941')) or (accessflag IN('46') AND basiccause IN('808','809','850','112','361','817','762'))) AND FIRSTTIMETONE='ISCHARGABLE' AND callcharge='0.0' THEN 1 ELSE 0 END)SMONochargeContent,
		SUM(CASE WHEN accessflag IN('72') AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') AND INternalcause IN('4012') then 1 else 0 END)SMOINSF,
		SUM(CASE WHEN accessflag IN('72') AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') AND INternalcause IN('5030') then 1 else 0 END)SMOUNKS,
		SUM(CASE WHEN accessflag IN('72') AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') AND INternalcause IN('5031') then 1 else 0 END)SMOBLCK,
		SUM(CASE WHEN accessflag IN('72') AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') AND INternalcause IN('4010') then 1 else 0 END)SMOSUSP,
		SUM(CASE WHEN accessflag IN('72') AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') AND INternalcause IN('3004','921','6022','2001','503','500','717') then 1 else 0 END)SMOSYSF,
		SUM(CASE WHEN accessflag IN('72') AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') AND INternalcause IN('9999') then 1 else 0 END)SMOCOMMIT_ERROR,
		SUM(CASE WHEN accessflag IN('72') AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') AND INternalcause NOT IN('4012','5030','5031','4010','3004','921','6022','2001','503','500','717','9999') then 1 else 0 END) SMOOTHER,
		SUM(CASE WHEN ((accessflag IN('73') AND basiccause IN('941')) or (accessflag IN('46') AND basiccause IN('808','809','850','112','361','817','762'))) AND FIRSTTIMETONE='ISCHARGABLE' AND callcharge!='0.0' THEN 1 ELSE 0 END)SMTchargecontent,
		SUM(CASE WHEN ((accessflag IN('73') AND basiccause IN('941')) or (accessflag IN('46') AND basiccause IN('808','809','850','112','361','817','762'))) AND FIRSTTIMETONE='ISCHARGABLE' AND callcharge='0.0' THEN 1 ELSE 0 END)SMTNochargeContent,
		SUM(CASE WHEN accessflag IN('73') AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') AND INternalcause IN('4012') then 1 else 0 END)SMTINSF,
		SUM(CASE WHEN accessflag IN('73') AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') AND INternalcause IN('5030') then 1 else 0 END)SMTUNKS,
		SUM(CASE WHEN accessflag IN('73') AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') AND INternalcause IN('5031') then 1 else 0 END)SMTBLCK,
		SUM(CASE WHEN accessflag IN('73') AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') AND INternalcause IN('4010') then 1 else 0 END)SMTSUSP,
		SUM(CASE WHEN accessflag IN('73') AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') AND INternalcause IN('3004','921','6022','2001','503','500','717') then 1 else 0 END)SMTSYSF,
		SUM(CASE WHEN accessflag IN('73') AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') AND INternalcause IN('9999') then 1 else 0 END)SMTCOMMIT_ERROR,
		SUM(CASE WHEN accessflag IN('73') AND basiccause IN('363','909','923','340','960','100','749','940','942','943','118','111','41','601','715','846') AND INternalcause NOT IN('4012','5030','5031','4010','3004','921','6022','2001','503','500','717','9999') then 1 else 0 END) SMTOTHER
		FROM scmcdr.scm_cc_{mon} 
		WHERE m_day='{day}'
		GROUP BY TO_CHAR(timestamp,'yyyymmdd'),hour,offercode) A 
	GROUP BY A.DT,HOUR )
ORDER BY hour;

