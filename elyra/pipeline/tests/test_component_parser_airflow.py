#
# Copyright 2018-2021 Elyra Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
import os
from types import SimpleNamespace

import jupyter_core.paths

from elyra.pipeline.component import FilesystemComponentReader
from elyra.pipeline.component import UrlComponentReader
from elyra.pipeline.component_parser_airflow import AirflowComponentParser
from elyra.pipeline.component_registry import ComponentRegistry

COMPONENT_CATALOG_DIRECORY = os.path.join(jupyter_core.paths.ENV_JUPYTER_PATH[0], 'components')


def _get_resource_path(filename):
    root = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    resource_path = os.path.join(root, 'resources', 'components', filename)

    return resource_path


def test_component_registry_can_load_components_from_catalog():
    component_registry_location = os.path.join(COMPONENT_CATALOG_DIRECORY, 'airflow_component_catalog.json')
    component_parser = AirflowComponentParser()
    component_registry = ComponentRegistry(component_registry_location, component_parser)

    components = component_registry.get_all_components()
    assert len(components) > 0


def test_parse_airflow_component_file():
    entry = {
        'id': 'test-operator_TestOperator',
        'name': 'Test Operator',
        'type': FilesystemComponentReader.type,
        'location': _get_resource_path('airflow_test_operator.py'),
        'adjusted_id': ''
    }
    component_entry = SimpleNamespace(**entry)

    parser = AirflowComponentParser()
    component = parser.parse(component_entry)[0]
    properties = ComponentRegistry.to_canvas_properties(component)

    properties_json = json.loads(properties)

    assert properties_json['current_parameters']['test_string_no_default'] == ''
    assert properties_json['current_parameters']['test_string_default_value'] == 'default'
    assert properties_json['current_parameters']['test_string_default_empty'] == ''

    assert properties_json['current_parameters']['test_bool_default'] is False
    assert properties_json['current_parameters']['test_bool_false'] is False
    assert properties_json['current_parameters']['test_bool_true'] is True

    assert properties_json['current_parameters']['test_int_default'] == 0
    assert properties_json['current_parameters']['test_int_zero'] == 0
    assert properties_json['current_parameters']['test_int_non_zero'] == 1

    assert properties_json['current_parameters']['test_dict_default'] == ''  # {}
    assert properties_json['current_parameters']['test_list_default'] == ''  # []


def test_parse_airflow_component_url():
    entry = {
        'id': 'bash-operator_BashOperator',
        'name': 'Bash Operator',
        'type': UrlComponentReader.type,
        'location': 'https://raw.githubusercontent.com/apache/airflow/1.10.15/airflow/operators/bash_operator.py',  # noqa: E501
        'adjusted_id': ''
    }
    component_entry = SimpleNamespace(**entry)

    parser = AirflowComponentParser()
    component = parser.parse(component_entry)[0]
    properties = ComponentRegistry.to_canvas_properties(component)

    properties_json = json.loads(properties)

    assert properties_json['current_parameters']['bash_command'] == ''
    assert properties_json['current_parameters']['xcom_push'] is False
    assert properties_json['current_parameters']['env'] == ''  # {}
    assert properties_json['current_parameters']['output_encoding'] == 'utf-8'
