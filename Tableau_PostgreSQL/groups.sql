--List All Groups

SELECT 
    g.id AS group_id,
    g.name AS group_name,
    g.domain_name,
    g.is_system,
    g.site_id
FROM groups g
ORDER BY g.name;

--Users in Each Group
SELECT 
    g.name AS group_name,
    u.name AS username,
    u.email,
    u.role,
    u.last_login
FROM groups g
JOIN group_users gu ON g.id = gu.group_id
JOIN users u ON gu.user_id = u.id
ORDER BY g.name, u.name;

--Role Distribution within Groups
SELECT 
    g.name AS group_name,
    u.role,
    COUNT(*) AS role_count
FROM groups g
JOIN group_users gu ON g.id = gu.group_id
JOIN users u ON gu.user_id = u.id
GROUP BY g.name, u.role
ORDER BY g.name, role_count DESC;



/*
    what groups is someone in
*/ 
select 
    * 
from group_users as gu 
    inner join users_view as uv on ( gu.user_id = uv.id )
    left outer join groups on ( gu.group_id = groups.id )
