--Workbooks with Connected Data Sources
SELECT 
    w.id AS workbook_id,
    w.name AS workbook_name,
    u.name AS workbook_owner,
    p.name AS project_name,
    ds.id AS datasource_id,
    ds.name AS datasource_name,
    du.name AS datasource_owner,
    w.created_at AS workbook_created,
    w.updated_at AS workbook_updated,
    ds.created_at AS datasource_created,
    ds.updated_at AS datasource_updated
FROM workbooks w
JOIN workbook_datasources wds ON w.id = wds.workbook_id
JOIN datasources ds ON wds.datasource_id = ds.id
JOIN users u ON w.owner_id = u.id
JOIN users du ON ds.owner_id = du.id
JOIN projects p ON w.project_id = p.id
ORDER BY w.name, ds.name;

--Count of Data Sources per Workbook
SELECT 
    w.name AS workbook_name,
    COUNT(wds.datasource_id) AS datasource_count
FROM workbooks w
JOIN workbook_datasources wds ON w.id = wds.workbook_id
GROUP BY w.name
ORDER BY datasource_count DESC;

--Data Sources by Project (via Workbooks)

SELECT 
    p.name AS project_name,
    ds.name AS datasource_name,
    COUNT(w.id) AS workbook_count
FROM datasources ds
JOIN workbook_datasources wds ON ds.id = wds.datasource_id
JOIN workbooks w ON wds.workbook_id = w.id
JOIN projects p ON w.project_id = p.id
GROUP BY p.name, ds.name
ORDER BY workbook_count DESC;

--Recently Updated Workbooks and Their Data Sources
SELECT 
    w.name AS workbook_name,
    ds.name AS datasource_name,
    w.updated_at AS workbook_updated,
    ds.updated_at AS datasource_updated
FROM workbooks w
JOIN workbook_datasources wds ON w.id = wds.workbook_id
JOIN datasources ds ON wds.datasource_id = ds.id
WHERE w.updated_at >= CURRENT_DATE - INTERVAL '30 days'
   OR ds.updated_at >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY w.updated_at DESC, ds.updated_at DESC;


