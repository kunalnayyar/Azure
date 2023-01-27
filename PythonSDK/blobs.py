import os,uuid
from dotenv import load_dotenv, dotenv_values  
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient,BlobClient,ContainerClient
#config = load_dotenv()
config = dotenv_values(".env")

try:
    print("Starting up")
    #print(config['AZURE_STORAGE_CONNECTION_STRING'])
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(config['AZURE_STORAGE_CONNECTION_STRING'])

    # Create a unique name for the container
    #container_name = str(uuid.uuid4())
    container_name = str('photos4')

    # Create the container
    container_client = blob_service_client.create_container(container_name)

    local_file_name = "docs-and-friends-selfie-stick.png"
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    blob_client.upload_blob(local_file_name)
    print("Uploading to azure storage...")
    print("\nListing blobs...")

    # List the blobs in the container
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)
    
    # Clean up
    print("\nPress the Enter key to begin clean up")
    input()

    print("Deleting blob container...")
    container_client.delete_container()
    print("Done")
    print("\nListing Containers...")

    containers = blob_service_client.list_containers(include_metadata=True)
    for container in containers:
        print(container['name'], container['metadata'])

except Exception as ex:
    print('Exception: ',ex)
