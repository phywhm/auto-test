#!/bin/bash

if [ x"$1" = x"test" ]; 
then
    export SAAS_HOST="saasauth-test.haimawan.com"
    export DB_HOST="172.16.2.16"
elif [ x"$1" = x"demo" ];
then
    export SAAS_HOST=saasauth-demo.haimawan.com
    export DB_HOST=172.16.2.99
elif [ x"$1" = x"pay" ];
then
    export SAAS_HOST=saasauth-pay.haimawan.com
    export DB_HOST=172.16.2.90
else
    echo "wrong env keyword, should be 'test', 'pay', 'demo'"
fi
