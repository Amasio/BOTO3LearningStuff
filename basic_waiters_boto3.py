import boto3
from botocore.exceptions import WaiterError

ec2 = boto3.client('ec2')
instance_id = 'id-della-tua-istanza'

# Avvia l'istanza
ec2.start_instances(InstanceIds=[instance_id])
print("Avvio dell'istanza in corso...")

# Ottieni il waiter
waiter = ec2.get_waiter('instance_running')

try:
    # Attendi che l'istanza sia in stato 'running'
    waiter.wait(Filters=[
        {
            'Name': 'ip-address',
            'Values': [
                '123.123.123.123',
            ]
        }],InstanceIds=[instance_id])
    print(f"L'istanza {instance_id} è ora in esecuzione.")
    # Qui puoi inserire ulteriori azioni da eseguire dopo che l'istanza è in esecuzione
except WaiterError as e:
    print(f"Errore: {e.message}")