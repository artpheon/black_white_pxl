#! /bin/bash
/bin/bash ./clean_dock.sh ; docker build . -t newi && docker run -it --name newc -p 8090:8090 newi