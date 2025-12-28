--List All Workbooks
SELECT 
    w.id AS workbook_id,
    w.name AS workbook_name,
    w.project_id,
    p.name AS project_name,
    w.owner_id,
    u.name AS owner_name,
    w.created_at,
    w.updated_at
FROM workbooks w
JOIN projects p ON w.project_id = p.id
JOIN users u ON w.owner_id = u.id
ORDER BY w.name;

--Workbook Usage (Views)
SELECT 
    w.name AS workbook_name,
    COUNT(v.id) AS view_count
FROM workbooks w
JOIN views v ON w.id = v.workbook_id
GROUP BY w.name
ORDER BY view_count DESC;

--Workbooks by Project
SELECT 
    p.name AS project_name,
    COUNT(w.id) AS workbook_count
FROM workbooks w
JOIN projects p ON w.project_id = p.id
GROUP BY p.name
ORDER BY workbook_count DESC;


--Recently Updated Workbooks

SELECT 
    w.name AS workbook_name,
    u.name AS owner_name,
    w.updated_at
FROM workbooks w
JOIN users u ON w.owner_id = u.id
WHERE w.updated_at >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY w.updated_at DESC;

--Workbook Permissions
SELECT 
    w.name AS workbook_name,
    u.name AS user_name,
    cap.capability_name,
    cap.allowed
FROM workbooks w
JOIN permissions perms ON w.id = perms.workbook_id
JOIN users u ON perms.grantee_id = u.id
JOIN capabilities cap ON perms.capability_id = cap.id
ORDER BY w.name, u.name;
