param([long]$TargetWindow)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
Add-Type -Path 'C:/Windows/Microsoft.NET/Framework64/v4.0.30319/WPF/UIAutomationTypes.dll'
Add-Type -Path 'C:/Windows/Microsoft.NET/Framework64/v4.0.30319/WPF/UIAutomationClient.dll'
$root = [System.Windows.Automation.AutomationElement]::FromHandle([IntPtr]$TargetWindow)
$walker = [System.Windows.Automation.TreeWalker]::ControlViewWalker
$queue = New-Object System.Collections.Queue
$queue.Enqueue(@($root,0))
$nodes = New-Object System.Collections.ArrayList
$deadline = [DateTime]::UtcNow.AddSeconds(8)
while ($queue.Count -gt 0 -and $nodes.Count -lt 120 -and [DateTime]::UtcNow -lt $deadline) {
    $entry = $queue.Dequeue()
    $element = $entry[0]; $depth = [int]$entry[1]
    $type = $element.Current.ControlType.ProgrammaticName
    $name = ''
    $skipType = $type -in @('ControlType.Edit','ControlType.Document','ControlType.List','ControlType.ListItem','ControlType.Tree','ControlType.TreeItem','ControlType.DataGrid','ControlType.DataItem','ControlType.ComboBox')
    if (-not $skipType) {
        $name = [string]$element.Current.Name
        if ($name -match '(?i)hostid|machine.?id|机器码|MAC.?address|SIGN\s*=|许可证|license|(?<![0-9A-Fa-f])(?:[0-9A-Fa-f]{2}[-:]){5}[0-9A-Fa-f]{2}') {
            $name = '[LICENSE_OR_IDENTIFIER_TEXT_NOT_RECORDED]'
        } else {
            $name = $name -replace '(?i)C:[\\/]+Users[\\/]+[^\s<>"'']+', '[PROFILE_PATH_REDACTED]'
            if ($name.Length -gt 1500) { $name = $name.Substring(0,1500) + '[TRUNCATED]' }
        }
    } else { $name = '[VALUE_OR_FILE_LIST_NOT_READ]' }
    [void]$nodes.Add([pscustomobject]@{depth=$depth;type=$type;name=$name})
    if ($depth -lt 4 -and -not $skipType) {
        $child = $walker.GetFirstChild($element)
        $children = 0
        while ($null -ne $child -and $children -lt 40) {
            $queue.Enqueue(@($child,$depth+1)); $children++
            $child = $walker.GetNextSibling($child)
        }
    }
}
[pscustomobject]@{status='READ_ONLY';nodes=@($nodes.ToArray());invoked_controls=0;edited_values=0} | ConvertTo-Json -Depth 7 -Compress
