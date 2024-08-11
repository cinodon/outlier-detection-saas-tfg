import csv
from models import User, WorkApp, UsersGroupUser, PermissionLevel, UserAppRole
from engine.engine import session


def fetch_data():
    # Realizar la consulta
    query = (
        session.query(
            #WorkApp.Name.label("WorkAppName"),
            WorkApp.Id.label("WorkAppId"),
            WorkApp.WorkAppCategoryId,
            UserAppRole.UserId,
            User.ManagerId,
            User.TypeOfWorkId,
            User.RoleId,
            UsersGroupUser.UsersGroupId,
            UserAppRole.PermissionLevelId,
            PermissionLevel.IsPrivileged.label("PermissionLevelIsPrivileged")
        )
        .select_from(WorkApp)
        .outerjoin(UserAppRole, UserAppRole.WorkAppId == WorkApp.Id)
        .outerjoin(User, UserAppRole.UserId == User.Id)
        .outerjoin(UsersGroupUser, UsersGroupUser.UserId == UserAppRole.UserId)
        .outerjoin(PermissionLevel, PermissionLevel.Id == UserAppRole.PermissionLevelId)
    )

    results = query.all()
    return results

def export_to_csv(filename, data):
    # Define the header based on your requirements
    header = [
        'WorkAppId', 'WorkAppCategoryId', 'UserId', 'ManagerId',
        'TypeOfWorkId', 'RoleId', 'UsersGroupId', 'PermissionLevelId',
        'PermissionLevelIsPrivileged'
    ]

    # Open the CSV file for writing
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(header)

        # Write the data
        for row in data:
            writer.writerow(row)

data = fetch_data()
export_to_csv('/app/files/output.csv', data)

while True:
    a = 0