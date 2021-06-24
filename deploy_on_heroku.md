# Deploy docker image on heroku

First be sure that you have installed the `heroku cli` : [Download and install](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

Then follow this process: 

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.

```bash
$ heroku login
```

Log in to Container Registry

You must have Docker set up locally to continue. You should see output when you run this command.

```bash
docker ps
```

Now you can sign into Container Registry.

```bash
heroku container:login
```

Push your Docker-based app

Build the Dockerfile in the current directory and push the Docker image.  <strong style="color:red;">Warning: here we push the image on the `dyslexia-ocr` app</strong>

```bash
heroku container:push web -a dyslexia-ocr
```

Deploy the changes

Release the newly pushed images to deploy your app. <strong style="color:red;">Warning: here we deploy on the `dyslexia-ocr` app</strong>

```bash
heroku container:release web -a dyslexia-ocr
```
