SELECT
    wa."Name" AS "WorkAppName",
    wa."Id" AS "WorkAppId",
    wa."WorkAppCategoryId",
    uar."UserId",
    u."ManagerId",
    u."TypeOfWorkId",
    u."RoleId",
    ugu."UsersGroupId",
    uar."PermissionLevelId",
    pl."IsPrivileged" AS "PermissionLevelIsPrivileged"
FROM
    api."WorkApps" wa
LEFT JOIN
    api."UserAppRoles" uar ON uar."WorkAppId" = wa."Id"
LEFT JOIN
    api."Users" u ON uar."UserId" = u."Id"
LEFT JOIN
    api."UsersGroupUsers" ugu ON ugu."UserId" = uar."UserId"
LEFT JOIN
    api."PermissionLevels" pl ON pl."Id" = uar."PermissionLevelId";