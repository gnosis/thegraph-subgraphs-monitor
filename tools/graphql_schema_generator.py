import os

import logging

# Configure logs format
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO)


def generate_schema(schema_info):
    """
    Generate a Graphql schema from a Graphql endpoint.
    That would be use later as a Python module to request Graphql data

    More information https://pypi.org/project/sgqlc/
    """


    # 1. Get Graphql JSON schema
    introspection_command = f"python -m sgqlc.introspection \
                             --exclude-deprecated \
                             --exclude-description \
                             {schema_info['graphql_endpoint']} \
                             {schema_info['schema_name']}.json"
    os.system(introspection_command)

    # 2. Generate Graphql Python schema from the JSON schema
    graphql_schema_generator_command = f"sgqlc-codegen {schema_info['schema_name']}.json {schema_info['schema_name']}.py"
    os.system(graphql_schema_generator_command)

    # 3. Move Graphql Python schema to schemas folder
    move_py_schema_cmd = f"mv {schema_info['schema_name']}.py {schema_info['schemas_dir']}"
    os.system(move_py_schema_cmd)

    # 4. Remove temporal files
    remove_json_schema_cmd = f"rm {schema_info['schema_name']}.json"
    os.system(remove_json_schema_cmd)


if __name__ == '__main__':

    # Project directory (abspath returns a normalized absolutized version)
    file_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(file_dir, os.pardir))
    schemas_dir = os.path.join(project_dir, 'graphql_schemas')

    # Info to download the Thegraph schema
    schema_info = {
        'schema_name': 'subgraph_status_schema',
        'graphql_endpoint': 'https://api.thegraph.com/index-node/graphql',
        'schemas_dir': schemas_dir
    }

    # Generate Thegraph status endpoint schema
    generate_schema(schema_info=schema_info)

    logging.info(f"Schema {schema_info['schema_name']} generated")
