"""Genera CA y certificado localhost para desarrollo, sin tocar la confianza del SO."""
import argparse
import ipaddress
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID


def generar(salida):
    archivos = [salida / nombre for nombre in ("ca.crt", "localhost.crt", "localhost.key")]
    if any(archivo.exists() for archivo in archivos):
        if all(archivo.exists() for archivo in archivos):
            print("TLS local ya preparado; no se sobrescriben archivos existentes.")
            return
        raise SystemExit("El directorio contiene una preparación parcial. Usa otra ruta --salida.")
    ahora = datetime.now(timezone.utc)
    clave_ca = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    nombre_ca = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "PJL desarrollo local")])
    ca = (x509.CertificateBuilder().subject_name(nombre_ca).issuer_name(nombre_ca)
          .public_key(clave_ca.public_key()).serial_number(x509.random_serial_number())
          .not_valid_before(ahora - timedelta(minutes=5)).not_valid_after(ahora + timedelta(days=30))
          .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
          .add_extension(x509.KeyUsage(digital_signature=True, content_commitment=False,
                                      key_encipherment=False, data_encipherment=False, key_agreement=False,
                                      key_cert_sign=True, crl_sign=True, encipher_only=None, decipher_only=None), critical=True)
          .add_extension(x509.SubjectKeyIdentifier.from_public_key(clave_ca.public_key()), critical=False)
          .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(clave_ca.public_key()), critical=False)
          .sign(clave_ca, hashes.SHA256()))
    clave = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    certificado = (x509.CertificateBuilder()
                   .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")]))
                   .issuer_name(ca.subject).public_key(clave.public_key()).serial_number(x509.random_serial_number())
                   .not_valid_before(ahora - timedelta(minutes=5)).not_valid_after(ahora + timedelta(days=30))
                   .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
                   .add_extension(x509.SubjectAlternativeName([
                       x509.DNSName("localhost"), x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
                       x509.IPAddress(ipaddress.ip_address("::1"))]), critical=False)
                   .add_extension(x509.KeyUsage(digital_signature=True, content_commitment=False,
                                               key_encipherment=True, data_encipherment=False, key_agreement=False,
                                               key_cert_sign=False, crl_sign=False, encipher_only=None, decipher_only=None), critical=True)
                   .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
                   .add_extension(x509.SubjectKeyIdentifier.from_public_key(clave.public_key()), critical=False)
                   .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(clave_ca.public_key()), critical=False)
                   .sign(clave_ca, hashes.SHA256()))
    salida.mkdir(parents=True, exist_ok=True)
    archivos[0].write_bytes(ca.public_bytes(serialization.Encoding.PEM))
    archivos[1].write_bytes(certificado.public_bytes(serialization.Encoding.PEM))
    archivos[2].write_bytes(clave.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                              serialization.NoEncryption()))
    print("TLS local preparado para localhost y loopback, válido 30 días. No se instaló confianza en el sistema.")


if __name__ == "__main__":
    argumentos = argparse.ArgumentParser(description=__doc__)
    argumentos.add_argument("--salida", type=Path, default=Path(__file__).resolve().parents[1] / ".local-tls")
    generar(argumentos.parse_args().salida)
