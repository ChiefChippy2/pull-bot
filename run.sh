cd bot/

echo "Vérification du fichier .env en cours"
python3.9 verify_env.py
echo "Lancement du bot..."
python3.9 src/main.py
echo "Pour garder le bot en ligne, veuillez utiliser `screen -S bot python3.9 src/main.py`, ou bien `screen -S bot ./run.sh`"