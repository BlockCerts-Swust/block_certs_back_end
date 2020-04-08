#!/usr/bin/env python

'''
Creates a certificate template with merge tags for recipient/assertion-specific data.
'''
import json
import uuid

from common import common_function
from students import helpers
from students import jsonpath_helpers

from cert_core.cert_model.model import scope_name
from cert_schema import OPEN_BADGES_V2_CANONICAL_CONTEXT, BLOCKCERTS_V2_CANONICAL_CONTEXT

OPEN_BADGES_V2_CONTEXT = OPEN_BADGES_V2_CANONICAL_CONTEXT
BLOCKCERTS_V2_CONTEXT = BLOCKCERTS_V2_CANONICAL_CONTEXT
png_prefix = 'data:image/png;base64,'

def create_badge_section(config):
    cert_image = config["cert_image"]
    issuer_image = config["issuer_logo"]
    badge = {
        'type': 'BadgeClass',
        'id': helpers.URN_UUID_PREFIX + config["badge_id"],
        'name': config["certificate_title"],
        'description': config["certificate_description"],
        'image': cert_image,
        'issuer': {
            'id': config["issuer_id"],
            'type': 'Profile',
            'name': config["issuer_name"],
            'url': config["issuer_url"],
            'email': config["issuer_email"],
            'image': issuer_image,
            'revocationList': config["revocation_list"]
        }
    }

    badge['criteria'] = {}
    badge['criteria']['narrative'] = config["criteria_narrative"]

    if config["issuer_signature_lines"]:
        signature_lines = []
        for signature_line in config["issuer_signature_lines"]:
            signature_image = signature_line['signature_image']
            signature_lines.append(
                {
                    'type': [
                        'SignatureLine',
                        'Extension'
                    ],
                    'jobTitle': signature_line['job_title'],
                    'image': signature_image,
                    'name': signature_line['name']
                }
            )
        badge[scope_name('signatureLines')] = signature_lines

    return badge


def create_verification_section(config):
    verification = {
        'type': ['MerkleProofVerification2017', 'Extension'],
        'publicKey': config["issuer_public_key"]

    }
    return verification


def create_recipient_section(config):
    recipient = {
        "type": "email",
        "identity": "*|EMAIL|*",
        "hashed": config["hash_emails"]
    }
    return recipient


def create_recipient_profile_section():
    return {
        "type": ["RecipientProfile", "Extension"],
        "name": "*|NAME|*",
        "publicKey": "ecdsa-koblitz-pubkey:*|PUBKEY|*"
    }


def create_assertion_section(config):
    assertion = {
        "@context": [
            OPEN_BADGES_V2_CONTEXT,
            BLOCKCERTS_V2_CONTEXT,
            {
                "displayHtml": {"@id": "schema:description"}
            }
        ],
        "type": "Assertion",
        "displayHtml": config["display_html"],
        "issuedOn": "*|DATE|*",
        "id": helpers.URN_UUID_PREFIX + "*|CERTUID|*"
    }
    return assertion


def create_certificate_template(config):

    if not config["badge_id"]:
        badge_uuid = str(uuid.uuid4())
        print("Generated badge id {0}".format(badge_uuid))
        config["badge_id"] = badge_uuid

    badge = create_badge_section(config)
    verification = create_verification_section(config)
    assertion = create_assertion_section(config)
    recipient = create_recipient_section(config)
    recipient_profile = create_recipient_profile_section()

    assertion["recipient"] = recipient
    assertion[scope_name("recipientProfile")] = recipient_profile

    assertion["badge"] = badge
    assertion["verification"] = verification

    if config["additional_global_fields"]:
        for field in config["additional_global_fields"]:
            assertion = jsonpath_helpers.set_field(assertion, field["path"], field["value"])

    if config["additional_per_recipient_fields"]:
        for field in config["additional_per_recipient_fields"]:
            assertion = jsonpath_helpers.set_field(assertion, field["path"], field["value"])

    return assertion

def main():
    # conf = get_config()
    # print(conf)
    # print(type(conf))
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
        "issuer_public_key": "ecdsa-koblitz-pubkey:n2xrLhx2z9UeXcuU7fyCJ9ePn5fb4u4izU",
        "revocation_list": "http://127.0.0.1:8000/v1/api/schools/21rrrrrrrrrrrrrrrrrrrrrrrh/certificates/revocations",
        "criteria_narrative": "dj",
        "issuer_signature_lines": [{
            "signature_image_wsid": "file_wsid_5a108235157e3b4658005f2c06b34200",
            "job_title": "教授",
            "name": "Jess"
        }],
        "hash_emails": False,
        "display_html": { "@id": "schema:description" },
        "additional_global_fields": [{"path": "$.displayHtml","value": "<h1>Some html code</h1>"}, {"path": "$.@context","value": ["https://w3id.org/openbadges/v2", "https://w3id.org/blockcerts/v2", {"displayHtml": { "@id": "schema:description" }}]}],
        "additional_per_recipient_fields": False
    }
    assertion = create_certificate_template(conf)
    print(json.dumps(assertion))
    print("Created template!")


if __name__ == "__main__":
    main()
