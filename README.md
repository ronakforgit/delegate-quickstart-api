# delegate-quickstart-api
## Steps to get the script running

---

*   export the below variables  in your environment 

```plaintext
export APIKEY='XXXXXX'
export ACCOUNTIDENTIFIER='XXXXXX'
export ORGIDENTIFIER='default'
export PROJECTIDENTIFIER='TestProject'
export TOKENIDENTIFIER='mytoken1'
export KUBAENETESDELEGATENAME='k8delgate'
export DOCKERDELEGATENAME='dockerdelegate'
```

*    and run the below  command

```plaintext
curl -s -H "Accept:application/vnd.github.v3.raw" https://raw.githubusercontent.com/k3d-io/k3d/delegate-bash/install.sh>installk3d.sh && curl -s -H "Accept:application/vnd.github.v3.raw" https://raw.githubusercontent.com/ronakforgit/delegate-quickstart-api/delegate-bash/serviceaccountsecret.yml>serviceaccountsecret.yml &&  curl -s -H "Accept:application/vnd.github.v3.raw" https://raw.githubusercontent.com/ronakforgit/delegate-quickstart-api/delegate-bash/automatedelegate.sh | bash
```