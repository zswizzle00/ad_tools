# Import AD module if not already loaded
Import-Module ActiveDirectory

# Define a time filter (example: accounts created in the last 7 days)
$StartDate = (Get-Date).AddDays(-7)

# Query AD accounts created after $StartDate
Get-ADUser -Filter { WhenCreated -ge $StartDate } -Properties WhenCreated |
    Select-Object SamAccountName, Name, WhenCreated |
    Sort-Object WhenCreated -Descending
