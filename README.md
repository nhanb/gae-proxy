I wanted an HTTP(S) proxy on Google App Engine, because apparently you can get
rotating IPs for outgoing traffic automatically. Well it doesn't really rotate
but actually just _not guaranteed to stay stay static_. Worth a try anyway.

Originally wanted to implement a proper generic proxy but gave up fast because
while plain HTTP is easy, HTTPS requires actual tcp tunnelling which I'm not
really up for at the moment (is that even possible on GAE standard
evironment?).

So I devised my own "scheme". Dumbest thing that works right?

# Server

Create an `envars.yaml` file to store secret password:

```yaml
env_variables:
  GAEPROXY_KEY: "long long string"
```

Then just `gcloud app deploy`.

# Use

See comments in **app.py**.
