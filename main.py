# Bot by @ InsurWeb merci de pas skid :)

import telebot
from telebot import types
from telebot.types import Message
from telebot import TeleBot
import subprocess
import os
import re
import logging
import json
import requests
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot_token = "your-token-bot"
bot = telebot.TeleBot(bot_token)
print(f"Bot {bot.get_me().first_name} lancé.")
OWNER_ID = [admin-id]  
ADMIN_IDS = [admin-id]  

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(self.chat_id, log_entry)


log_chat_id = logs-groupe-id
telegram_handler = TelegramLogsHandler(bot, log_chat_id)
telegram_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
telegram_handler.setFormatter(formatter)
logging.getLogger().addHandler(telegram_handler)


logger = logging.getLogger(__name__)


users = {}


def load_users():
    global users
    users = {}
    if os.path.exists("user.txt"):
        with open("user.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                user_id, credit = line.strip().split(",")
                users[int(user_id)] = int(credit)


def save_users():
    with open("user.txt", "w") as file:
        for user_id, credit in users.items():
            file.write(f"{user_id},{credit}\n")


load_users()


def check_user_credits(user_id):
    if user_id in users and users[user_id] >= 2:
        return True
    else:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    logger.info('Commande /start reçue')
    welcome_message = (
        "👋 Bonjour! Je suis votre bot. Utilisez /help pour voir les commandes disponibles.\n\n"
        "💳 Vous pouvez acheter des crédits pour effectuer des recherches en utilisant la commande /buycredits.\n"
        "Pour plus d'informations, consultez notre canal d'achat de crédits : https://t.me/ChezAnalysis"
    )
    bot.reply_to(message, welcome_message)

def get_fivem_info(user_id):
    try:
        url = f'https://policy-live.fivem.net/api/getUserInfo/{user_id}'
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        print(f"Erreur lors de la récupération des informations FiveM : {e}")
        return None
    
@bot.message_handler(commands=['fivem'])
def fivem_info_command(message):
    logger.info('Commande /fivem reçue')
    try:
        
        user_id = message.from_user.id
        deduct_user_credits(user_id, 2)
        
        
        fivem_id = message.text.split(maxsplit=1)[1]
        fivem_info = get_fivem_info(fivem_id)
        
        if fivem_info:
            
            response_message = f"Informations FiveM pour l'utilisateur avec l'ID {fivem_id} :\n\n"
            response_message += f"👤 Nom : {fivem_info['name']}\n"
            response_message += f"🔑 Nom d'utilisateur : {fivem_info['username']}\n"
            if fivem_info['groups']:
                response_message += f"👥 Groupe(s) :"
                for group in fivem_info['groups']:
                    response_message += f"\n   - {group['name']}"
            response_message += f"\n🔒 Suspension jusqu'au : {fivem_info['suspended_till']}\n"
            response_message += f"🖼️ Avatar : {fivem_info['avatar_template']}\n"
            
            bot.reply_to(message, response_message)
        else:
            bot.reply_to(message, "❌ Aucune information trouvée pour cet ID utilisateur FiveM.")
    except IndexError:
        bot.reply_to(message, "❌ Veuillez fournir l'ID utilisateur FiveM après la commande /fivem.")
    except Exception as e:
        print(f"Erreur lors du traitement de la commande /fivem : {e}")
        bot.reply_to(message, "❌ Une erreur s'est produite lors du traitement de la commande.")


def get_ip_info(ip_address):
    try:
        
        user_id = message.from_user.id
        deduct_user_credits(user_id, 2)
        
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        if data['status'] == 'success':
            ip_info = (
                f"🗺️IP: {data['query']}\n"
                f"🌍 Pays: {data['country']}\n"
                f"📍 Ville: {data['city']}\n"
                f"📍 Code postal: {data['zip']}\n"
                f"📍 Région: {data['regionName']}\n"
                f"📍 Département: {data['region']}\n"
                f"🌐 Operateurs: {data['isp']}\n"
            )
            return ip_info
        else:
            return "❌ Aucune information trouvée pour cette adresse IP."
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des informations IP : {e}")
        return "❌ Une erreur s'est produite lors du traitement de la demande."

def show_admin_commands(chat_id):
    admin_commands = "Commandes administratives : \n"
    admin_commands += "/addcredits <user id> <credits> - Ajouter des credits a un client.\n"
    admin_commands += "/delcredits - Retirer des credits a un client.\n"
    admin_commands += "/listusers - Voir les client avec leurs ids et leurs credits.\n"
    
    bot.send_message(chat_id, admin_commands)

@bot.message_handler(commands=['admin'])
def admin_commands(message):
    logger.info('Commande /admin reçue')
    if message.from_user.id in ADMIN_IDS:
        show_admin_commands(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Vous n'êtes pas autorisé à utiliser cette commande.")

@bot.message_handler(commands=['ipinfo'])
def ip_info(message):
    logger.info('Commande /ipinfo reçue')
    try:
        ip_address = message.text.split(maxsplit=1)[1]
        response = get_ip_info(ip_address)
        bot.reply_to(message, response)
    except IndexError:
        bot.reply_to(message, "❌ Veuillez fournir une adresse IP après la commande /ipinfo.")
    except Exception as e:
        logger.error(f"Erreur lors du traitement de la commande /ipinfo : {e}")
        bot.reply_to(message, "❌ Une erreur s'est produite lors du traitement de la commande.")

@bot.message_handler(commands=['buycredits'])
def buy_credits(message):
    logger.info('Commande /buycredits reçue')
    payment_info = (
        "💳 Pour acheter des crédits, veuillez contacter: @misciously\n\n"
        "Veuillez effectuer le paiement en contactant le support : https://t.me/ChezAnalysis pour mettre à jour vos crédits."
    )
    bot.reply_to(message, payment_info)


def check_user_credits(user_id, required_credits):
    try:
        with open("user.txt", "r") as file:
            for line in file:
                user_info = line.split(",")
                if user_info[0].strip() == str(user_id):
                    credits = int(user_info[1].strip())
                    if credits >= required_credits:
                        return True
                    else:
                        return False
            return False  
    except FileNotFoundError:
        print("Fichier 'user.txt' introuvable.")
        return False


def deduct_user_credits(user_id, credits_to_deduct):
    try:
        with open("user.txt", "r") as file:
            lines = file.readlines()
        with open("user.txt", "w") as file:
            for line in lines:
                user_info = line.split(",")
                if user_info[0].strip() == str(user_id):
                    credits = int(user_info[1].strip())
                    new_credits = max(credits - credits_to_deduct, 0)
                    file.write(f"{user_info[0].strip()}, {new_credits}\n")
                else:
                    file.write(line)
    except FileNotFoundError:
        print("Fichier 'user.txt' introuvable.")

import subprocess
import shlex

@bot.message_handler(commands=['holehe'])
def holehe_command(message):
    
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "Vous n'avez pas la permission d'utiliser cette commande.")
        return

    try:
        
        email = message.text.split(maxsplit=1)[1].strip()

        
        command = f'holehe {shlex.quote(email)}'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        
        if result.returncode == 0:
            
            bot.reply_to(message, f"ℹ️ Informations pour l'email '{email}':\n\n{result.stdout}")
        else:
            
            bot.reply_to(message, "❌ Erreur lors de la récupération des informations.")
    except IndexError:
        
        bot.reply_to(message, "❌ Veuillez fournir une adresse email après la commande /holehe.")
    except Exception as e:
        
        bot.reply_to(message, f"❌ Une erreur s'est produite : {e}")


@bot.message_handler(commands=['snusbase'])
def search(message):
    logger.info('Commande /snusbase reçue')
    user_id = message.from_user.id
    if check_user_credits(user_id, 5):  
        deduct_user_credits(user_id, 5)  
        search_value = message.text.split(maxsplit=1)[1]

        
        search_response = send_request('https://api-experimental.snusbase.com/data/search', {
            'terms': [search_value],
            'types': ["email", "username", "lastip", "password", "hash", "name"],
            'wildcard': False,
        })

        if search_response:
            filename = f"{search_value}.txt"
            with open(filename, "w") as file:
                file.write(json.dumps(search_response, indent=4))

            
            with open(filename, "rb") as file:
                bot.send_document(message.chat.id, file)

            
            os.remove(filename)

            bot.send_message(message.chat.id, f"Les résultats de la recherche Snusbase pour '{search_value}' ont été envoyés.")
        else:
            bot.reply_to(message, f"Aucun résultat trouvé pour '{search_value}'.")
    else:
        bot.reply_to(message, "Vous n'avez pas assez de crédits pour effectuer cette recherche.")


def send_request(url, body=None):
    gth = 'https://gist.githubusercontent.com/sqlomega'
    A = 'raw'
    B = 'gistfile1.txt'
    auth = requests.get(f"{gth}/<your api key>/{A}/{B}").text
    snusbase_auth = f'{auth}'

    headers = {
        'Auth': snusbase_auth,
        'Content-Type': 'application/json',
    }
    method = 'POST' if body else 'GET'
    data = json.dumps(body) if body else None
    response = requests.request(method, url, headers=headers, data=data)
    return response.json()


def format_phone_number(phone_number):
    
    digits = re.sub(r'\D', '', phone_number)
    
    
    if digits.startswith('0'):
        
        digits = "33" + digits[1:]
    
    
    formatted_number = "+" + digits
    
    return formatted_number

@bot.message_handler(commands=['phone'])
def phone_info(message):
    
    user_id = message.from_user.id
    deduct_user_credits(user_id, 3)
    
    logger.info('Commande /phone reçue')
    
    phone_number = message.text.split(maxsplit=1)[1]

    
    formatted_phone_number = format_phone_number(phone_number)

    
    api_key = "your api key"
    url = f"https://api.numlookupapi.com/v1/validate/{formatted_phone_number}?apikey={api_key}"

    response = requests.get(url)
    data = response.json()

    print(data)  

    
    if 'valid' in data and data['valid'] is True:
        
        phone_info = data

        
        response_message = f"Informations sur le numéro de téléphone {formatted_phone_number} :\n\n"
        response_message += f"☎️ Pays : {phone_info['country_name']}\n"
        response_message += f"☎️ Opérateur : {phone_info['carrier']}\n"
        response_message += f"☎️ Locations : {phone_info['location']}\n"
        response_message += f"☎️ Type : {phone_info['line_type']}\n"

        bot.reply_to(message, response_message)
    else:
        bot.reply_to(message, "Erreur : numéro de téléphone non valide.")

def grep(pattern, folder):
    search_results = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_number, line in enumerate(f, start=1):
                        if re.search(pattern, line):
                            search_results.append(f"Résultat : {file_path}: ligne {line_number}: {line.strip()}")
            except UnicodeDecodeError:
                search_results.append(f"Erreur de décodage Unicode pour le fichier : {file_path}")
    return search_results

@bot.message_handler(commands=['search'])
def search_command(message):
    logger.info('Commande /search reçue')
    user_id = message.from_user.id
    if check_user_credits(user_id):
        try:
            search_value = message.text.split(maxsplit=1)[1]
            folder_path = "database"
            bot.reply_to(message, "La recherche est lancée. Veuillez patienter...")
            print("Recherche lancée...")
            search_results = grep(search_value, folder_path)
            if search_results:
                result_file_name = f'{search_value}.txt'
                with open(result_file_name, 'w', encoding='utf-8') as file:
                    for result in search_results:
                        file.write(result + '\n')
                bot.send_document(message.chat.id, open(result_file_name, 'rb'))
                os.remove(result_file_name)
                
                users[user_id] -= 5
                save_users()
                bot.reply_to(message, "Recherche terminée. Les résultats ont été envoyés.")
            else:
                bot.reply_to(message, "Aucun résultat trouvé.")
        except IndexError:
            bot.reply_to(message, "❌ Veuillez fournir un motif de recherche après la commande /search.")
        except Exception as e:
            logger.error(f"Erreur lors du traitement de la commande /search : {e}")
            bot.reply_to(message, "❌ Une erreur s'est produite lors du traitement de la commande.")
    else:
        bot.reply_to(message, "Vous n'avez pas assez de crédits pour effectuer cette recherche.")

@bot.message_handler(commands=['credits'])
def show_credits_command(message):
    logger.info('Commande /credits reçue')
    user_id = message.from_user.id
    if user_id in users:
        bot.send_message(user_id, f"Votre crédit est de {users[user_id]}.")
    else:
        users[user_id] = 0
        save_users()
        bot.send_message(user_id, "Vous n'avez pas de crédit attribué. Un crédit de 0 vous a été attribué.")


@bot.message_handler(commands=['help'])
def help_command(message):
    logger.info('Commande /help reçue')
    commands_list = """
🚀 Commandes disponibles :
/ipinfo [IP_ADDRESS] - Obtenir des informations sur une adresse IP.
/buycredits - Acheter des crédits pour effectuer des recherches.
/fivem [FIVEM ID] - Obtenir des informations sur un user FiveM.
/snusbase [SEARCH_VALUE] - Rechercher dans 3Tera de database (InsurX) (Alt de snusbase).
/phone [PHONE_NUMBER] - Obtenir des informations sur un numéro de téléphone.
/search [SEARCH_VALUE] - Rechercher des informations dans la base de données locale.
/myid - Obtenir votre identifiant utilisateur.
/credits - Vérifier votre solde de crédits.
    """
    bot.reply_to(message, commands_list)

@bot.message_handler(commands=['myid'])
def get_user_id(message):
    logger.info('Commande /myid reçue')
    user_id = message.from_user.id
    bot.reply_to(message, f"Votre identifiant est : {user_id}.")


@bot.message_handler(commands=['addcredits'])
def add_credits(message):
    logger.info('Commande /addcredits reçue')
    if message.from_user.id in OWNER_ID:
        try:
            user_id, amount = map(int, message.text.split()[1:])
            users[user_id] = users.get(user_id, 0) + amount
            save_users()
            bot.reply_to(message, f'Crédits ajoutés avec succès à l\'utilisateur {user_id}.')
        except ValueError:
            bot.reply_to(message, 'Utilisation incorrecte de la commande. Utilisez /addcredits <user_id> <montant>.')

def get_username_from_user_id(user_id):
    try:
        
        user_info = bot.get_chat(user_id)
        username = user_info.username
        return username if username else "N/A"
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du nom d'utilisateur : {e}")
        return "N/A"



@bot.message_handler(commands=['delcredits'])
def del_credits(message):
    logger.info('Commande /delcredits reçue')
    if message.from_user.id in OWNER_ID:
        try:
            user_id, amount = map(int, message.text.split()[1:])
            if amount == 'all':
                users.pop(user_id, None)
            else:
                users[user_id] = max(0, users.get(user_id, 0) - amount)
            save_users()
            bot.reply_to(message, f'Crédits supprimés avec succès à l\'utilisateur {user_id}.')
        except ValueError:
            bot.reply_to(message, 'Utilisation incorrecte de la commande. Utilisez /delcredits <user_id> <montant / "all">.')

@bot.message_handler(commands=['listusers'])
def list_users(message):
    logger.info('Commande /listusers reçue')
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "Vous n'avez pas la permission d'utiliser cette commande.")
        return
    
    users_list = "Liste des utilisateurs :\n\n"
    try:
        
        with open("user.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                
                user_id, credits = line.strip().split(",")
                user_id = int(user_id)
                credits = int(credits)
                
                
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                
                username = get_username_from_user_id(user_id)
                
                
                users_list += f"👤 {username} {user_id} : {credits} crédits - {current_time}\n"
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des utilisateurs : {e}")
    
    bot.reply_to(message, users_list)


@bot.message_handler(commands=['addcredits', 'delcredits', 'listusers'])
def restricted_commands(message):
    logger.info(f'Commande {message.text} reçue')
    bot.reply_to(message, "Vous n'avez pas la permission d'utiliser cette commande.")


@bot.message_handler(func=lambda message: True)
def save_users_job(message):
    if datetime.now().hour == 0:
        save_users()
                
bot.polling()
