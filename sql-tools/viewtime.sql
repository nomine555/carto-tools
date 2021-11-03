SET ANSI_NULLS on
set QUOTED_IDENTIFIER  ON
select     top 55
           CONVERT(VARCHAR(4),Aces.dbo.STUDIES_TABLE.STUDY_IDX) StudyID,	  
	   CONVERT(VARCHAR(10),CAST(CAST(Aces.dbo.STUDIES_TABLE.date AS Datetime) AS Date)) AS Date,    
           CONVERT(VARCHAR(9),Aces.dbo.SETUP_TABLE.NAME) Template,
           CONVERT(VARCHAR(9),Aces.dbo.STUDIES_TABLE.NAME) StudyName, 
           CONVERT(VARCHAR(15),Aces.dbo.STUDIES_TABLE.PHYSICIAN1) Physician,               
           CONVERT(VARCHAR(33),Aces.dbo.STUDIES_TABLE.NOTES) Comments, 
           CONVERT(VARCHAR(8),CAST(CAST(Aces.dbo.STUDIES_TABLE.START_TIME AS Datetime) AS Time)) AS Carto_Start,
           CONVERT(VARCHAR(9),Points.First_Point) AS map_start,           
           CONVERT(VARCHAR(9),RFTime.First_RF) AS rf_start,
           CONVERT(VARCHAR(9),RFTime.Last_RF) AS rf_end,
	   CONVERT(VARCHAR(9),Points2.Last_Point) AS validation_end,
	   CONVERT(VARCHAR(9),RFTime.TotalRFTime) AS TotalRFTime,
	   CONVERT(VARCHAR(9),RFTime.MeanRFTime) AS MeanRFTime,
	   CONVERT(VARCHAR(9),RFTime.numRFs) AS numRFs,
 	   CONVERT(VARCHAR(9),RFForce.CF_MEAN) AS meanForce,
           CONVERT(VARCHAR(9),RFForce.CF_STD) AS stdForce,
	   CONVERT(VARCHAR(9),Aces.dbo.PROCEDURES_TABLE.NAME) AS CASETYPE,
	   CONVERT(VARCHAR(9),Cath.names) AS catheters
from       Aces.dbo.STUDIES_TABLE
LEFT JOIN       Aces.dbo.SETUP_TABLE
ON         Aces.dbo.SETUP_TABLE.SETUP_IDX = Aces.dbo.STUDIES_TABLE.SETUP_IDX
LEFT JOIN	 Aces.dbo.PATIENTS_TABLE
ON	   Aces.dbo.PATIENTS_TABLE.IDX = Aces.dbo.STUDIES_TABLE.PATIENT_IDX
LEFT JOIN
( select   Aces.dbo.STUDIES_TABLE.STUDY_IDX,    
           CAST(CAST(MIN(Aces.dbo.POINTS_TABLE.ACQUISITION_TIME) AS Datetime)AS Time(0)) AS First_Point
  from     Aces.dbo.STUDIES_TABLE,
           Aces.dbo.MAPS_TABLE,
	       Aces.dbo.POINTS_TABLE
  where    Aces.dbo.STUDIES_TABLE.STUDY_IDX = Aces.dbo.MAPS_TABLE.STUDY_IDX
  and      Aces.dbo.MAPS_TABLE.MAP_IDX = Aces.dbo.POINTS_TABLE.MAP_IDX
  group by Aces.dbo.STUDIES_TABLE.STUDY_IDX
) AS Points
ON Points.STUDY_IDX = Aces.dbo.STUDIES_TABLE.STUDY_IDX
LEFT JOIN
( select   Aces.dbo.STUDIES_TABLE.STUDY_IDX,    
           CAST(CAST(MAX(Aces.dbo.POINTS_TABLE.ACQUISITION_TIME) AS Datetime)AS Time(0)) AS Last_Point
  from     Aces.dbo.STUDIES_TABLE,
           Aces.dbo.MAPS_TABLE,
	       Aces.dbo.POINTS_TABLE
  where    Aces.dbo.STUDIES_TABLE.STUDY_IDX = Aces.dbo.MAPS_TABLE.STUDY_IDX
  and      Aces.dbo.MAPS_TABLE.MAP_IDX = Aces.dbo.POINTS_TABLE.MAP_IDX
  group by Aces.dbo.STUDIES_TABLE.STUDY_IDX
) AS Points2
ON Points2.STUDY_IDX = Aces.dbo.STUDIES_TABLE.STUDY_IDX
LEFT JOIN

(
SELECT  IDX, 
        CAST(CAST(MIN(STARTTIME) AS Datetime)AS Time(0)) AS First_RF,
        CAST(CAST(MAX(STARTTIME) AS Datetime)AS Time(0)) AS Last_RF,
        SUM(RFTIME/1000)/60 AS TotalRFTime,
	     AVG(RFTIME)/1000 AS MeanRFTime,
	     COUNT(RFTIME) AS numRFs
FROM 
(
select DISTINCT 
           Aces.dbo.STUDIES_TABLE.STUDY_IDX AS IDX, 
			  Aces.dbo.RF_TABLE.RF_IDX, 
			  Aces.dbo.RF_TABLE.RF_TIME AS RFTIME, 
			  Aces.dbo.RF_TABLE.ABLATION_START_TIME AS STARTTIME
  from     Aces.dbo.STUDIES_TABLE,
           Aces.dbo.MAPS_TABLE,
	       Aces.dbo.RF_TABLE
  where    Aces.dbo.STUDIES_TABLE.STUDY_IDX = Aces.dbo.MAPS_TABLE.STUDY_IDX
  and	   Aces.dbo.RF_TABLE.MAP_IDX = Aces.dbo.MAPS_TABLE.MAP_IDX
) AS RFLIST
group by IDX


) AS RFTime
ON RFTime.IDX = Aces.dbo.STUDIES_TABLE.STUDY_IDX
LEFT JOIN
(
SELECT DISTINCT(Aces.dbo.STUDIES_TABLE.STUDY_IDX), CONFIG_MAIN_TABLE.PROCEDURE_IDX AS ptype,
			STUFF((
          			SELECT ',' + Aces.dbo.CONFIG_CONNECTOR_TABLE.CATHETER_NAME
          			FROM  Aces.dbo.CONFIG_CONNECTOR_TABLE
          			WHERE Aces.dbo.CONFIG_MAIN_TABLE.CONFIG_IDX = Aces.dbo.CONFIG_CONNECTOR_TABLE.CONFIG_IDX
          			AND Aces.dbo.CONFIG_CONNECTOR_TABLE.IS_IN_CONNECTOR_SETUP =1
          			FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'
						 ), 1, 1, '') as names
FROM Aces.dbo.STUDIES_TABLE,
     Aces.dbo.CONFIG_MAIN_TABLE,
     Aces.dbo.CONFIG_CONNECTOR_TABLE
WHERE
 	Aces.dbo.STUDIES_TABLE.SETUP_IDX = Aces.dbo.CONFIG_MAIN_TABLE.SETUP_IDX
AND
 	Aces.dbo.CONFIG_MAIN_TABLE.CONFIG_IDX = Aces.dbo.CONFIG_CONNECTOR_TABLE.CONFIG_IDX
) AS Cath
ON Cath.STUDY_IDX = Aces.dbo.STUDIES_TABLE.STUDY_IDX
LEFT JOIN
( select   Aces.dbo.STUDIES_TABLE.STUDY_IDX, 
           AVG(Aces.dbo.RF_TABLE.AVERAGE_CONTACT_FORCE) AS CF_MEAN,
           STDEV(Aces.dbo.RF_TABLE.AVERAGE_CONTACT_FORCE) AS CF_STD
  from     Aces.dbo.STUDIES_TABLE,
           Aces.dbo.MAPS_TABLE,
	   Aces.dbo.RF_TABLE
  where    Aces.dbo.STUDIES_TABLE.STUDY_IDX = Aces.dbo.MAPS_TABLE.STUDY_IDX
  and	   Aces.dbo.RF_TABLE.MAP_IDX = Aces.dbo.MAPS_TABLE.MAP_IDX
  AND    Aces.dbo.RF_TABLE.AVERAGE_CONTACT_FORCE > 0
  group by Aces.dbo.STUDIES_TABLE.STUDY_IDX

) AS RFForce
ON RFForce.STUDY_IDX = Aces.dbo.STUDIES_TABLE.STUDY_IDX
LEFT JOIN  Aces.dbo.PROCEDURES_TABLE
on  Aces.dbo.PROCEDURES_TABLE.PROCEDURE_IDX = Cath.ptype
ORDER BY Date DESC

