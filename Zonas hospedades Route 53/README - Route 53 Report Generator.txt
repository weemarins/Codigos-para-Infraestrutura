Descrição
Este script Python utiliza a biblioteca Boto3 para interagir com o serviço Route 53 da AWS, listando todas as zonas hospedadas e seus respectivos registros. Ele gera um relatório em formato JSON contendo essas informações.

Funcionalidades:
Lista todas as zonas hospedadas no Route 53.
Lista todos os registros de cada zona hospedada.
Gera um arquivo route53_report.json com as zonas e seus registros.
Pré-requisitos
Antes de executar este script, é necessário ter o seguinte ambiente configurado:

Python 3.x instalado.

Boto3 instalado

AWS CLI instalado e configurado. O script requer que você tenha permissões adequadas para listar zonas e registros no Route 53.

Durante a configuração, será solicitado seu AWS Access Key, AWS Secret Key, região padrão e formato de saída. As permissões necessárias incluem:

route53:ListHostedZones
route53:ListResourceRecordSets

Como Executar

Certifique-se de que o AWS CLI está instalado e configurado corretamente com permissões para acessar o Route 53.

Execute o script a partir do terminal

O script processará todas as zonas hospedadas e criará um arquivo route53_report.json no diretório atual contendo os detalhes das zonas e seus registros.