SELECT
    uar."WorkAppId" AS WorkAppId,
    wa."WorkAppCategoryId" AS WorkAppCategoryId,
    uar."UserId" AS UserId,
    u."ManagerId" AS UserManagerId,
    u."TypeOfWorkId" AS UserTypeOfWorkId,
    u."RoleId" AS UserRoleId,
    uar."PermissionLevelId" AS PermissionLevelId,
    pl."IsPrivileged" AS PermissionLevelIsPrivileged,
    ARRAY_AGG(ugu."UsersGroupId") AS UsersGroupIds
FROM
    api."UserAppRoles" uar
LEFT JOIN
    api."WorkApps" wa ON uar."WorkAppId" = wa."Id"
LEFT JOIN
    api."Users" u ON uar."UserId" = u."Id"
LEFT JOIN
    api."PermissionLevels" pl ON uar."PermissionLevelId" = pl."Id"
LEFT JOIN
    api."UsersGroupUsers" ugu ON uar."UserId" = ugu."UserId"
WHERE
    uar."WorkAppId" != '63ae5646-1edf-4beb-90a8-1f002140c6f0'
GROUP BY
    uar."WorkAppId",
    wa."WorkAppCategoryId",
    uar."UserId",
    u."ManagerId",
    u."TypeOfWorkId",
    u."RoleId",
    uar."PermissionLevelId",
    pl."IsPrivileged";