==================
Simple URL shorter
==================

------------
Requirements
------------

* `Python`_ >= 3.4
* `Redis`_ > 1.0

.. _Redis: http://redis.io/
.. _Python: https://www.python.org/

-----
Start
-----

.. code:: shell

    sudo aptitude install redis-server  # or other path install redis
    pip install 'git+http://github.com/zzzsochi/aiohttp_traversal.git'
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
    :status: 301
    :headers:
        :Location: Original URL
