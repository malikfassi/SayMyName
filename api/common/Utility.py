import collections
import copy
import datetime
from binascii import unhexlify

import os
import base64
from base64 import b64encode
from flask import abort
import random
import string
from functools import reduce
import yaml
from typing import Dict
import re
import json


class Utility:

    @staticmethod
    def is_json(myjson):
        try:
            json.loads(myjson)
        except ValueError:
            return False
        return True

    @staticmethod
    def random_pub_key():
        return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(100))

    @staticmethod
    def get_params_or_400(param_dict, *params):
        pair = lambda x : (x, param_dict[x])
        try:
            return dict(pair(x) for x in params)
        except (KeyError, TypeError):
            abort(400, 'Parameter not found')

    @staticmethod
    def get_param_or_400(param_dict, param):
        try:
            return param_dict[param]
        except KeyError:
            abort(400, 'Parameter not found')

    @staticmethod
    def get_param(param_dict, *params):
        pair = lambda x : (x, param_dict.get(x))
        return dict(pair(x) for x in params)

    @staticmethod
    def get_int_id_or_400(id):
        try:
            return int(id)
        except ValueError:
            abort(400, 'Bad ID value')

    @staticmethod
    def b64encode(source):
        encoded = base64.urlsafe_b64encode(source)
        return encoded.decode('utf-8').rstrip('=')

    @staticmethod
    def b64decode(source):
        missing_padding_length = (-len(source) % 4)
        return base64.urlsafe_b64decode(source + '=' * missing_padding_length)

    @staticmethod
    def generate_token(length):
        return b64encode(os.urandom(length))

    @staticmethod
    def flatten_list(my_list):
        return reduce(lambda x, y: x + y, my_list)

    @staticmethod
    def get_object_or_none_from_list(my_list):
        if len(my_list) > 0:
            return my_list[0]
        else:
            return {}

    @staticmethod
    def now_as_string():
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # take obj2 key if override
    @staticmethod
    def merge_objects(obj1, obj2):
        merged = dict()
        merged.update(obj1)
        merged.update(obj2)
        return merged

    @staticmethod
    def merge_list1_with_list2_by_key(list1, list2, key):
        final_obj_list = []
        for obj_list1 in list1:
            obj_list2_found = [obj_list2 for obj_list2 in list2 if obj_list2[key] == obj_list1[key]]
            obj_list2_found = Utility.get_object_or_none_from_list(obj_list2_found)
            if not obj_list2_found:  # empty: obj nit found
                final_obj_list.append(obj_list1)
            else:
                fusion = Utility.merge_objects(obj_list2_found, obj_list1)  # enrich dao obj with daemon obj
                final_obj_list.append(fusion)
        return final_obj_list

    @staticmethod
    def read_yaml(file_name: str) -> Dict:
        with open(file_name, 'r') as stream:
            try:
                data = yaml.load(stream)
                stream.close()
                return data
            except yaml.YAMLError as exc:
                stream.close()

    def get_env_conf(self) -> Dict:
        config = self.read_yaml('configuration/vault_conf.yaml')
        env = os.environ.get('FLASK_ENV', 'DEVELOPMENT_WITH_DB')
        return config.get(env, config)

    @staticmethod
    def get_type_name(name) -> str:
        return '_'.join(re.findall('[A-Z][^A-Z]*', name)).upper()

    @staticmethod
    def decode_device_signature(data):
        return b64encode(unhexlify(data)).decode('utf-8')

    @staticmethod
    def merge_gate_op_with_daemon_op(gate_op, daemon_operations):
        uid = gate_op['uid']
        for op in daemon_operations:
            if op['uid'] == uid:
                gate_op = Utility.merge_objects(gate_op, op)
                break
        return gate_op

    @staticmethod
    def get_organization(config_file='configuration/vault_conf.yaml'):
        with open(config_file) as f:
            c = yaml.load(f)
            f.close()
        return c['COMMON']['ORGANIZATION']

    @staticmethod
    def date_converter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    @staticmethod
    def utc_now():
        return datetime.datetime.now(datetime.timezone.utc)

    @staticmethod
    def deep_merge(d, u):
        """Do a deep merge of one dict into another.

        This will update d with values in u, but will not delete keys in d
        not found in u at some arbitrary depth of d. That is, u is deeply
        merged into d.

        Args -
          d, u: dicts

        Note: this is destructive to d, but not u.

        Returns: None
        """
        stack = [(d, u)]
        while stack:
            d, u = stack.pop(0)
            for k, v in u.items():
                if not isinstance(v, collections.Mapping):
                    # u[k] is not a dict, nothing to merge, so just set it,
                    # regardless if d[k] *was* a dict
                    d[k] = v
                else:
                    # note: u[k] is a dict

                    # get d[k], defaulting to a dict, if it doesn't previously
                    # exist
                    dv = d.setdefault(k, {})

                    if not isinstance(dv, collections.Mapping):
                        # d[k] is not a dict, so just set it to u[k],
                        # overriding whatever it was
                        d[k] = v
                    else:
                        # both d[k] and u[k] are dicts, push them on the stack
                        # to merge
                        stack.append((dv, v))