import boto3

region_name = 'us-east-1'
profile_name = "thedasbot"
resource = 'dynamodb'
table_name = 'users'
field_name = 'item'

session = boto3.Session(profile_name=profile_name, region_name=region_name)
client = session.client('dynamodb')
boto3.setup_default_session(profile_name=profile_name)

dynamodb = boto3.resource(resource, region_name=region_name)
table = dynamodb.Table(table_name)

def clearUser(id) -> bool:
    try:
        client.delete_item(TableName=table_name, Key={ 'id': { 'N': str(id) } }, Expected={ 'id': { "Exists": True, "Value": { "N": str(id)} } })
    except:
        return False
    else:
        return True

def getUser(id) -> str:
    try:
        result = client.get_item(TableName=table_name, Key={ 'id': { 'N': str(id) } })
    except:
        return None

    if "Item" in result:
        return result["Item"][field_name]["S"]
    return None

def setUser(id, item) -> str:
    try:
        result = client.put_item(TableName='users', Item={'id': { 'N': str(id) }, field_name: { 'S': str(item) } })
    except:
        return None
    
    if result['ResponseMetadata']['HTTPStatusCode'] == 200:
        return item
    return None
