[CmdletBinding()]
param(
    [string]$PythonPath,
    [switch]$SoloInstalarCLI
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$toolRoot = Join-Path $projectRoot '.tools/spec-kit'
$toolPython = Join-Path $toolRoot 'Scripts/python.exe'
$specify = Join-Path $toolRoot 'Scripts/specify.exe'

function Invoke-Checked {
    param([string]$Executable, [string[]]$Arguments)
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "El comando fallo con codigo $LASTEXITCODE : $Executable"
    }
}

# No sobrescribir instalaciones previas o configuraciones de otros agentes.
if (-not $SoloInstalarCLI) {
    foreach ($relativePath in @('.agents', '.codex')) {
        if (Test-Path -LiteralPath (Join-Path $projectRoot $relativePath)) {
            throw "Ya existe $relativePath. Revisar la instalacion antes de inicializar; puede usar -SoloInstalarCLI."
        }
    }
    $specifyRoot = Join-Path $projectRoot '.specify'
    if (Test-Path -LiteralPath $specifyRoot) {
        $ajenos = @(Get-ChildItem -LiteralPath $specifyRoot -File -Recurse | Where-Object {
            $_.FullName -ne (Join-Path $specifyRoot 'memory/constitution.md')
        })
        if ($ajenos.Count -gt 0) { throw 'Ya existe infraestructura .specify; revise su actualizacion antes de reinicializar.' }
    }
}

if (-not (Test-Path -LiteralPath $toolPython)) {
    if (-not $PythonPath) {
        $PythonPath = Join-Path $projectRoot '.venv/Scripts/python.exe'
    }
    if (-not (Test-Path -LiteralPath $PythonPath)) {
        throw 'Indique -PythonPath con un python.exe de Python 3.11 o superior.'
    }
    Invoke-Checked $PythonPath @('-c', 'import sys; assert sys.version_info >= (3,11), "Se requiere Python 3.11+"')
    Invoke-Checked $PythonPath @('-m', 'venv', $toolRoot)
}

# Fuente oficial y version fijada; entorno separado de las dependencias de Django.
Invoke-Checked $toolPython @('-m', 'pip', 'install', 'specify-cli @ git+https://github.com/github/spec-kit.git@v1.4.3')
Invoke-Checked $specify @('version')
if ($SoloInstalarCLI) { return }

Push-Location $projectRoot
$constitutionPath = Join-Path $projectRoot '.specify/memory/constitution.md'
$constitutionBytes = if (Test-Path -LiteralPath $constitutionPath) { [IO.File]::ReadAllBytes($constitutionPath) } else { $null }
try {
    Invoke-Checked $specify @('init', '--here', '--force', '--non-interactive', '--integration', 'codex', '--script', 'ps', '--ignore-agent-tools')
    Invoke-Checked $specify @('integration', 'status')
    foreach ($relativePath in @('.specify/templates', '.specify/scripts/powershell', '.agents/skills/speckit-specify/SKILL.md')) {
        if (-not (Test-Path -LiteralPath (Join-Path $projectRoot $relativePath))) {
            throw "Inicializacion incompleta: falta $relativePath"
        }
    }
    Write-Host 'Spec Kit instalado. Abra una nueva conversacion desde la raiz del repositorio y revise las skills speckit.'
    Write-Host 'La constitucion y los specs existentes se conservan. Consulte documentacion/FLUJO-SPEC-KIT.md.'
}
finally {
    if ($null -ne $constitutionBytes) { [IO.File]::WriteAllBytes($constitutionPath, $constitutionBytes) }
    Pop-Location
}
