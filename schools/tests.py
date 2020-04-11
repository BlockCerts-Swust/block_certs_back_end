from django.test import TestCase

# Create your tests here.

# introduction_url = "http://www.baidu.com" + "intro/" if  "http://www.baidu.com/".endswith('/') else "/intro/"
# print(introduction_url)

class CertificateMetadata(object):
    def __init__(self, uid, unsigned_certs, signed_certs, blockcerts, final_blockcerts):
        self.uid = uid
        # self.unsigned_cert_file_name = os.path.join(unsigned_certs_dir, uid + file_extension)
        # if signed_certs_dir:
        #     self.signed_cert_file_name = os.path.join(signed_certs_dir, uid + file_extension)
        # self.blockchain_cert_file_name = os.path.join(blockcerts_dir, uid + file_extension)
        # self.final_blockchain_cert_file_name = os.path.join(final_blockcerts_dir, uid + file_extension)
        self.unsigned_certs  = unsigned_certs
        self.signed_certs = signed_certs
        self.blockcerts = blockcerts
        self.final_blockcerts = final_blockcerts

cert1 = CertificateMetadata(uid=0, unsigned_certs=[{"1": 1}, {"2": 2}],
                            signed_certs=[{"1": 1}, {"2": 2}],
                            blockcerts=[{"1": 1}, {"2": 2}],
                            final_blockcerts=[{"1": 1}, {"2": 2}])

cert2 = CertificateMetadata(uid=2, unsigned_certs=[{"3": 3}, {"4": 4}],
                            signed_certs=[{"3": 3}, {"4": 4}],
                            blockcerts=[{"3": 3}, {"4": 4}],
                            final_blockcerts=[{"3": 3}, {"4": 4}])

certificates_to_issue = {
    0: cert1,
    2: cert2
}

for uid, metadata in certificates_to_issue.items():
    print(uid)
    print(metadata)