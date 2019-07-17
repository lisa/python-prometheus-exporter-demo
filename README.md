# Who is Logged In?

Exposes to Prometheus who is logged in and how many sessions they have open. Broken out by hostname. If a user is not logged in, they will not appear.

## Exported Metrics

* `logged_in_users` - Gauge of how many sessions are open.
  * `hostname` - Which host
  * `username` - name of the user

