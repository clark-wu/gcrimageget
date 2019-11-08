#/bin/bash

curl http://metadata.google.internal/computeMetadata/v1/instance/zone -H "Metadata-Flavor: Google"
ls
git config --global user.name $1
git config --global user.password $2

git add -A
git commit -m 'add google script'
git push origin master
