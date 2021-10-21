$Source = "\\ifrn.local\SYSVOL\ifrn.local\scripts\CNAT\dti12.png"
$Destination = "C:\Windows\Web\Wallpaper\Windows\"
$Item = "C:\Windows\Web\Wallpaper\Windows\dti12.png"

#Check destination path
if (Test-Path $Source)
{
    if (Test-Path $Item)
    {
    #then copy
    "Exist"
	$HashSource=(Get-FileHash $Source | Format-List -Property Hash)
	$HashDestination=(Get-FileHash $Destination | Format-List -Property Hash)

	if($HashSource -eq $HashDestination)
	{
		"Equal"
	}
	else
	{
		Copy-Item -Path $Source -Destination $Destination -Force
	}
    }
    else
    {
    #then copy
    Copy-Item -Path $Source -Destination $Destination -Force
    }
}