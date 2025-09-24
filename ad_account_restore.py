from ldap3 import Server, Connection, ALL, MODIFY_REPLACE

# AD connection details
AD_SERVER = "your.domain.controller"
AD_USER = "DOMAIN\\Administrator"  # Or use UPN format: user@domain.local
AD_PASSWORD = "YourPassword"
SEARCH_BASE = "DC=your,DC=domain,DC=com"

# Connect to AD
server = Server(AD_SERVER, get_info=ALL)
conn = Connection(server, user=AD_USER, password=AD_PASSWORD, auto_bind=True)

# Search for deleted user accounts
conn.search(
    search_base=SEARCH_BASE,
    search_filter="(isDeleted=TRUE)",
    search_scope="subtree",
    attributes=["distinguishedName", "lastKnownParent", "sAMAccountName"]
)

if not conn.entries:
    print("No deleted accounts found.")
else:
    for entry in conn.entries:
        dn = entry.distinguishedName.value
        parent = entry.lastKnownParent.value if "lastKnownParent" in entry else None
        sam = entry.sAMAccountName.value if "sAMAccountName" in entry else None

        print(f"Found deleted account: {sam} ({dn})")

        if parent:
            # Restore by moving object back to last known parent
            new_dn = f"CN={sam},{parent}"
            success = conn.modify_dn(dn, f"CN={sam}", new_superior=parent)
            if success:
                print(f"Restored {sam} to {parent}")
            else:
                print(f"Failed to restore {sam}: {conn.result}")
        else:
            print(f"Skipping {sam}, no lastKnownParent found.")

conn.unbind()