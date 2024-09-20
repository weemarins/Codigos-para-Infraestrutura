# Caminho da nova OU para onde os usuários serão movidos
$novaOU = "OU=NovosUsuarios,DC=dominio,DC=com"

# Caminho do arquivo contendo os endereços de e-mail dos usuários
$caminhoLista = "C:\caminho\para\sua\lista_de_emails.txt"

# Verificar se o arquivo existe
if (-not (Test-Path $caminhoLista -PathType Leaf)) {
    Write-Host "Arquivo não encontrado."
    exit
}

# Ler a lista de endereços de e-mail do arquivo
$listaEmails = Get-Content $caminhoLista

# Loop através dos endereços de e-mail na lista
foreach ($email in $listaEmails) {
    # Encontrar o usuário no AD com base no endereço de e-mail
    $usuarioAD = Get-ADUser -Filter {EmailAddress -eq $email} -Properties DistinguishedName

    if ($usuarioAD -ne $null) {
        # Mover o usuário para a nova OU
        Move-ADObject -Identity $usuarioAD.DistinguishedName -TargetPath $novaOU -Confirm:$false
        Write-Host "Usuário com e-mail $email movido com sucesso para a nova OU."
    } else {
        Write-Host "Usuário com e-mail $email não encontrado."
    }
}
