### > Checks if environment variable file ".env" is present
if [ -f "../../.env" ]; then
  printf "File: .env is present !!!\n\n"
else
  echo "File: .env is not present"
  ERR
fi

docker compose up --build -d