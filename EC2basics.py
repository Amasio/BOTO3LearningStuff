#EC2 BASICS
import security_access_key
import boto3
import json

session = boto3.Session(
    aws_access_key_id=security_access_key.aws_access_key_id,
    aws_secret_access_key=security_access_key.aws_secret_access_key,
    region_name=security_access_key.region_name
)

ec2 = session.resource('ec2')
instance_name="new-ec2"

instance_id = None

#check is already exist
instances=ec2.instances.all()

#launch instance if isnt created
# Creazione di una nuova istanza EC2
instances = ec2.create_instances( 
    ImageId='ami-0d7a109bf30624c99',  # ID dell'AMI: sostituiscilo con un ID valido per la tua regione
    MinCount=1,  # Numero minimo di istanze da lanciare
    MaxCount=1,  # Numero massimo di istanze da lanciare
    InstanceType='t2.micro',  # Tipo di istanza, ad es. 't2.micro'
    KeyName='your-key-pair-name',  # Il nome della tua chiave SSH: sostituiscilo con il nome effettivo della tua chiave
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': instance_name
                },
            ]
        },
    ]
    # Puoi aggiungere altri parametri qui, come SecurityGroups, UserData, etc.
)
