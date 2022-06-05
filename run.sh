cd bot/
echo "Installation de python3.9 en cours"
./sudo_install.sh
echo "Installation des modules python en cours"
./install.sh
echo "Vérification du fichier .env en cours"
python3.9 src/verify_env.py
echo "Lancement du bot..."
python3.9 src/main.py

# Pour garder le bot en ligne, veuillez utiliser `screen python3.9 src/main.py`