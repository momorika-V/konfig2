#!/bin/sh
cd "$(dirname "$0")" || exit 1
PYTHON=python3
command -v python3 >/dev/null 2>&1 || PYTHON=python
echo "Команды: аргументы программы, test - тесты, exit - выход."
while true; do
    printf "> "
    read -r line || break
    if [ "$line" = "exit" ]; then
        break
    fi
    if [ "$line" = "test" ]; then
        $PYTHON -m unittest discover -s tests -v
        continue
    fi
    $PYTHON src/main.py $line
done
