if [ -z "$GOOGLE_CREDENTIALS" ]
then
    echo No Google Credential Env
else
    echo ${GOOGLE_CREDENTIALS} > google-credentials.json
fi