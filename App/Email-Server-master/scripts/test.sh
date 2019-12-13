#!/usr/bin/env bash
echo "Mandando email..."
sudo echo "Teste email" | mail -s "Testando email Testando" localhost@localhost
echo "Email enviado!"