# -*- coding: utf-8 -*-
import requests
import json


def fetch_data(city="bangalore"):
    """ Gets AQI data for bangalore from api.waqi.info site. """
    token = "22a7ea10a287c7d9ff26771099a975f48db68e52"  # AQI api token
    url = "http://api.waqi.info/feed/{0}/?token={1}".format(city, token)
    response = requests.get(url)
    return response.json()


def generate_data():
    """ Creates a demo sensor data json in the following format.
    {
        'refCatalogueSchemaRelease': '',
        'data_schema': {'city': u'BWSSB, Bangalore',
                 'co': 4,
                 'h': 55,
                 'p': 1009,
                 'so2': 2.2,
                 'geo': [77.5945627, 12.9715987],
                 'no2': 12.8},
        'accessMechanism': {},
        'tags': ['virtual_sensor', 'test_sensor'],
        'refCatalogueSchema': '',
        'provider': {'website': 'http://aqicn.org/',
              'name': 'CPCB - India Central Pollution Control Board'},
        'owner': {'name': 'harish'},
        'id': 'virtual_air_pollution_device8191'
    }
    """
    api_json = fetch_data()
    data = dict()
    data["id"] = "virtual_air_pollution_device_" + str(api_json["data"]["idx"])
    data["owner"] = {"name": "harish"}
    data["provider"] = {
        "name": "CPCB - India Central Pollution Control Board",
        "website": "http://aqicn.org/"}
    data["refCatalogueSchema"] = "air_quality_index_item.json"
    data["refCatalogueSchemaRelease"] = "0.1.0"
    data["tags"] = ["virtual_sensor", "test_sensor"]
    data["accessMechanism"] = {}
    data["latitude"] = {
        "value": 12.9715987,
        "ontologyRef": "http://www.w3.org/2003/01/geo/wgs84_pos#"}
    data["longitude"] = {
        "value": 77.5945627,
        "ontologyRef": "http://www.w3.org/2003/01/geo/wgs84_pos#"}

    data_schema = dict()
    data_schema["city"] = api_json['data']['city']['name']
    data_schema["geo"] = api_json['data']['city']['geo']
    data_schema["humidity"] = api_json['data']['iaqi']['h']['v']
    data_schema["pressure"] = api_json['data']['iaqi']['p']['v']
    data_schema["ozone"] = api_json['data']['iaqi']['o3']['v']
    data_schema["temperature"] = api_json['data']['iaqi']['t']['v']
    data_schema["time"] = api_json['data']['time']['s']

    data["data_schema"] = data_schema

    with open('air_quality_index_data.json', 'w+') as jsonfile:
        json.dump(data, jsonfile, indent=4, sort_keys=True)


def generate_schema():
    """ Creates a schema for demo sensor's data presented in generate_data().
    Returns a schema file
    """
    generic_base_iot_schema_template = {
        "type": "object",
        "properties": {
            "accessMechanism": {
                "type": "object",
                "properties": {
                    "accessEndPoint": {
                        "type": "object",
                        "properties": {
                            "describes": {
                                "type": "string"
                            },
                            "value": {
                                "type": "string",
                                "format": "uri"
                            }
                        }
                    },
                    "additionalResourceInfo": {
                        "type": "object",
                        "properties": {
                            "describes": {
                                "type": "string"
                            },
                            "value": {
                                "type": "string",
                                "format": "uri"
                            }
                        }
                    },
                    "requestAccessSite": {
                        "type": "object",
                        "properties": {
                            "describes": {
                                "type": "string"
                            },
                            "value": {
                                "type": "string",
                                "format": "uri"
                            }
                        }
                    },
                    "resourceAPIInfo": {
                        "type": "object",
                        "properties": {
                            "describes": {
                                "type": "string"
                            },
                            "value": {
                                "type": "string",
                                "format": "uri"
                            }
                        }
                    },
                    "subscriptionEndPoint": {
                        "type": "object",
                        "properties": {
                            "describes": {
                                "type": "string"
                            },
                            "value": {
                                "type": "string",
                                "format": "uri"
                            }
                        }
                    },
                    "updateEndPoint": {
                        "type": "object",
                        "properties": {
                            "describes": {
                                "type": "string"
                            },
                            "value": {
                                "type": "string",
                                "format": "uri"
                            }
                        }
                    }
                }
            },
            "id": {
                "type": "string"
            },
            "owner": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "website": {
                        "type": "string",
                        "format": "uri"
                    }
                },
                "required": [
                    "name"
                ]
            },
            "provider": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "website": {
                        "type": "string",
                        "format": "uri"
                    }
                },
                "required": [
                    "name"
                ]
            },
            "refCatalogueSchema": {
                "type": "string"
            },
            "refCatalogueSchemaRelease": {
                "type": "string"
            },
            "tags": {
                "type": "array"
            }
        }
    }

    data_schema = {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "units": "dimensionless",
                "description": "Name of the city where Air Quality Index is taken",
                "permissions": "read-write",
                "accessModifier": "protected"
            },
            "geo": {
                "type": "array",
                "minItems": 2,
                "describes": "2 element array having latitude and longitude",
                "items": {
                    "type": "number"
                }
            },
            "humidity": {
                "type": "number",
                "describes": "Humidity levels",
                "units": "percent",
                "accessModifier": "protected"
            },
            "ozone": {
                "type": "number",
                "describes": "Ozone levels",
                "units": "µg/m3",
                "accessModifier": "protected"
            },
            "temperature": {
                "type": "number",
                "describes": "Temperature in the area",
                "units": "Celsius",
                "accessModifier": "protected"
            },
            "pressure": {
                "type": "number",
                "describes": "Pressure levels",
                "units": "hPa",
                "accessModifier": "protected"
            },
            "time": {
                "type": "string",
                "describes": "Time when data was taken",
                "units": "YYYY-MM-DD HH:MM:SS",
                "accessModifier": "protected"
            }
        },
        "additionalProperties": True
    }
    generic_base_iot_schema_template["properties"]["data_schema"] = data_schema

    with open('air_quality_index_item.json', 'w+') as jsonfile:
        json.dump(generic_base_iot_schema_template, jsonfile, indent=4)


if __name__ == "__main__":
    generate_data()
    generate_schema()
