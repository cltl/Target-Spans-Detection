SELECT fileName, listNumber, assignmentId, hitId, workerId, origin, timestamp, partId, questionId, answer::TEXT, (data->>'ID') as ID, (data->>'dataset') as dataset, (data->>'text') as text, (data->>'tokens') as tokens, (data->>'label') as label, (data->>'redirectUrl') as redirectUrl, id FROM (
	(SELECT * FROM Results WHERE experimentType='TargetSpanDetectionExperiment') as tmp1
	LEFT OUTER JOIN Questions USING (QuestionId)
	LEFT OUTER JOIN Groups USING (PartId)
) as tmp
WHERE LingoExpModelId = 206
ORDER BY partId, questionId, workerId