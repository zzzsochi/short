==================
Simple URL shorter
==================

-----
Start
-----

.. code:: shell

    sudo aptitude install redis-server
    pip install 'git+http://github.com/zzzsochi/short.git'
    short serve --host=0.0.0.0 --port=8080

Use `short serve --help` for additional information.

---
API
---

**POST /**

:request:
    :headers:
        :Content-Type: Application/json
    :json:
        :url: URL for short

:response:
    :status: 200
    :headers:
        :Content-Type: Application/json
    :json:
        :url: Short url

**GET /short_url**

:response:
    :status: 302
    :headers:
        :Location: Original URL
