curl --request POST \
--url https://api.sendgrid.com/v3/mail/send \
--header 'Authorization: Bearer <<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>>' \
--header 'Content-Type: application/json' \
--data '{"personalizations":[{"to":[{"email":"lindanjau21@gmail.com","name":"Linda Njau"}],"subject":"Hello, World!"}],"content": [{"type": "text/plain", "value": "Heya!"}],"from":{"email":""mucunguzia@gmail.com"","name":"Sam Smith"},"reply_to":{"email":""mucunguzia@gmail.com"","name":"Sam Smith"}}'
