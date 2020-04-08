#!/usr/bin/env python

'''
Merges a certificate template with recipients defined in a roster file. The result is
unsigned certificates that can be given to cert-issuer.
'''
import copy
import hashlib
import json
import os
import uuid

from cert_core.cert_model.model import scope_name
from cert_schema import schema_validator

from students import helpers
from students import jsonpath_helpers


class Recipient:
    def __init__(self, fields):
        self.name = fields.pop('name')
        self.pubkey = fields.pop('pubkey')
        self.identity = fields.pop('identity')

        self.additional_fields = fields


def hash_and_salt_email_address(email, salt):
    return 'sha256$' + hashlib.sha256(email + salt).hexdigest()


def instantiate_assertion(cert, uid, issued_on):
    cert['issuedOn'] = issued_on
    cert['id'] = helpers.URN_UUID_PREFIX + uid
    return cert


def instantiate_recipient(cert, recipient, additional_fields, hash_emails):

    if hash_emails:
        salt = helpers.encode(os.urandom(16))
        cert['recipient']['hashed'] = True
        cert['recipient']['salt'] = salt
        cert['recipient']['identity'] = hash_and_salt_email_address(recipient["identity"], salt)
    else:
        cert['recipient']['identity'] = recipient["identity"]
        cert['recipient']['hashed'] = False

    profile_field = scope_name('recipientProfile')

    cert[profile_field] = {}
    cert[profile_field]['type'] = ['RecipientProfile', 'Extension']
    cert[profile_field]['name'] = recipient["name"]
    cert[profile_field]['publicKey'] = "ecdsa-koblitz-pubkey:" + recipient["pubkey"]

    if additional_fields:
        if not recipient["additional_fields"]:
            raise Exception('expected additional recipient fields but none found')
        for field in additional_fields:
            # TODO 如果有additional_fields需要修改这里的代码
            cert = jsonpath_helpers.set_field(cert, field['path'], recipient.additional_fields[field['csv_column']])
    else:
        if recipient["additional_fields"]:
            # throw an exception on this in case it's a user error. We may decide to remove this if it's a nuisance
            raise Exception(
                'there are fields that are not expected by the additional_per_recipient_fields configuration')


def create_unsigned_certificates_from_roster(template, recipients, use_identities, additionalFields, hash_emails):
    issued_on = helpers.create_iso8601_tz()

    certs = {}
    for recipient in recipients:
        if use_identities:
            uid = template['badge']['name'] + recipient["identity"]
            uid = "".join(c for c in uid if c.isalnum())
        else:
            uid = str(uuid.uuid4())

        cert = copy.deepcopy(template)

        instantiate_assertion(cert, uid, issued_on)
        instantiate_recipient(cert, recipient, additionalFields, hash_emails)

        # validate certificate before writing
        schema_validator.validate_v2(cert)

        certs[uid] = cert
    return certs


def instantiate_batch(config):
    from students.create_v2_certificate_template import create_certificate_template
    recipients = config["recipients"]
    template = create_certificate_template(config)
    use_identities = config["filename_format"] == "certname_identity"
    certs = create_unsigned_certificates_from_roster(template, recipients, use_identities, config["additional_per_recipient_fields"], config["hash_emails"])
    for uid in certs.keys():
        print(json.dumps(certs[uid]))
    return certs

def main():
    # conf = get_config()
    conf = {
        "badge_id": "",
        "cert_image": "http://127.0.0.1:8000/v1/api/files/file_wsid_d1d68fe7ca2cb3eed34802e4e85baf41/download/",
        "issuer_logo_wsid": "file_wsid_1e1d742e522bd156e7913acf67ad7808",
        "certificate_title": "cet4",
        "certificate_description": "四级",
        "issuer_id": "http://127.0.0.1:8000/v1/api/schools/21rrrrrrrrrrrrrrrrrrrrrrrh/issue/info",
        "issuer_name": "西南科技大学",
        "issuer_url": "https://www.baidu.com/",
        "issuer_email": "21444444444@qq.com",
        "issuer_public_key": "n2xrLhx2z9UeXcuU7fyCJ9ePn5fb4u4izU",
        "revocation_list": "http://127.0.0.1:8000/v1/api/schools/21rrrrrrrrrrrrrrrrrrrrrrrh/certificates/revocations",
        "criteria_narrative": "dj",
        "issuer_signature_lines": [{
            "signature_image_wsid": "file_wsid_5a108235157e3b4658005f2c06b34200",
            "job_title": "教授",
            "name": "Jess"
        }],
        "hash_emails": False,
        "display_html": {"@id": "schema:description"},
        "additional_global_fields": [{"path": "$.displayHtml", "value": "<h1>Some html code</h1>"},
                                     {"path": "$.@context",
                                      "value": ["https://w3id.org/openbadges/v2", "https://w3id.org/blockcerts/v2",
                                                {"displayHtml": {"@id": "schema:description"}}]}],
        "additional_per_recipient_fields": False,
        "recipients": [{"identity": "", "name": "", "pubkey": "", "additional_fields": ""}],
        "filename_format": "uuid"
    }
    instantiate_batch(conf)
    print('Instantiated batch!')


if __name__ == "__main__":
    main()
