echo "Recherche d'une mise à jour sur GitHub..."
git pull
echo "Installation de python3.9 en cours"
./sudo_install.sh
echo "Installation des modules python en cours"
./install.sh
echo "OK"