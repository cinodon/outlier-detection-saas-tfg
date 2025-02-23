SELECT
    uar."Id" AS UserAppRoleId,
    uar."WorkAppId" AS WorkAppId,
    wa."Name" AS WorkAppName,
    wa."WorkAppCategoryId" AS WorkAppCategoryId,
    uar."UserId" AS UserId,
    tow."Name" AS TypeOfWorkName,
    u."RoleId" AS UserRoleId,
    uar."PermissionLevelId" AS PermissionLevelId,
    pl."IsPrivileged" AS PermissionLevelIsPrivileged
FROM
    api."UserAppRoles" uar
LEFT JOIN
    api."WorkApps" wa ON uar."WorkAppId" = wa."Id"
LEFT JOIN
    api."Users" u ON uar."UserId" = u."Id"
LEFT JOIN
    api."PermissionLevels" pl ON uar."PermissionLevelId" = pl."Id"
LEFT JOIN
    api."TypeOfWorks" tow ON u."TypeOfWorkId" = tow."Id"
WHERE
    uar."WorkAppId" != '63ae5646-1edf-4beb-90a8-1f002140c6f0';