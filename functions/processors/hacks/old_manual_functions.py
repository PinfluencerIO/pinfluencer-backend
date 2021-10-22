import json
import boto3
import os

DB_PARAMS = {
    'DATABASE_NAME': os.environ['DATABASE_NAME'],
    'DB_CLUSTER_ARN': os.environ['DB_CLUSTER_ARN'],
    'DB_SECRET_ARN': os.environ['DB_SECRET_ARN']
}

rds_client = boto3.client('rds-data')

COLUMNS_FOR_PRODUCT = ['id', 'name', 'description', 'image_s3_key', 'image', 'brand_id', 'brand_name']
COLUMNS_FOR_BRAND = ['id', 'name', 'bio', 'description', 'website', 'email', 'logo', 'auth_user_id']


def hack_get_brands(event):
    sql = "SELECT " + ', '.join(COLUMNS_FOR_BRAND) + " FROM brand"
    result = execute_query(sql, None)
    print(result)
    records = format_records(result['records'])
    print(records)
    return build_json_from_db_records(records, COLUMNS_FOR_BRAND)


def hack_get_brand_by_id(event):
    sql = "SELECT " + ', '.join(COLUMNS_FOR_BRAND) + " FROM brand where id = :id"
    id_ = event['pathParameters']['brand_id']
    print(f'sql {sql} for id {id_}')
    sql_parameters = [{'name': 'id', 'value': {'stringValue': id_}}]
    result = execute_query(sql, sql_parameters)
    return build_json_from_db_records(format_records(result['records']), COLUMNS_FOR_BRAND)


def hack_get_all_products_for_brand_by_id(event):
    sql = "SELECT " + ', '.join(COLUMNS_FOR_PRODUCT) + " FROM product where brand_id = :id"
    id_ = event['pathParameters']['brand_id']
    sql_parameters = [{'name': 'id', 'value': {'stringValue': id_}}]
    result = execute_query(sql, sql_parameters)
    return build_json_from_db_records(format_records(result['records']), COLUMNS_FOR_PRODUCT)


def hack_get_products(event):
    sql = "SELECT " + ', '.join(COLUMNS_FOR_PRODUCT) + " FROM product"
    result = execute_query(sql, None)
    return build_json_from_db_records(format_records(result['records']), COLUMNS_FOR_PRODUCT)


def hack_get_product_by_id(event):
    sql = "SELECT " + ', '.join(COLUMNS_FOR_PRODUCT) + " FROM product where id = :id"
    id_ = event['pathParameters']['product_id']
    sql_parameters = [{'name': 'id', 'value': {'stringValue': id_}}]
    result = execute_query(sql, sql_parameters)
    return build_json_from_db_records(format_records(result['records']), COLUMNS_FOR_PRODUCT)


def hack_brand_me(event):
    user = event['requestContext']['authorizer']['jwt']['claims']['cognito:username']
    sql = "SELECT " + ', '.join(COLUMNS_FOR_BRAND) + " FROM brand where auth_user_id = :id"
    parameter = [{'name': 'id', 'value': {'stringValue': user}}]
    result = execute_query(sql, parameter)
    body = format_records(result['records'])
    return build_json_from_db_records(body, COLUMNS_FOR_BRAND)


def hack_product_me(event):
    user = event['requestContext']['authorizer']['jwt']['claims']['cognito:username']
    print(user)
    sql = "SELECT id FROM brand WHERE auth_user_id=:id"
    parameter = [{'name': 'id', 'value': {'stringValue': user}}]
    records = execute_query(sql, parameter)
    print("!!!")
    print(records['records'])
    print("!!!")
    if len(records['records']) == 0:
        print(f"zero found for {user}")
        return {
            'statusCode': 200,
            'body': "no products"
        }

    id = format_records(records['records'])[0][0]
    print(f"the id is {id}")
    second_sql = "SELECT " + ', '.join(COLUMNS_FOR_PRODUCT) + " FROM product WHERE brand_id=:id"
    second_p = [{'name': 'id', 'value': {'stringValue': id}}]
    result = execute_query(second_sql, second_p)
    body = format_records(result['records'])
    return build_json_from_db_records(body, COLUMNS_FOR_PRODUCT)


def hack_brand_me_create(event):
    user = event['requestContext']['authorizer']['jwt']['claims']['cognito:username']
    sql = "SELECT id FROM brand WHERE auth_user_id=:auth_user_id"
    sql_parameters = [{'name': 'auth_user_id', 'value': {'stringValue': user}}]
    result = execute_query(sql, sql_parameters)
    print(result)
    if len(result['records']) >= 1:
        return {'message': 'this user is already associated with a brand', 'id': format_records(result['records'])[0][0]}
    else:
        return {'body': 'create'}


def build_json_from_db_records(body, cols):
    result = list()

    for rowIndex, row in enumerate(body):
        result.append({})
        for index, columnValue in enumerate(row):
            result[rowIndex][cols[index]] = columnValue

    print(result)

    return result


def execute_query(sql, sql_parameters=None):
    if sql_parameters is None:
        sql_parameters = []
    response = rds_client.execute_statement(
        secretArn=DB_PARAMS['DB_SECRET_ARN'],
        database=DB_PARAMS['DATABASE_NAME'],
        resourceArn=DB_PARAMS['DB_CLUSTER_ARN'],
        sql=sql,
        parameters=sql_parameters
    )

    return response


def format_field(field):
    if list(field.keys())[0] != 'isNull':
        return list(field.values())[0]
    else:
        return ""


def format_record(record):
    return [format_field(field) for field in record]


def format_records(records):
    return [format_record(record) for record in records]
