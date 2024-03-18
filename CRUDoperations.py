#credential test
import security_access_key
import boto3

session = boto3.Session(
    aws_access_key_id=security_access_key.aws_access_key_id,
    aws_secret_access_key=security_access_key.aws_secret_access_key,
    region_name=security_access_key.region_name
)

s3 = session.resource('s3')

#il nome dei bucket deve essere tutto in minuscolo
bucket_name="altro-bucket-da-boto3"
all_my_bycket=[bucket.name for bucket in s3.buckets.all()]

######VERIFICA E CREAZIONE DEL BUCKET ########
if bucket_name not in all_my_bycket:
	print(f"'{bucket_name}' bucket dose not exist, creating...")
	s3.create_bucket(Bucket=bucket_name)
	print(f"'{bucket_name}' è stato creato")
else:
	print("bucket gia esistente")

#######Creation and upload of files.#######
file1= 'file1.txt'
lista_file = ['file2.txt', 'file3.txt']  # e così via fino a file10.txt

#upload
s3.Bucket(bucket_name).upload_file(Filename=file1, Key=file1)
#in key indichi dove e come vuoi che il seguente file venga salvato
#s3.Bucket(bucket_name).upload_file(filename=file1, key=pathInbucket/file_1_with_another_name)
for file_name in lista_file:
    s3.Bucket(bucket_name).upload_file(Filename=file_name, Key='ListDirectory/'+ file_name)

#READ
obj=s3.Object(bucket_name, file1) #1) crei il riferimento
response = obj.get()# 2) recuperi l' oggetto in se tramite API GET.(ovvero un file json con vari dati della richiesta +body)
body = response['Body'].read()#3)accediamo al body
#oppure con singolo comando
onelinebody=obj.get()['Body'].read()
print(body)

#update file1 with the contenet of file2
s3.Object(bucket_name, file1).put(Body=open("file2.txt", 'rb'))#file2 is in my pc not in aws
onelinebody=obj.get()['Body'].read()
print(onelinebody)

#Delete object
s3.Object(bucket_name, file1).delete()
#Delete object into a directory
objects_to_delete = [] #this list will be full with all the objects with the prefix ListDirectory/ <-(so all file in subdirectory)
for obj in s3.Bucket(bucket_name).objects.filter(Prefix="ListDirectory/"):
    objects_to_delete.append({'Key': obj.key})

if objects_to_delete:
    s3.Bucket(bucket_name).delete_objects(Delete={'Objects': objects_to_delete})

#delete bucket
bucket = s3.Bucket(bucket_name)
bucket.delete()