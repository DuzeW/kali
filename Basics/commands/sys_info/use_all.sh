#!/bin/bash

for s in *.sh
do
  if [[ "$s" != "use_all.sh" ]]; then
  echo -e "\e[35mUruchomiono $s\e[0m"
  ./"$s"
  fi
done

