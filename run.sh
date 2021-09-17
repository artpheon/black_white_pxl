#! /bin/bash
docker build . -t newimage && docker run -it --name newcontainer -p 8090:8090 newimage