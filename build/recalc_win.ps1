# Recalculate an .xlsx via Excel COM and report any formula errors.
#
# The xlsx skill's recalc.py drives LibreOffice through a Unix-domain socket,
# which does not exist on Windows. This does the same job with the Excel that is
# already installed: full rebuild, save, then scan formula cells for errors.
#
# Uses SpecialCells to visit only formula cells rather than the whole UsedRange,
# which keeps the COM round-trips down.
#
# Usage: powershell -ExecutionPolicy Bypass -File build/recalc_win.ps1 <xlsx>

param([Parameter(Mandatory = $true)][string]$Path)

$full = (Resolve-Path $Path).Path
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false

$xlFormulas = -4123
$xlErrors = 16

try {
    $wb = $excel.Workbooks.Open($full)
    $excel.CalculateFullRebuild()
    $wb.Save()

    $formulaCount = 0
    $errorCells = @()

    foreach ($ws in $wb.Worksheets) {
        $formulas = $null
        try { $formulas = $ws.Cells.SpecialCells($xlFormulas) } catch { }
        if ($formulas) { $formulaCount += $formulas.Count }

        $errs = $null
        try { $errs = $ws.Cells.SpecialCells($xlFormulas, $xlErrors) } catch { }
        if ($errs) {
            foreach ($c in $errs) {
                $errorCells += "$($ws.Name)!$($c.Address($false, $false))  <-  $($c.Formula)"
            }
        }
    }

    $wb.Close($true)

    [pscustomobject]@{
        status         = if ($errorCells.Count -eq 0) { "success" } else { "errors_found" }
        total_formulas = $formulaCount
        total_errors   = $errorCells.Count
    } | ConvertTo-Json

    if ($errorCells.Count -gt 0) {
        Write-Output ""
        Write-Output "Error cells:"
        $errorCells | ForEach-Object { Write-Output "  $_" }
    }
}
finally {
    $excel.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
}
