import boto3
import json

# Inicializar cliente do Route 53
client = boto3.client('route53')

# Função para listar zonas hospedadas
def list_hosted_zones():
    zones = client.list_hosted_zones()
    return zones['HostedZones']

# Função para listar registros de uma zona
def list_records(zone_id):
    records = client.list_resource_record_sets(HostedZoneId=zone_id)
    return records['ResourceRecordSets']

# Função principal para gerar o relatório
def generate_report():
    report = {}

    # Listar todas as zonas hospedadas
    zones = list_hosted_zones()
    for zone in zones:
        zone_id = zone['Id'].split('/')[-1]
        zone_name = zone['Name']
        print(f"Processando zona: {zone_name}")

        # Listar todos os registros da zona
        records = list_records(zone_id)
        report[zone_name] = records

    # Salvar relatório em um arquivo JSON
    with open('route53_report.json', 'w') as outfile:
        json.dump(report, outfile, indent=4)

    print("Relatório gerado em route53_report.json")

# Executar a função principal
if __name__ == "__main__":
    generate_report()
