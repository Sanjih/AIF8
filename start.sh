#!/bin/bash

echo "🛑 Arrêt des anciens processus..."
pkill -f "uvicorn api:app"
pkill -f "python3 bot.py"
pkill -f "cloudflared tunnel"
sleep 2

echo "🌐 Lancement du tunnel Cloudflare..."
# On lance cloudflared en arrière-plan et on cache les logs dans un fichier temporaire
cloudflared tunnel --url http://localhost:80 > /tmp/cloudflare.log 2>&1 &

echo "⏳ Attente de la génération de l'URL sécurisée (5 secondes)..."
sleep 5

# On extrait l'URL du fichier de logs
TUNNEL_URL=$(grep -oE 'https://[a-zA-Z0-9\-]+\.trycloudflare\.com' /tmp/cloudflare.log | head -n 1)

if [ -z "$TUNNEL_URL" ]; then
    echo "❌ ERREUR : Impossible de récupérer l'URL Cloudflare. Vérifiez votre connexion."
    exit 1
fi

echo "✅ URL obtenue : $TUNNEL_URL"

cd /root/AIF8

echo "🔧 Mise à jour automatique de bot.py..."
# On remplace l'ancienne URL par la nouvelle dans bot.py
sed -i "s|url=\"https://.*\.trycloudflare\.com.*\"|url=\"$TUNNEL_URL\"|g" bot.py

echo "🔧 Mise à jour automatique de index.html..."
# On remplace l'ancienne API_URL par la nouvelle dans index.html
sed -i "s|const API_URL = \".*\"|const API_URL = \"$TUNNEL_URL/api/fight\"|g" frontend/index.html

echo "🚀 Lancement de l'API dans un écran tmux..."
tmux kill-session -t api 2>/dev/null
tmux new-session -d -s api "cd /root/AIF8 && source venv/bin/activate && uvicorn api:app --host 127.0.0.1 --port 8000"

echo "🤖 Lancement du Bot dans un écran tmux..."
tmux kill-session -t bot 2>/dev/null
tmux new-session -d -s bot "cd /root/AIF8 && source venv/bin/activate && python3 bot.py"

echo "========================================="
echo "🎉 SUCCÈS ! Tout est lancé et opérationnel."
echo "🌐 Lien Web App : $TUNNEL_URL"
echo "========================================="
echo "Pour voir les logs de l'API : tape  -> tmux attach -t api"
echo "Pour voir les logs du Bot : tape  -> tmux attach -t bot"
