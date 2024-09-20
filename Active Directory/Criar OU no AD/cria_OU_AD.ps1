# Caminho do arquivo contendo os nomes das OUs
$caminhoLista = "C:\caminho\para\sua\lista_de_OUs.txt"

# Verificar se o arquivo existe
if (-not (Test-Path $caminhoLista -PathType Leaf)) {
    Write-Host "Arquivo não encontrado."
    exit
}

# Ler a lista de nomes das OUs do arquivo
$listaOUs = Get-Content $caminhoLista

# Loop através dos nomes das OUs na lista
foreach ($nomeOU in $listaOUs) {
    # Verificar se a OU já existe no Active Directory
    if (-not (Get-ADOrganizationalUnit -Filter {Name -eq $nomeOU})) {
        # Criar a nova OU no Active Directory
        New-ADOrganizationalUnit -Name $nomeOU -Path "OU=NomeDaOUPai,DC=dominio,DC=com" -Confirm:$false
        Write-Host "OU '$nomeOU' criada com sucesso."
    } else {
        Write-Host "OU '$nomeOU' já existe. Ignorando a criação."
    }
}
