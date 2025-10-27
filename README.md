## Environment Setup

The project uses encrypted environment variables. To set up:

1. Request the .env.gpg file and encryption password from the project admin
2. Place .env.gpg in the project root
3. The application will automatically decrypt environment variables on startup
4. If you need to modify environment variables:
   ```bash
   # Decrypt
   gpg -d .env.gpg > .env
   
   # Make your changes to .env
   
   # Re-encrypt
   gpg -c .env
   ```
5. Never commit the unencrypted .env file