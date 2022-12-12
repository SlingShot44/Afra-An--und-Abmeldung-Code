#! /bin/bash

date
#New Cert
#Go to cert dir
cd /home/pi/Server/cert
#Create new Cert and Bundle
echo "Generate key"
openssl genrsa -out cert-key.pem 4096
echo "Generate CSR"
openssl req -new -sha256 -subj "/C=DE/ST=Saxony/L=Meissen/O=Sankt Afra/OU=IT/CN=abmeldung.afra" -key cert-key.pem -out cert.csr
echo "Generate Cert and bundle"
sudo openssl x509 -req -sha256 -days 61 -in cert.csr -out cert.pem -passin file:pwd.txt -CA ca.pem -CAkey ca-key.pem -extfile extfile.cnf -CAcreateserial
cat cert.pem ca.pem cert-key.pem > bundle.pem
#Replace bundle on server
echo "Upload Cert"
curl -X PUT -d '{}' --unix-socket /var/run/control.unit.sock http://localhost/config/listeners
curl -X DELETE --unix-socket /var/run/control.unit.sock http://localhost/certificates/bundle
curl -X PUT --data-binary @bundle.pem --unix-socket /var/run/control.unit.sock http://localhost/certificates/bundle
cd ../config
curl -X PUT --data-binary @unit.json --unix-socket /var/run/control.unit.sock http://localhost/config

#Delete stale sessions
echo "Purge Sessions"
/home/pi/Server/env/bin/python /home/pi/Server/manage.py clearsessions
echo "Done!"
echo " "
