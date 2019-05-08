# Flask-SQLAlchemy

## 扩展配置

修改源码支持 engine 参数 `site-packages/flask_sqlalchemy/__init__.py`

参考:

https://github.com/pallets/flask-sqlalchemy/issues/166#issuecomment-281398183

https://github.com/PeterParker/flask-sqlalchemy/commit/5e17c5622bec8f6a66ed10e093faf501fc69c895

```
options = {'convert_unicode': True}
self._sa.apply_pool_defaults(self._app, options)
self._sa.apply_driver_hacks(self._app, info, options)
if echo:
    options['echo'] = echo

# next two lines are new
config_engine_opts = self._app.config.get('SQLALCHEMY_ENGINE_OPTS', {})
options.update(config_engine_opts)

self._engine = rv = sqlalchemy.create_engine(info, **options)
```
