#! /bin/bash
docker rm newc && docker rmi newi && docker build . -t newi && docker run -it --name newc -p 8090:8090 newi