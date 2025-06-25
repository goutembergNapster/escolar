#!/bin/bash
PID=$(ps aux | grep runserver | grep -v grep | awk '{print $2}')
if [ ! -z "$PID" ]; then
  kill -9 $PID
  echo "Servidor Django parado."
else
  echo "Servidor Django não está em execução."
fi
