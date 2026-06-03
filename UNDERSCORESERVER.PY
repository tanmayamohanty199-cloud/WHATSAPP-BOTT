from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# अपनी डिटेल्स यहाँ बदलें
ACCESS_TOKEN = 'EAAnzlUSYg7oBRgoZCRP0pBCdcFqyQ5syDluIZBZADkG5m10l3tcZBqDedT0s5fO8yhkNypYEq3EvsPPEWfe4ZA1KlZA9JGJ5aU1ZB6MgPNHbnFL8JDveu6BjkFIV2hN45dnNKUQlZBBg3zVa1527uFabtSBRLauZBfGfd3aaaysrTjnzmmwKMvMiw9JtTuzpJGAdvOWrNhDYZA3vkngcXIdCuENkXG9MNhtEQH56DuSPxzmxStOjLp766gcVOZBTFaZB4Ma1dInu0ZCaGEdjhUjlhGgUJMd25SwZDZD'
PHONE_NUMBER_ID = '1126929047176908'
NEWS_API_KEY = 'a6fdcb5917c449ce80e1e45b00e18921'

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # ये WhatsApp वेरिफिकेशन के लिए है
        return request.args.get("hub.challenge")

    elif request.method == "POST":
        data = request.json
        try:
            # मैसेज रिसीव करना
            message_data = data['entry'][0]['changes'][0]['value']['messages'][0]
            sender_id = message_data['from']
            company_name = message_data['text']['body'] 
            
            # NewsAPI से न्यूज़ लेना
            news_url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&apiKey={NEWS_API_KEY}"
            news_res = requests.get(news_url).json()
            
            if news_res.get('status') == 'ok' and news_res.get('articles'):
                headline = news_res['articles'][0]['title']
                response_text = f"News for {company_name}: {headline}"
            else:
                response_text = f"Sorry, no news found for {company_name}."

            # WhatsApp पर जवाब भेजना
            reply_url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"
            headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
            payload = {"messaging_product": "whatsapp", "to": sender_id, "text": {"body": response_text}}
            requests.post(reply_url, headers=headers, json=payload)
            
        except Exception as e:
            print(f"Error: {e}")
        return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=5000)
