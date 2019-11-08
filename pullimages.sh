#/bin/bash

curl http://metadata.google.internal/computeMetadata/v1/instance/zone -H "Metadata-Flavor: Google"