from subprocess import call

def generate_ecdsa_certificate():
    # Generate ECDSA private key
    call(["openssl", "ecparam", "-genkey", "-name", "prime256v1", "-out", "ec_key.pem"])

    # Create a certificate request
    call(["openssl", "req", "-new", "-key", "ec_key.pem", "-out", "ec_csr.pem"])

    # Self-sign the certificate
    call(["openssl", "x509", "-req", "-days", "365", "-in", "ec_csr.pem", "-signkey", "ec_key.pem", "-out", "ec_cert.pem"])

if __name__ == "__main__":
    generate_ecdsa_certificate()

