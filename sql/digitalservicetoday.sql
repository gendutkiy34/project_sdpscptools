WITH base AS (select to_char(timestamp,'yyyy-mm-dd') DT,hour,
sum(CASE WHEN accessflag IN('68') then  1 else 0 end)attempt,
sum(case when accessflag IN('68') and basiccause in('852','963','123','949') then 1 else 0 end) success,
sum(case when accessflag IN('68') and basiccause in('100','961','962','810','297','804','288','948','293','950','111') and internalcause in('4012') then 1 else 0 end) INSF,
sum(case when accessflag IN('68') and basiccause in('100','961','962','810','297','804','288','948','293','950','111') and internalcause in('5030') then 1 else 0 end) UNSUBS,
sum(case when accessflag IN('68') and basiccause in('100','961','962','810','297','804','288','948','293','950','111') and internalcause in('5031') then 1 else 0 end) BLCK,
sum(case when accessflag IN('68') and basiccause in('100','961','962','810','297','804','288','948','293','950','111') and internalcause in('4010') then 1 else 0 end) SUSP,
sum(case when accessflag IN('68') and basiccause in('100','961','962','810','297','804','288','948','293','950','111') and internalcause in('3004','921','6022','2001','503','500','717') then 1 else 0 end) SYSFAIL,
sum(case when accessflag IN('68') and basiccause in('100','961','962','810','297','804','288','948','293','950','111') and internalcause in('9999') then 1 else 0 end) COMMITE,
sum(case when accessflag IN('68') and basiccause in('100','961','962','810','297','804','288','948','293','950','111') and internalcause NOT in('4012','5030','5031','4010','3004','921','6022','2001','503','500','717','9999') then 1 else 0 end) OTHER
FROM scmcdr.scm_cc_{mon} 
WHERE m_day = '{day}' AND accessflag in('68')  
GROUP BY to_char(timestamp,'yyyy-mm-dd'),hour)
SELECT dt,hour,attempt,success
,(insf+unsubs+blck+susp) BF
,(sysfail+commite+other) F
FROM base
ORDER BY hour
